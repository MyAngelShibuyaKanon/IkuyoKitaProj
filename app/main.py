from stt_service import STT_SERVICE
from llm_service import LLM_SERVICE
from tts_service import TTS_SERVICE


def main():
    stt = STT_SERVICE()
    llm = LLM_SERVICE()
    tts = TTS_SERVICE()
    print("Press Ctrl+C to exit.")
    with stt.mic as source:
        stt.recognizer.adjust_for_ambient_noise(source)
        try:
            while True:
                transcript = stt.listen_from_source(source)
                if transcript:
                    print("📝 Transcription:", transcript)
                    response = llm.query_stream(transcript)
                    if response:
                        print("🤖 Ollama response:", response)
                        # Send to TTS
                        audio_path = tts.speak(response)
                        if audio_path:
                            print(f"🔊 Audio available at {audio_path}")
                    else:
                        print("⚠️ No response from Ollama API.")
                else:
                    print("🗑️ No clear speech detected, try again.")
        except KeyboardInterrupt:
            print("\n🛑 Exiting...")


if __name__ == "__main__":
    main()
