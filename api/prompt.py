import os

chat_language = os.getenv("INIT_LANGUAGE", default="zh")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=7))
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}

AI_GUIDELINES = '你是一個AI小幫手，會用簡單明瞭的句子跟我聊天'

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.initialize_conversation()
    
    def initialize_conversation(self):
        """初始化對話，添加系統提示"""
        self.msg_list = [{
            "role": "system",
            "content": f"{LANGUAGE_TABLE[chat_language]}, {AI_GUIDELINES}"
        }]
    
    def add_msg(self, new_msg):
        """
        添加新消息到對話列表
        自動檢測消息角色 (用戶或助手)
        """
        # 自動判斷消息角色
        if new_msg.startswith("User: "):
            role = "user"
            content = new_msg[len("User: "):]
        elif new_msg.startswith("Assistant: "):
            role = "assistant"
            content = new_msg[len("Assistant: "):]
        else:
            # 默認為用戶消息
            role = "user"
            content = new_msg
        
        # 維護消息列表長度
        if len(self.msg_list) >= MSG_LIST_LIMIT + 1:  # +1 是為了保留系統消息
            # 保留系統消息和最新的對話
            self.msg_list = [self.msg_list[0]] + self.msg_list[-(MSG_LIST_LIMIT-1):]
        
        self.msg_list.append({
            "role": role,
            "content": content
        })
    
    def generate_prompt(self):
        """生成符合 DeepSeek API 要求的提示格式"""
        return self.msg_list
    
    def clear_conversation(self):
        """清空對話歷史，保留系統提示"""
        self.initialize_conversation()
