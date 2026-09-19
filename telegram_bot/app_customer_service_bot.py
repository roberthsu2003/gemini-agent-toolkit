"""
Telegram 實務應用：智慧客服情緒辨識與後台真人告警機器人 (Customer Service Bot)
核心技術：
1. 即時情緒分析：當使用者私聊進線時，呼叫 Gemini 進行情緒與客訴等級判斷
2. 同理心回應：根據情緒狀態生成適合的回覆安撫用戶
3. 雙向通報架構：
   - 使用者端：收到即時同理心回覆與處理進度告知
   - 後台管理群組：若判定為緊急/客訴 (requires_human_agent=True)，立即將警報與完整分析轉發至客服主管群組
"""

import json
import logging
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from telegram import Update
from telegram.constants import ChatAction, ChatType, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 後台客服/管理員群組 Chat ID (負整數)
TARGET_GROUP_ID = os.environ.get("TELEGRAM_GROUP_CHAT_ID", "-1001234567890")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)


class SentimentReport(BaseModel):
    sentiment: str = Field(description="positive, neutral, negative, urgent_angry")
    confidence_score: float = Field(description="0.0 到 1.0")
    requires_human_agent: bool = Field(description="是否需要真人客服介入")
    reasoning: str = Field(description="繁體中文判斷理由")
    suggested_reply: str = Field(description="繁體中文建議回覆")


def analyze_customer_message(user_message: str) -> dict:
    """呼叫 Gemini 進行客服情緒分析"""
    system_instruction = """
    你是一位專業的 Telegram 線上客服情緒分析與應對助手。
    請分析客戶發送的訊息情緒，特別注意台灣在地的口語語境與反諷語氣。

    情緒分類說明:
    - positive: 正向滿意、表揚
    - neutral: 一般詢問、訂單或產品查詢
    - negative: 輕微不滿、物流稍微延誤抱怨
    - urgent_angry: 強烈憤怒、要求退費、揚言投訴消保官或投訴媒體

    如果客戶表達強烈不滿、投訴消保官、威脅退費或情緒極度憤怒，請將 requires_human_agent 設為 true。
    請務必以繁體中文撰寫 reasoning 與 suggested_reply。
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=SentimentReport,
                temperature=0.1,
            ),
        )
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"Gemini API 分析失敗: {e}")
        return {
            "sentiment": "neutral",
            "confidence_score": 0.0,
            "requires_human_agent": False,
            "reasoning": f"分析過程例外：{e}",
            "suggested_reply": "您好，已收到您的訊息，客服人員將儘速為您服務。"
        }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """歡迎訊息"""
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            "👋 您好！歡迎使用線上智慧客服系統。\n\n"
            "請直接在此留言您的問題、訂單編號或回饋，我們的 AI 助理與線上專員將隨時為您服務！"
        )
    else:
        await update.message.reply_text("👋 線上客服監控機器人已在群組中就緒。")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶私聊訊息，分析情緒並決定是否轉發後台群組告警"""
    if not update.message or not update.message.text:
        return

    raw_text = update.message.text
    chat_type = update.effective_chat.type
    user = update.message.from_user

    # 僅對私聊進行客服分析，避免群組互相對話被重複解析
    if chat_type != ChatType.PRIVATE:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # 1. 執行 Gemini 情緒分析
    analysis = analyze_customer_message(raw_text)

    sentiment_emoji = {
        "positive": "😊 正向滿意",
        "neutral": "💬 一般中立",
        "negative": "⚠️ 輕微抱怨",
        "urgent_angry": "🚨 緊急客訴"
    }.get(analysis.get("sentiment"), "💬 一般中立")

    requires_human = analysis.get("requires_human_agent", False)
    reply_content = analysis.get("suggested_reply", "收到您的訊息，處理中。")

    # 2. 回覆前端客戶
    if requires_human:
        user_reply = (
            f"【{sentiment_emoji}｜專人優先進線處理中】\n\n"
            f"{reply_content}\n\n"
            f"（⚠️ 系統已發送高優先權通知給主管與專人客服，請稍候片刻）"
        )
    else:
        user_reply = reply_content

    await update.message.reply_text(user_reply, reply_to_message_id=update.message.message_id)

    # 3. 若有設定後台群組，發送通報到客服主管群組
    if TARGET_GROUP_ID and TARGET_GROUP_ID != "-1001234567890":
        user_name = f"{user.full_name} (@{user.username})" if user.username else user.full_name
        
        # 標題依是否需要真人介入區分警示度
        if requires_human:
            alert_header = "🚨 <b>【高優先權客訴告警｜需要真人介入】</b>"
        else:
            alert_header = "📋 <b>【客服進線通知】</b>"

        group_notification = (
            f"{alert_header}\n\n"
            f"👤 <b>客戶資訊：</b> {user_name} (ID: <code>{user.id}</code>)\n"
            f"💬 <b>客戶留言：</b>\n{raw_text}\n\n"
            f"📊 <b>情緒判定：</b> {sentiment_emoji} (信心度: {analysis.get('confidence_score', 0):.2f})\n"
            f"💡 <b>判斷理由：</b> {analysis.get('reasoning')}\n"
            f"💌 <b>AI 建議/已回覆：</b>\n{reply_content}"
        )

        try:
            await context.bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=group_notification,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"✅ 已成功將客服通報轉發至後台群組 {TARGET_GROUP_ID}")
        except Exception as e:
            logger.error(f"❌ 轉發後台群組失敗：{e}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在 .env 中設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("=" * 60)
    print("🚀 Telegram 智慧客服情緒分析與真人告警 Bot 運行中 (Polling 模式)...")
    print(f"📱 後台通報群組 ID: {TARGET_GROUP_ID}")
    print("=" * 60)
    app.run_polling()


if __name__ == "__main__":
    main()
