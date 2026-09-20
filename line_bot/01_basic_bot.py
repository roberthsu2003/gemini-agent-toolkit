"""
LINE 基礎教學 01：基礎連線與 Echo 文字回覆 (Basic Echo Bot)
使用 line-bot-sdk v3 與 FastAPI
功能：
1. 架設 Webhook 伺服器並驗證 LINE 數位簽章 (X-Line-Signature)
2. 處理 FollowEvent（加好友歡迎訊息）
3. 接收並回應用戶傳送的一般文字訊息 (Echo 鏡像回覆)
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    TextMessageContent,
)
import uvicorn

load_dotenv()

# 讀取 LINE 金鑰設定
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    print("❌ 請先在 .env 中設定 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN！")

# 初始化 LINE SDK 組件
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 建立 FastAPI 應用
app = FastAPI(title="LINE Basic Echo Bot")


@app.get("/")
def health_check():
    """健康檢查端點"""
    return {"status": "ok", "message": "LINE Bot Webhook 服務正常運作中！"}


@app.post("/callback")
async def callback(request: Request):
    """LINE Webhook 回呼端點"""
    # 取得 X-Line-Signature 標頭
    signature = request.headers.get("X-Line-Signature", "")

    # 取得請求主體文字
    body = await request.body()
    body_text = body.decode("utf-8")

    # 驗證數位簽章並將事件派發給 handler
    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        print("❌ 簽章驗證失敗 (Invalid Signature)，請檢查 CHANNEL_SECRET 是否正確。")
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"


# ==============================================================================
# 事件監聽器 (Event Handlers)
# ==============================================================================

@handler.add(FollowEvent)
def handle_follow(event: FollowEvent):
    """當使用者加入好友或解除封鎖時觸發"""
    user_id = event.source.user_id
    print(f"🎉 新好友加入！User ID: {user_id}")

    welcome_message = (
        "👋 你好！歡迎加入 LINE 機器人好友！\n\n"
        "這是一個使用 FastAPI 與 line-bot-sdk v3 打造的基礎範例。\n"
        "請隨意傳送文字訊息給我，我會原樣回覆你喔！"
    )

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=welcome_message)]
            )
        )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    """接收使用者傳送的文字訊息並進行 Echo 鏡像回覆"""
    user_text = event.message.text
    user_id = event.source.user_id
    print(f"📩 收到來自 [{user_id}] 的訊息：{user_text}")

    reply_text = f"你說了：{user_text}"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )


def main():
    print("🤖 LINE Echo Bot 伺服器啟動中...")
    print("👉 請使用 ngrok http 8000 穿透並將 Webhook 網址設定於 LINE Developers")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
