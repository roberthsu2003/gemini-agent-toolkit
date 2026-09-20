"""
LINE 基礎教學 05：Gemini 客服情緒分析核心 (Sentiment Analysis)
使用 Google GenAI SDK (Structured Outputs / Pydantic)
功能：
1. 使用 Gemini API 的結構化輸出 (JSON Mode)
2. 精準辨識 LINE 客戶語意情緒（特別考量台灣在地口語與反諷語氣）
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
    你是一位專業的 LINE 官方帳號線上客服情緒分析與應對助手。
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
                temperature=0.2,
            )
        )

        return json.loads(response.text)
    except Exception as e:
        print(f"❌ 分析發生錯誤：{e}")
        return {
            "sentiment": "neutral",
            "confidence_score": 0.0,
            "requires_human_agent": False,
            "reasoning": f"分析失敗：{e}",
            "suggested_reply": "非常抱歉，系統暫時無法處理，稍後將由客服專員為您服務。"
        }


def main():
    if not GEMINI_API_KEY:
        print("❌ 請先在 .env 設定 GEMINI_API_KEY！")
        return

    # 模擬 3 種不同情境的 LINE 用戶傳來的話
    test_cases = [
        "請問你們的營業時間到幾點？假日有配送嗎？",
        "你們的包裹昨天就收到了，包裝很仔細，出貨速度超快，謝謝你們！",
        "我上週三就下單了，客服問了三天都只會回機器人罐頭訊息，再不回覆我直接找消保官！"
    ]

    print("🤖 Gemini LINE 客服情緒分析核心測試\n" + "=" * 50)

    for i, text in enumerate(test_cases, 1):
        print(f"\n【案例 {i}】顧客訊息：\n「{text}」")
        result = analyze_customer_message(text)
        print("📊 分析結果：")
        print(f"  • 情緒類別: {result.get('sentiment')}")
        print(f"  • 信心度:   {result.get('confidence_score')}")
        print(f"  • 真人介入: {'🚨 是 (需轉接主管/專員)' if result.get('requires_human_agent') else '🟢 否 (AI 可自處理)'}")
        print(f"  • 判斷理由: {result.get('reasoning')}")
        print(f"  • 建議回覆:\n    「{result.get('suggested_reply')}」")


if __name__ == "__main__":
    main()
