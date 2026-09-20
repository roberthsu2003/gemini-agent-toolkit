"""
LINE 基礎教學 02：串接 Gemini 3.7 Flash AI 智慧對話助理
使用 line-bot-sdk v3、FastAPI 與 Google GenAI SDK (Interactions API)
功能：
1. 接收使用者私聊文字提問
2. 呼叫 LINE 官方 Loading 動態效果 (ShowLoadingAnimationRequest)
3. 調用 Gemini Interactions API 獲得高品質繁體中文回覆
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from google import genai
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    ShowLoadingAnimationRequest,
    TextMessage,
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    TextMessageContent,
)
import uvicorn

load_dotenv()

# 金鑰配置
LINE_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not LINE_SECRET or not LINE_TOKEN:
    print("❌ 請先在 .env 設定 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN！")

if not GEMINI_KEY:
    print("❌ 請先在 .env 設定 GEMINI_API_KEY！")

configuration = Configuration(access_token=LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
gemini_client = genai.Client(api_key=GEMINI_KEY)

app = FastAPI(title="LINE Gemini 3.7 AI Bot")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Gemini AI LINE Bot 運作中！"}


@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"


@handler.add(FollowEvent)
def handle_follow(event: FollowEvent):
    """歡迎訊息"""
    welcome_text = (
        "👋 你好！我是串接 Google 最新 Gemini 3.7 Flash 的 LINE AI 助理。\n\n"
        "你可以直接傳送任何問題、文章摘要、程式碼撰寫、語言翻譯或生活疑難雜症給我！"
    )
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=welcome_text)]
            )
        )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    """接收訊息並調用 Gemini API 生成回應"""
    user_query = event.message.text
    user_id = event.source.user_id
    print(f"📩 收到來自 [{user_id}] 的問題：{user_query}")

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 1. 觸發 LINE 官方載入中動畫 (Loading Animation)，提升使用者等待體驗
        try:
            line_bot_api.show_loading_animation(
                ShowLoadingAnimationRequest(chat_id=user_id, loading_seconds=15)
            )
        except Exception as e:
            # 部分帳號或群組可能不支援 loading 動畫，容錯略過
            print(f"⚠️ Loading 動畫發送略過：{e}")

        # 2. 呼叫 Gemini 3.7 Flash Interactions API
        try:
            interaction = gemini_client.interactions.create(
                model="gemini-3.7-flash",
                input=user_query,
                system_instruction="你是一個繁體中文的 LINE 智慧生活與工作助理，請用親切、清晰、精準且格式整齊的繁體中文回覆。"
            )
            reply_text = interaction.output_text or "抱歉，AI 暫時無法生成回覆。"
        except Exception as e:
            print(f"❌ Gemini 調用錯誤：{e}")
            reply_text = f"抱歉，處理您的訊息時發生錯誤：{str(e)}"

        # 3. 回覆使用者訊息 (LINE 單次訊息長度上限為 5000 字元)
        if len(reply_text) > 4900:
            reply_text = reply_text[:4900] + "\n...(回答長度已截斷)"

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )


def main():
    print("🤖 LINE Gemini AI Bot 伺服器啟動中...")
    print("👉 請使用 ngrok http 8000 穿透並將 Webhook 網址設定於 LINE Developers")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
