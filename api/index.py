from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.deepseek import DeepSeek  # 修改導入的類

import os

line_bot_api = LineBotApi(os.getenv("FpdNfeUp58OCtnjGKgtA6K+0eNZI8XhS6Ov5isHB2Kg/lmHnyng7DcLu3PRDgZSwHSXkAqOm0rNOcVqOCQPcp80Yo1o4jteqMA5j3dA6gs5CD3aBnn0MdyM+vLyXdpmdpir6h1r/s38NLylI5zTFMwdB04t89/1O/w1cDnyilFU="))
line_handler = WebhookHandler(os.getenv("f917b362eda1465eec9709359c397c68"))
working_status = os.getenv("DEFAULT_TALKING", default="true").lower() == "true"

app = Flask(__name__)
deepseek_bot = DeepSeek()  # 實例化 DeepSeek 而不是 ChatGPT

# domain root
@app.route('/')
def home():
    return 'Hello, World! This is a DeepSeek-powered Line bot!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    # 指令處理
    if event.message.text.lower() == "說話":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，現在由 DeepSeek 提供智慧支持！歡迎來跟我互動 ^_^ "))
        return

    if event.message.text.lower() == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說「說話」"))
        return

    if working_status:
        # 添加用戶消息到對話歷史
        deepseek_bot.add_msg(f"User: {event.message.text}")
        
        # 獲取 DeepSeek 的回應
        try:
            reply_msg = deepseek_bot.get_response()
            # 添加 AI 回應到對話歷史
            deepseek_bot.add_msg(f"Assistant: {reply_msg}")
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_msg))
        except Exception as e:
            app.logger.error(f"DeepSeek API 錯誤: {str(e)}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，處理您的請求時出現問題，請稍後再試。"))

if __name__ == "__main__":
    app.run()
