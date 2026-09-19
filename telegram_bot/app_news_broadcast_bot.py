"""
Telegram 實務應用：Gemini 聯網即時新聞自動推播機器人 (News Broadcast Bot)
核心技術：
1. Google Search Grounding：啟用 Google 官方即時聯網搜尋
2. 整合 Telegram 主動推播：將整理後的新聞摘要推播到指定群組或頻道
3. 支援單次手動推播，或透過 asyncio / systemd 定時排程定時執行
"""

import asyncio
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 推播目標（頻道或群組 ID）
TARGET_CHAT_ID = os.environ.get("TELEGRAM_GROUP_CHAT_ID", "-1001234567890")

client = genai.Client(api_key=GEMINI_API_KEY)


def fetch_latest_news(topic: str = "最新國際與台灣科技重大焦點新聞") -> str:
    """
    呼叫 Gemini 透過 Google 搜尋取得最新焦點新聞並整理摘要
    """
    prompt = f"請搜尋並整理今天『{topic}』三則最新要聞，每則包含【標題】、簡要說明（50~80字）與新聞發生時間，請使用繁體中文。"

    system_instruction = (
        "你是一位即時新聞播報編輯，請將新聞整理為清晰好讀的格式，"
        "可以使用 HTML 粗體 <b>標題</b> 與條列呈現。"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.3,
            ),
        )
        return response.text or "目前未能擷取到最新新聞資訊。"
    except Exception as e:
        print(f"❌ 聯網搜尋失敗：{e}")
        return f"無法獲取即時新聞：{e}"


async def broadcast_news(chat_id: str | int, news_content: str):
    """將新聞內容推播至 Telegram 目標"""
    bot = Bot(token=TELEGRAM_TOKEN)

    header = "📰 <b>【Gemini AI 即時科技焦點快訊】</b>\n"
    footer = "\n\n<i>⚡ 由 Gemini 3.7 Flash + Google Search Grounding 即時聯網生成</i>"
    full_message = header + "\n" + news_content + footer

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 瀏覽更多科技新聞", url="https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtdHZHZ0pMVWlnQVAB?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant")
        ]
    ])

    try:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=full_message,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
            disable_web_page_preview=False
        )
        print(f"✅ 成功推播即時新聞至 [{chat_id}] (Message ID: {msg.message_id})")
    except Exception as e:
        print(f"❌ 推播失敗：{e}")


async def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在 .env 設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    print("🌐 正在使用 Gemini 聯網搜尋最新焦點新聞...")
    news_summary = fetch_latest_news()

    print("\n--- 整理後之新聞內容 ---")
    print(news_summary)
    print("------------------------\n")

    print(f"📢 正在推播至目標 Chat ID: {TARGET_CHAT_ID}...")
    await broadcast_news(TARGET_CHAT_ID, news_summary)


if __name__ == "__main__":
    asyncio.run(main())
