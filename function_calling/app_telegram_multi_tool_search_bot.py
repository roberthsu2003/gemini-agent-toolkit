"""
app_telegram_multi_tool_search_bot.py
實務進階應用：Telegram 聯網搜尋 + 自訂動作混合調用 AI 智慧管家 (Grounding + Tool Use)

採用 Google 最新 GenAI SDK (google-genai) 與 Gemini 3.7 Flash
核心突破：同時掛載 Google Search 聯網搜尋工具 與 本地 Python 自訂工具！
模型會自主判斷：
1. 何時該上網 Google 搜尋最新即時世界資訊
2. 何時該執行本地 Python 動作 (例如預訂席位、記錄記帳日誌、發送通知)
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# 儲存預訂成功的紀錄清單
RESERVATIONS: list[dict] = []


# ==============================================================================
# 本地自訂 Python 工具函式
# ==============================================================================

def book_dining_reservation(restaurant_name: str, party_size: int, time_slot: str, special_requests: str = "") -> dict:
    """完成餐廳預約訂位並產生確認單。

    Args:
        restaurant_name: 欲預訂的餐廳名稱
        party_size: 用餐人數
        time_slot: 預訂用餐時間 (例如 '18:30' 或 '12:00')
        special_requests: 特殊用餐需求 (如靠窗、包廂、素食等)
    """
    print(f"\n⚡ [本地 Tool 執行] book_dining_reservation(restaurant='{restaurant_name}', size={party_size}, time='{time_slot}', requests='{special_requests}')")

    booking_id = f"BK-{len(RESERVATIONS) + 8801}"
    record = {
        "booking_id": booking_id,
        "restaurant_name": restaurant_name,
        "party_size": party_size,
        "time_slot": time_slot,
        "special_requests": special_requests or "無特殊備註",
        "status": "訂位已確認"
    }
    RESERVATIONS.append(record)

    return {
        "status": "success",
        "message": f"成功預約 {restaurant_name}！",
        **record
    }


def record_expense_entry(category: str, amount_twd: float, description: str) -> dict:
    """將消費支出記錄至個人出差記帳本。

    Args:
        category: 支出類別 (例如 '餐飲', '交通', '住宿', '購物', '娛樂')
        amount_twd: 新台幣金額
        description: 支出詳細描述
    """
    print(f"\n⚡ [本地 Tool 執行] record_expense_entry(category='{category}', amount={amount_twd}, desc='{description}')")
    return {
        "status": "success",
        "category": category,
        "amount_twd": amount_twd,
        "description": description,
        "note": "已寫入記帳資料庫"
    }


# ==============================================================================
# Telegram 訊息處理
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "🌐 **歡迎使用 Gemini 聯網搜尋 + 自訂工具雙核心智慧管家！**\n\n"
        "我具備 **Google 即時聯網搜尋** 與 **本地 Python 動作執行** 雙重超能力，你可以這樣吩咐我：\n\n"
        "🍽️ **搜尋並預訂餐廳**：\n"
        "• `請幫我聯網查一下台北信義區目前評價最高的一家牛排餐廳，並幫我預約今晚 19:00 兩位靠窗座位！`\n\n"
        "💰 **即時查價與記帳**：\n"
        "• `請上網查詢今天日本環球影城門票大概多少台幣？順便幫我記錄一筆『娛樂』類別的門票預算記帳。`\n\n"
        "✨ *模型會自主決定先上 Google 查資料，再自動調用本地函式完成操作！*"
    )
    if update.message:
        await update.message.reply_text(welcome_msg, parse_mode=ParseMode.MARKDOWN)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_query = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    system_prompt = (
        "你是一位繁體中文的 Telegram 智慧差旅與生活助理。"
        "你擁有兩種工具："
        "1. Google 搜尋工具 (google_search)：用於查詢即時資訊、最新餐廳評價、景點價格等外部知識。"
        "2. 本地自訂 Python 工具 (book_dining_reservation 與 record_expense_entry)：用於預訂餐廳或記帳。"
        "請根據使用者的需求自主規劃工具調用順序，整合結果後用熱情、條理分明的繁體中文回答。"
    )

    try:
        # 同時傳入自訂函式與 Google 搜尋工具
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[
                    book_dining_reservation,
                    record_expense_entry,
                    types.Tool(google_search=types.GoogleSearch()),
                ],
                temperature=0.3,
            ),
        )

        reply_text = response.text or "處理完成！"
        await update.message.reply_text(reply_text)

    except Exception as e:
        print(f"❌ 混合工具執行失敗：{e}")
        await update.message.reply_text(f"執行時發生例外：{e}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在專案根目錄 .env 中設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("=" * 65)
    print("🚀 Gemini 聯網搜尋 + 自訂工具雙核心 Telegram Bot 運行中...")
    print("=" * 65)
    app.run_polling()


if __name__ == "__main__":
    main()
