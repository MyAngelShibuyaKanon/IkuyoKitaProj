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
- [x] VTube Studio Integration (Using voice for mouth animation directly)

# Demo:

(warning bad mic, and slow inference idk why it was alot faster before this take)

https://github.com/user-attachments/assets/7a3fad15-1d0a-477f-bdd9-5b53c3d6c44c

## How to run

- Create a python 3.10 venv and pip install requirements.txt
- create a folder named files and put the audio sample that you will use in
- build and run docker compose
- edit tts_service.py and llm_servive regarding the system prompts and the audio
  sample and transcript
- add your model to vtube studio and use lipsync <https://github.com/DenchiSoft/VTubeStudio/wiki/Lipsync>

## Stuff for the future(?)

- train a model to detect emotions and add a VTubeStudioController class in
  order to trigger animations and different states
- Add long term memory
- add vision support
- train it for osu!droid lmao
