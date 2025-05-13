from api.prompt import Prompt
import os
import requests

class ChatLLM:
    def __init__(self):
        self.prompt = Prompt()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = os.getenv("DEEPSEEK_MODEL", default="deepseek-chat")
        self.api_url = os.getenv("DEEPSEEK_API_URL", default="https://api.deepseek.com/v1/chat/completions")
        self.temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", default=0.7))
        self.max_tokens = int(os.getenv("DEEPSEEK_MAX_TOKENS", default=500))

    def get_response(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": self.prompt.generate_prompt(),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print("❌ DeepSeek API 錯誤：", response.text)
            return "發生錯誤，請稍後再試。"

    def add_msg(self, text):
        self.prompt.add_msg(text)
