"""
app_telegram_bot.py
實務應用整合：Telegram 全能 AI 生活與差旅特助 (Function Calling & Tool Use)

採用 Google 最新 GenAI SDK (google-genai) 與 Gemini 3.7 Flash
支援多工具自動調用 (Automatic Function Calling) 與平行呼叫 (Parallel Function Calling)

內建實用工具：
1. get_city_weather: 即時氣象與出門穿著建議
2. convert_currency: 即時外幣匯率換算器 (TWD, JPY, USD, EUR, KRW 等)
3. manage_todo_list: 個人即時待辦清單管理器 (新增、查看、清除)
4. schedule_meeting: 行事曆會議預約與會議室分配
"""

import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 載入環境變數
load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 初始化最新版 Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# 本機儲存各使用者的待辦清單 (使用者 ID -> 待辦事項清單)
USER_TODOS: dict[int, list[str]] = {}

# 目前進行中的會議預約記錄
MEETING_RECORDS: list[dict] = []


# ==============================================================================
# 定義供 Gemini 呼叫的 Python 外部工具函式 (具備完整 Type Hints 與 Docstring)
# ==============================================================================

def get_city_weather(city: str) -> dict:
    """查詢指定城市的即時天氣氣候、氣溫與穿著/帶傘建議。

    Args:
        city: 城市名稱，例如 '台北', '台中', '高雄', '東京', '大阪', '首爾', '紐約', '倫敦'
    """
    print(f"⚡ [Tool 調用] get_city_weather(city='{city}')")
    
    # 模擬即時氣象資料庫
    weather_database = {
        "台北": {"temperature": 26.5, "condition": "多雲偶陣雨", "humidity": "78%", "clothing": "短袖加薄外套，出門請攜帶雨具"},
        "台中": {"temperature": 29.0, "condition": "晴朗", "humidity": "60%", "clothing": "透氣短袖，注意防曬"},
        "高雄": {"temperature": 31.0, "condition": "艷陽天", "humidity": "65%", "clothing": "清涼夏裝，多補充水分"},
        "東京": {"temperature": 19.5, "condition": "晴時多雲", "humidity": "50%", "clothing": "長袖襯衫配夾克，早晚偏涼"},
        "大阪": {"temperature": 21.0, "condition": "舒適微風", "humidity": "55%", "clothing": "薄長袖即可"},
        "首爾": {"temperature": 15.0, "condition": "陰天稍涼", "humidity": "45%", "clothing": "建議穿保暖外套或風衣"},
        "紐約": {"temperature": 17.5, "condition": "多雲", "humidity": "52%", "clothing": "秋裝連帽衫或風衣"},
    }
    
    for key, data in weather_database.items():
        if key in city:
            return {"status": "success", "city": city, **data}
            
    return {
        "status": "success",
        "city": city,
        "temperature": 24.0,
        "condition": "晴朗舒適",
        "humidity": "60%",
        "clothing": "舒適休閒便服"
    }


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """即時外幣匯率計算與金額換算。

    Args:
        amount: 要換算的原始金額數字
        from_currency: 來源貨幣代碼，例如 'TWD', 'JPY', 'USD', 'EUR', 'KRW', 'CNY'
        to_currency: 目標貨幣代碼，例如 'TWD', 'JPY', 'USD', 'EUR', 'KRW', 'CNY'
    """
    print(f"⚡ [Tool 調用] convert_currency(amount={amount}, from='{from_currency}', to='{to_currency}')")

    # 以 TWD 為基準的常見匯率表
    rates_to_twd = {
        "TWD": 1.0,
        "USD": 32.2,
        "JPY": 0.215,
        "EUR": 34.8,
        "KRW": 0.024,
        "CNY": 4.45,
        "GBP": 41.5,
    }

    f_curr = from_currency.upper().strip()
    t_curr = to_currency.upper().strip()

    if f_curr not in rates_to_twd or t_curr not in rates_to_twd:
        return {
            "status": "error",
            "message": f"不支援的貨幣轉換：{from_currency} -> {to_currency}，支援幣別包含 TWD, USD, JPY, EUR, KRW, CNY, GBP"
        }

    # 先換算為 TWD 再換算為目標貨幣
    amount_in_twd = amount * rates_to_twd[f_curr]
    result_amount = amount_in_twd / rates_to_twd[t_curr]
    exchange_rate = rates_to_twd[f_curr] / rates_to_twd[t_curr]

    return {
        "status": "success",
        "original_amount": amount,
        "from_currency": f_curr,
        "to_currency": t_curr,
        "converted_amount": round(result_amount, 2),
        "rate": round(exchange_rate, 4),
    }


def manage_todo_list(action: str, item_text: str = "") -> dict:
    """管理使用者的個人待辦清單 (Todo List)。

    Args:
        action: 操作動作，必須為 'add' (新增項目), 'list' (查看目前清單), 'clear' (清空所有項目)
        item_text: 待辦事項內容 (當 action 為 'add' 時必填)
    """
    print(f"⚡ [Tool 調用] manage_todo_list(action='{action}', item_text='{item_text}')")
    
    # 預設儲存於通用清單中
    todos = USER_TODOS.setdefault(0, [])

    if action == "add":
        if not item_text:
            return {"status": "error", "message": "新增項目時必須提供待辦內容"}
        todos.append(item_text)
        return {
            "status": "success",
            "action": "add",
            "added_item": item_text,
            "total_items": len(todos),
            "current_list": todos
        }
    elif action == "list":
        return {
            "status": "success",
            "action": "list",
            "total_items": len(todos),
            "current_list": todos if todos else "目前沒有任何待辦事項！"
        }
    elif action == "clear":
        todos.clear()
        return {"status": "success", "action": "clear", "message": "已清空所有待辦事項"}
    else:
        return {"status": "error", "message": f"未知的動作：{action}，僅支援 add, list, clear"}


def schedule_meeting(topic: str, date: str, time_slot: str, participants_count: int) -> dict:
    """預約內部會議或行事曆活動。

    Args:
        topic: 會議主題或活動名稱
        date: 會議日期 (格式例如 '2026-09-30' 或 '下週一')
        time_slot: 會議開始時段 (例如 '14:00' 或 '10:30')
        participants_count: 預計參與會議的人數
    """
    print(f"⚡ [Tool 調用] schedule_meeting(topic='{topic}', date='{date}', time='{time_slot}', count={participants_count})")

    room_name = "大會議廳 A" if participants_count > 10 else ("中會議室 B" if participants_count > 4 else "小型討論室 C")
    meeting_id = f"MTG-{len(MEETING_RECORDS) + 101}"

    record = {
        "meeting_id": meeting_id,
        "topic": topic,
        "date": date,
        "time_slot": time_slot,
        "participants_count": participants_count,
        "assigned_room": room_name,
        "status": "預約確認"
    }
    MEETING_RECORDS.append(record)

    return {"status": "success", **record}


# ==============================================================================
# Telegram Bot 事件處理邏輯
# ==============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """歡迎訊息與功能演示提示"""
    welcome_text = (
        "🤖 **歡迎使用 Gemini 3.7 全能智慧特助！**\n\n"
        "我內建了多項自動執行工具，你可以用**最自然的話**吩咐我：\n\n"
        "🌦️ **即時天氣**：\n"
        "• `台北今天會下雨嗎？出門要怎麼穿？`\n"
        "• `東京現在氣溫如何？`\n\n"
        "💱 **外幣匯率換算**：\n"
        "• `我想去日本玩，50000 日圓折合台幣大概多少錢？`\n"
        "• `1200 美元換成台幣是多少？`\n\n"
        "📝 **個人待辦清單**：\n"
        "• `幫我把『繳信用卡費』加入待辦清單`\n"
        "• `我目前有哪些待辦事項？`\n\n"
        "📅 **行事曆會議預約**：\n"
        "• `幫我預約下週三下午 2 點的 Q4 策略會議，大概 6 個人參加`\n\n"
        "🔥 **最殺手的『複合多任務』體驗 (Parallel Function Calling)**：\n"
        "• `我明天要去大阪出差，幫我查大阪天氣、換算 3 萬日圓是多少台幣，並幫我預約下週一下午 3 點 5 個人的出差心得分享會！`"
    )
    if update.message:
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶自然語言訊息並執行 Function Calling"""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    chat_id = update.effective_chat.id

    # 發送輸入中狀態
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # 系統指令指示
    system_instruction = (
        "你是一位高效率且親切的繁體中文 Telegram 智慧個人管家。"
        "你可以使用提供的 Python 工具來查詢天氣、計算匯率、管理待辦清單與預約會議。"
        "當使用者提出的請求包含多個任務時，你可以同時調用多個工具 (Parallel Function Calling)。"
        "完成工具調用後，請使用排版美觀的繁體中文條列統整，並適度加入 Emoji 給出專業、清楚的回覆。"
    )

    try:
        # 最新版 google-genai 呼叫方式：傳入 tools 清單，SDK 會自動執行函式並完成回傳
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[
                    get_city_weather,
                    convert_currency,
                    manage_todo_list,
                    schedule_meeting,
                ],
                temperature=0.2,
            ),
        )

        reply = response.text or "✅ 已成功為您調用相關工具處理完畢！"
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"❌ Function Calling 執行錯誤：{e}")
        await update.message.reply_text(f"抱歉，處理您的請求時發生錯誤：{e}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在專案根目錄 .env 中設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    # 建立 Telegram Application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("=" * 65)
    print("🚀 Telegram Function Calling 智慧特助已啟動 (Polling 模式)...")
    print("💡 支援工具：get_city_weather, convert_currency, manage_todo, schedule_meeting")
    print("=" * 65)

    app.run_polling()


if __name__ == "__main__":
    main()
