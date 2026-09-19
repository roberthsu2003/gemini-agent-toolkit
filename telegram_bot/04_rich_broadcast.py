"""
Telegram 基礎教學 04：圖文排版與互動按鈕推播 (Rich Media Broadcast)
功能：
1. 發送圖片 (本地檔案或 URL 網址)
2. 搭配 HTML 格式說明的文字 (caption)
3. 加入底部行內按鈕 (InlineKeyboardMarkup / InlineKeyboardButton)
"""

import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 推播目標（個人、群組或頻道）
TARGET_CHAT_ID = os.environ.get("TELEGRAM_GROUP_CHAT_ID", "-1001234567890")


async def send_photo_broadcast(
    chat_id: str | int,
    photo_source: str,
    caption: str,
    keyboard: InlineKeyboardMarkup | None = None
):
    """
    發送帶有排版說明的圖片與按鈕推播
    :param photo_source: 圖片網址 (URL) 或 本地圖片檔案路徑
    :param caption: 說明文字 (上限 1024 字元，支援 HTML 標籤)
    :param keyboard: 訊息底部的按鈕 (選填)
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        # 判斷是本地檔案還是 URL
        if os.path.isfile(photo_source):
            with open(photo_source, "rb") as photo_file:
                msg = await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                )
        else:
            msg = await bot.send_photo(
                chat_id=chat_id,
                photo=photo_source,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
        print(f"✅ 成功發送圖文推播至 [{chat_id}] (Message ID: {msg.message_id})")
    except Exception as e:
        print(f"❌ 圖文推播至 [{chat_id}] 失敗：{e}")


async def main():
    if not TELEGRAM_TOKEN:
        print("❌ 請先在 .env 設定 TELEGRAM_BOT_TOKEN")
        return

    # 範例圖片網址 (Unsplash 高畫質相片)
    sample_photo = "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800"

    # HTML 排版文字說明
    caption = (
        "<b>🔥 2026 最新 AI Agent 實戰系列課程上線！</b>\n\n"
        "探索如何結合 <b>Google Gemini 3 世代模型</b> 與 <b>Telegram Bot</b>，"
        "打造具備自動推播、情緒分析與自動化運算的全功能智慧助理。\n\n"
        "📌 <i>包含：聯網搜尋、結構化輸出、多模態圖文理解等全方位實戰。</i>"
    )

    # 建立行內互動按鈕 (跳轉連結)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌐 前往 GitHub 專案庫", url="https://github.com/roberthsu2003"),
            InlineKeyboardButton("📖 閱讀官方文件", url="https://ai.google.dev/")
        ],
        [
            InlineKeyboardButton("💬 聯絡客服支援", url="https://t.me/BotFather")
        ]
    ])

    print("🚀 正在發送圖文推播...")
    await send_photo_broadcast(
        chat_id=TARGET_CHAT_ID,
        photo_source=sample_photo,
        caption=caption,
        keyboard=keyboard
    )


if __name__ == "__main__":
    asyncio.run(main())
