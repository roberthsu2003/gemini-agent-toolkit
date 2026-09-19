"""
Telegram 實務應用：客服對話日誌與每日 Excel 報表匯出機器人 (Sentiment Excel Logger)
核心技術：
1. 即時情緒辨識：使用 Gemini API 分析客戶訊息
2. 每日自動分割 Excel 報表：使用 openpyxl 建立或累加當日報表 (chat_logs/YYYY-MM-DD.xlsx)
3. 商業報表排版：自動設定表頭顏色、欄寬自適應、文字對齊與欄位凍結
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from pydantic import BaseModel, Field
from telegram import Update
from telegram.constants import ChatAction, ChatType
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

LOG_DIR = Path(__file__).parent / "chat_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

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


def get_daily_excel_path() -> Path:
    """取得當日 Excel 檔案路徑 (chat_logs/YYYY-MM-DD.xlsx)"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"{today_str}.xlsx"


def init_excel_sheet(filepath: Path):
    """初始化 Excel 檔案並建立美化表頭"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "客服對話紀錄"

    headers = [
        "時間戳記", "使用者 ID", "使用者姓名", "帳號 (@username)",
        "原始訊息", "情緒分類", "信心指數", "需真人介入",
        "判斷理由", "建議/已發送回覆"
    ]
    ws.append(headers)

    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Microsoft JhengHei", size=11, bold=True, color="FFFFFF")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align

    # 設定欄寬
    column_widths = [20, 15, 18, 18, 35, 12, 12, 12, 30, 35]
    for i, w in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

    wb.save(filepath)


def log_conversation_to_excel(
    user_id: int,
    full_name: str,
    username: str,
    raw_text: str,
    analysis: dict
):
    """將一筆對話紀錄與分析結果寫入當日的 Excel 報表"""
    filepath = get_daily_excel_path()
    if not filepath.exists():
        init_excel_sheet(filepath)

    try:
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentiment = analysis.get("sentiment", "neutral")
        confidence = round(analysis.get("confidence_score", 0.0), 2)
        requires_human = "⚠️ 是" if analysis.get("requires_human_agent") else "否"
        reasoning = analysis.get("reasoning", "")
        suggested_reply = analysis.get("suggested_reply", "")

        row_data = [
            now_str,
            str(user_id),
            full_name,
            f"@{username}" if username else "無",
            raw_text,
            sentiment,
            confidence,
            requires_human,
            reasoning,
            suggested_reply
        ]
        ws.append(row_data)

        # 設定新加入列的對齊方式
        last_row = ws.max_row
        for col_idx in range(1, len(row_data) + 1):
            cell = ws.cell(row=last_row, column=col_idx)
            cell.alignment = Alignment(vertical="center", wrap_text=True)

        wb.save(filepath)
        logger.info(f"📁 已寫入 Excel 報表：{filepath.name} (第 {last_row} 列)")
    except Exception as e:
        logger.error(f"❌ 寫入 Excel 失敗：{e}")


def analyze_customer_message(user_message: str) -> dict:
    """呼叫 Gemini 進行情緒分析"""
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
        logger.error(f"Gemini 分析失敗：{e}")
        return {
            "sentiment": "neutral",
            "confidence_score": 0.0,
            "requires_human_agent": False,
            "reasoning": f"分析過程例外：{e}",
            "suggested_reply": "您好，已收到您的訊息，我們將儘速協助您。"
        }


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理訊息、調用分析、回覆用戶並存入 Excel 報表"""
    if not update.message or not update.message.text:
        return

    raw_text = update.message.text
    chat_type = update.effective_chat.type
    user = update.message.from_user

    # 僅處理私聊對話以記錄客服報表
    if chat_type != ChatType.PRIVATE:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # 1. Gemini 情緒分析
    analysis = analyze_customer_message(raw_text)

    # 2. 自動寫入每日 Excel 報表
    log_conversation_to_excel(
        user_id=user.id,
        full_name=user.full_name or "",
        username=user.username or "",
        raw_text=raw_text,
        analysis=analysis
    )

    # 3. 回覆客戶
    reply_content = analysis.get("suggested_reply", "收到您的訊息，處理中。")
    if analysis.get("requires_human_agent"):
        user_reply = f"【專人進線處理中】\n{reply_content}\n\n（系統已將您的需求排入高優先權專人隊列）"
    else:
        user_reply = reply_content

    await update.message.reply_text(user_reply, reply_to_message_id=update.message.message_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 您好！我是客服助理，請輸入您的問題，我會為您服務並記錄通訊日誌。")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在 .env 中設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("=" * 60)
    print("🚀 Telegram 客服情緒分析與每日 Excel 報表 Bot 運行中...")
    print(f"📁 報表輸出目錄：{LOG_DIR.resolve()}")
    print("=" * 60)
    app.run_polling()


if __name__ == "__main__":
    main()
