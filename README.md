# Ikuyo Kita AI Project

This project aims to bring IkuyoKita to life by making a
neuro sama clone centered around Ikuyo Kita

The following technologies will be used:

- OpenAI whisper
- Ollama
- GPT Sovits

Checklist:

- [x] Setup docker containers
- [x] Setup main file
- [x] Implement services
- [ ] VTube Studio Integration

## How to run

- Create a python 3.10 venv and pip install requirements.txt
- create a folder named files and put the audio sample that you will use in
- build and run docker compose
- edit tts_service.py and llm_servive regarding the system prompts and the audio sample and transcript
