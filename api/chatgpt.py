from api.prompt import Prompt
import os
import requests  # 改用 requests 發送 HTTP 請求

class DeepSeek:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("DEEPSEEK_MODEL", default="deepseek-chat")  # 預設模型
        self.temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", default=0.7))
        self.max_tokens = int(os.getenv("DEEPSEEK_MAX_TOKENS", default=2048))
        self.api_key = os.getenv("sk-0cb99e089f104f8f89cc3d4858552b90") #deepseek api key
        self.api_base = os.getenv("DEEPSEEK_API_BASE", default="https://api.deepseek.com/v1")  # API 基礎 URL

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
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()  # 檢查 HTTP 錯誤
            response_data = response.json()
            
            # 假設 DeepSeek API 返回格式與 OpenAI 類似
            return response_data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"DeepSeek API 請求失敗: {e}")
            return "抱歉，我暫時無法處理您的請求。請稍後再試。"
            
        except (KeyError, IndexError) as e:
            print(f"解析 DeepSeek API 響應失敗: {e}")
            return "抱歉，處理回應時出現問題。"

    def add_msg(self, text):
        self.prompt.add_msg(text)
