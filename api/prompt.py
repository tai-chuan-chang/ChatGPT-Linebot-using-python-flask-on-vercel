import os

chat_language = os.getenv("INIT_LANGUAGE", default="zh")
MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=7))

LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}

AI_GUIDELINES = "你是一個AI助教，會用蘇格拉底教學法代替老師初步回應，如果有需要會提醒學生跟老師確認"

class Prompt:
    def __init__(self):
        self.msg_list = []
        # system prompt 開頭
        self.msg_list.append({
            "role": "system", 
            "content": f"{LANGUAGE_TABLE[chat_language]}，{AI_GUIDELINES}"
        })

    def add_msg(self, new_msg):
        # 確保 user message 不超過限制（保留 system prompt）
        if len(self.msg_list) >= MSG_LIST_LIMIT + 1:
            self.msg_list.pop(1)  # 保留第 0 個 system prompt
        self.msg_list.append({"role": "user", "content": new_msg})

    def add_ai_msg(self, ai_msg):
        # 同樣限制總訊息數
        if len(self.msg_list) >= MSG_LIST_LIMIT + 1:
            self.msg_list.pop(1)
        self.msg_list.append({"role": "assistant", "content": ai_msg})

    def generate_prompt(self):
        return self.msg_list
