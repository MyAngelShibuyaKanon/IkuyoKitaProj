import speech_recognition as sr
from pywhispercpp.model import Model
from df.enhance import enhance, init_df, load_audio, save_audio
import wave
import tempfile
import os
import torchaudio
import numpy as np


class STT_SERVICE:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(sample_rate=16000)
        self.whisper = Model("small.en", print_realtime=False, print_progress=False)
        self.model, self.df_state, _ = init_df()

    def save_speech_audio(self, audio_data, path):
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data.get_raw_data())

    def is_valid_audio(self, path, min_duration=0.3, min_rms=50):
        try:
            with wave.open(path, "rb") as wf:
                n_frames = wf.getnframes()
                framerate = wf.getframerate()
                duration = n_frames / float(framerate)
                if duration < min_duration:
                    return False
                audio_data = wf.readframes(n_frames)
                samples = np.frombuffer(audio_data, dtype=np.int16)
                rms = np.sqrt(np.mean(samples.astype(np.float32) ** 2))
                return rms > min_rms
        except Exception:
            return False

    def resample_to_16k(self, in_path, out_path):
        waveform, sr = torchaudio.load(in_path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
            waveform = resampler(waveform)
        torchaudio.save(out_path, waveform, 16000)

    def denoise_audio_file(self, input_path, output_path_16k):
        audio, _ = load_audio(input_path, sr=self.df_state.sr())
        enhanced = enhance(self.model, self.df_state, audio)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            enhanced_path = tmpfile.name
        save_audio(enhanced_path, enhanced, self.df_state.sr())

        self.resample_to_16k(enhanced_path, output_path_16k)
        os.remove(enhanced_path)

    def transcribe(self, audio_path):
        if not self.is_valid_audio(audio_path):
            return None
        result = self.whisper.transcribe(audio_path)

        if isinstance(result, list):
            text = " ".join(segment.text for segment in result).strip()
        elif isinstance(result, dict):
            text = result.get("text", "").strip()
        else:
            text = ""

        if text and "[BLANK_AUDIO]" not in text:
            return text
        return None

    def listen_from_source(self, source):
        print("🎤 Listening for speech...")
        audio = self.recognizer.listen(source)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as raw_file:
            raw_path = raw_file.name
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as enhanced_file:
            enhanced_path = enhanced_file.name

        try:
            self.save_speech_audio(audio, raw_path)
            self.denoise_audio_file(raw_path, enhanced_path)
            text = self.transcribe(enhanced_path)
            return text
        finally:
            os.remove(raw_path)
            os.remove(enhanced_path)
