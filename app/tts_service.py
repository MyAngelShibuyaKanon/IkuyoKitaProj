import requests
import pyaudio
import wave
import io


class TTS_SERVICE:
    def __init__(self, api_url="http://127.0.0.1:9880/tts"):
        self.api_url = api_url
        self.ref_audio_path = "/files/ref_audio_sample.mp3"
        self.prompt_text = "結束バンドに入って先輩の娘になりたかったの 友達より深く密"
        self.sample_rate = 32000  # or 24000 depending on GPT-SoVITS output

    def speak(self, text):
        payload = {
            "text": text,
            "text_lang": "en",
            "ref_audio_path": self.ref_audio_path,
            "prompt_text": self.prompt_text,
            "prompt_lang": "ja",
            "text_split_method": "cut5",
            "streaming_mode": True,  # <-- as bool, not string
            "top_k": 5,
            "top_p": 1,
            "temperature": 1,
            "repetition_penalty": 1.35,
            "speed_factor": 1.0,
            "sample_steps": 32,
        }

        try:
            print("🗣 Sending text to TTS engine...")
            response = requests.post(self.api_url, json=payload, stream=True)
            response.raise_for_status()

            buffer = b""
            header_size = 44
            header_parsed = False
            p = pyaudio.PyAudio()
            stream = None
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    if not header_parsed:
                        buffer += chunk
                        if len(buffer) >= header_size:
                            wav_header = buffer[:header_size]
                            wav_file = wave.open(io.BytesIO(wav_header), "rb")

                            channels = wav_file.getnchannels()
                            sample_width = wav_file.getsampwidth()
                            sample_rate = wav_file.getframerate()
                            wav_file.close()

                            stream = p.open(
                                format=p.get_format_from_width(sample_width),
                                channels=channels,
                                rate=sample_rate,
                                output=True,
                            )

                            # Write remaining data after header
                            stream.write(buffer[header_size:])
                            buffer = b""
                            header_parsed = True
                    else:
                        if stream:
                            stream.write(chunk)

            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()

            print("✅ Playback finished.")

        except requests.RequestException as e:
            print(f"❌ TTS API Error: {e}")
            return None
