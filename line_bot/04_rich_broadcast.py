"""
LINE 基礎教學 04：圖文排版與 Flex Message 卡片推播 (Rich Media & Flex Message)
使用 line-bot-sdk v3
功能：
1. 發送圖片訊息 (ImageMessage - 需提供 HTTPS 原始圖與縮圖 URL)
2. 發送現代化 Flex Message 氣泡卡片 (自訂配色、標籤、商品/通知卡片與互動按鈕)
"""

import json
import os
from dotenv import load_dotenv
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    FlexContainer,
    FlexMessage,
    ImageMessage,
    MessagingApi,
    PushMessageRequest,
)

load_dotenv()

LINE_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
TARGET_USER_ID = os.environ.get("LINE_USER_ID", "U_REPLACE_WITH_YOUR_USER_ID")


def send_image(api: MessagingApi, user_id: str, image_url: str):
    """發送圖片訊息（LINE 要求必須為公開 HTTPS 且支援 TLS 1.2+ 的直連圖片）"""
    try:
        api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[
                    ImageMessage(
                        original_content_url=image_url,
                        preview_image_url=image_url
                    )
                ]
            )
        )
        print("✅ 圖片訊息推播成功！")
    except Exception as e:
        print(f"❌ 圖片推播失敗：{e}")


def send_flex_card(api: MessagingApi, user_id: str):
    """
    發送高質感 Flex Message 氣泡卡片
    此範例為「Gemini 智慧科技快報卡片」
    """
    # 定義 Flex Bubble JSON 結構
    flex_json = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://ai.google.dev/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Gemini 3.7 Flash",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1DB446"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "最新混合推理與 Agentic 模型已整合至 LINE 機器人！",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "查看官方文件",
                        "uri": "https://ai.google.dev/gemini-api/docs"
                    },
                    "color": "#06C755"
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "開啟 GitHub 專案",
                        "uri": "https://github.com"
                    }
                }
            ],
            "flex": 0
        }
    }

    try:
        # 將 JSON 字典轉化為 FlexContainer
        flex_container = FlexContainer.from_json(json.dumps(flex_json))
        api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[
                    FlexMessage(
                        alt_text="✨ Gemini 智慧科技快報來囉！",
                        contents=flex_container
                    )
                ]
            )
        )
        print("✅ Flex Message 卡片推播成功！")
    except Exception as e:
        print(f"❌ Flex Message 卡片推播失敗：{e}")


def main():
    if not LINE_TOKEN:
        print("❌ 請先在 .env 設定 LINE_CHANNEL_ACCESS_TOKEN！")
        return

    if not TARGET_USER_ID or TARGET_USER_ID.startswith("U_REPLACE"):
        print("❌ 請先在 .env 設定有效的 LINE_USER_ID 以便接收推播！")
        return

    configuration = Configuration(access_token=LINE_TOKEN)

    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)

        print(f"🚀 開始向 [{TARGET_USER_ID}] 發送圖文與 Flex Message 卡片...")

        # 1. 發送高質感 Flex Message 氣泡卡片
        send_flex_card(api, TARGET_USER_ID)

        # 2. 發送一般圖片（可自由開啟測試）
        # sample_img = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800"
        # send_image(api, TARGET_USER_ID, sample_img)


if __name__ == "__main__":
    main()
