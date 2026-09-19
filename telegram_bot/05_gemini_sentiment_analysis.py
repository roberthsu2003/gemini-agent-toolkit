"""
Telegram 基礎教學 05：Gemini 客服情緒分析核心 (Sentiment Analysis)
功能：
1. 使用 Gemini API 的結構化輸出 (JSON Mode)
2. 精準辨識客戶語意情緒（特別考量台灣在地口語與反諷語氣）
3. 輸出包含情緒類型、信心度、是否需要真人介入、理由與建議同理心回覆
"""

import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


# 定義回傳的資料結構模型
class SentimentReport(BaseModel):
    sentiment: str = Field(
        description="情緒類型：positive (正向滿意), neutral (中立詢問), negative (輕微不滿), urgent_angry (強烈憤怒/客訴)"
    )
    confidence_score: float = Field(
        description="判斷信心指數 (0.0 到 1.0)"
    )
    requires_human_agent: bool = Field(
        description="是否需要真人客服介入接手 (True / False)"
    )
    reasoning: str = Field(
        description="繁體中文判斷理由簡述"
    )
    suggested_reply: str = Field(
        description="適合同理客戶的繁體中文建議回覆內容"
    )


def analyze_customer_message(user_message: str) -> dict:
    """
    呼叫 Gemini 分析客戶訊息情緒並回傳結構化字典
    """
    system_instruction = """
    你是一位專業的 Telegram 線上客服情緒分析與應對助手。
    請分析客戶發送的訊息情緒，並特別注意台灣在地的口語語境與反諷語氣（例如：「真的是太棒了喔，等了一個月還沒寄出」屬於負面反諷）。

    情緒分類說明：
    - positive: 正向滿意、感謝、讚許
    - neutral: 一般性詢問、商品或訂單查詢
    - negative: 輕微不滿、物流延誤抱怨、疑惑不耐
    - urgent_angry: 強烈憤怒、要求退費、揚言投訴消保官或找主管

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
        print(f"❌ Gemini 分析失敗：{e}")
        return {
            "sentiment": "neutral",
            "confidence_score": 0.0,
            "requires_human_agent": False,
            "reasoning": f"分析過程發生例外狀況：{e}",
            "suggested_reply": "您好，已收到您的訊息，請稍候專人為您服務。"
        }


def main():
    if not GEMINI_API_KEY:
        print("❌ 請先在 .env 設定 GEMINI_API_KEY")
        return

    # 測試多組不同情緒的客戶留言
    test_messages = [
        "請問今天下單大概什麼時候會出貨呢？",
        "太棒了！昨天訂今天就收到了，包裝非常仔細，感謝你們！",
        "你們的系統是不是又壞掉了？購物車一直無法結帳，真的很浪費時間耶。",
        "真的是太扯了！商品寄錯還客服不理不睬，再不處理我就直接去消保官申訴並投訴媒體！"
    ]

    print("🧠 Gemini 客服訊息情緒分析測試：\n" + "=" * 60)
    for msg in test_messages:
        print(f"💬 客戶訊息：{msg}")
        result = analyze_customer_message(msg)
        print(f"📊 情緒判定：{result.get('sentiment')}")
        print(f"🎯 信心度：{result.get('confidence_score'):.2f}")
        print(f"🚨 真人介入：{'⚠️ 是 (需專人處理)' if result.get('requires_human_agent') else '否 (AI 可自理)'}")
        print(f"💡 判斷原因：{result.get('reasoning')}")
        print(f"💌 建議回覆：{result.get('suggested_reply')}")
        print("-" * 60)


if __name__ == "__main__":
    main()
