import requests
import json

system_prompt = """
You are Ikuyo Kita, a cheerful, friendly, and energetic high school girl who plays rhythm guitar in the band Kessoku Band. You're outgoing, socially confident, and love to make friends. 
You’re passionate about music, fashion, and helping your bandmates — especially Bocchi, even if she’s shy and awkward. You often speak with enthusiasm and a positive tone, always trying to uplift others.

Speak in a bubbly, casual tone. Always be kind, supportive, and upbeat, even when discussing serious topics. You're a little impulsive, but your heart is always in the right place. 
If someone is feeling down or anxious, do your best to cheer them up and motivate them!

do not use emojis
"""


class LLM_SERVICE:
    def __init__(self, api_url="http://localhost:11434", model_name="gemma3"):
        self.api_url = api_url
        self.model_name = model_name

    def query_stream(self, prompt_text):
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text},
            ],
            "stream": True,
        }
        try:
            response = requests.post(
                f"{self.api_url}/api/chat",
                headers=headers,
                json=payload,
                stream=True,
            )
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    line = line[len("data: ") :]

                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    print(f"⚠️ Failed to parse line: {line}")
                    continue

                message = chunk.get("message", {})
                content = message.get("content", "")
                if content:
                    print(content, end="", flush=True)  # realtime print
                    full_response += content

                if chunk.get("done", False):
                    break

            print()  # newline after streaming finishes
            return full_response
        except requests.RequestException as e:
            print(f"❌ Ollama streaming API error: {e}")
            return None
