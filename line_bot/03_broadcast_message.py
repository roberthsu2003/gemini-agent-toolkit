"""
LINE 基礎教學 03：全方位主動推播訊息 (Push / Multicast / Broadcast)
使用 line-bot-sdk v3
功能：
1. Push Message：向指定單一使用者 (User ID) 推播
2. Multicast Message：向多名指定使用者群發 (最多 500 人)
3. Broadcast Message：向全體已加入好友的使用者全域廣播
"""

import os
from dotenv import load_dotenv
from linebot.v3.messaging import (
    ApiClient,
    BroadcastRequest,
    Configuration,
    MessagingApi,
    MulticastRequest,
    PushMessageRequest,
    TextMessage,
)

load_dotenv()

LINE_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

# ==============================================================================
# 推播目標設定
# ==============================================================================
# LINE User ID 格式為 U 開頭的 33 碼字串（例如：U1234567890abcdef1234567890abcdef）
# 可在 01_basic_bot.py 收到訊息時的終端機 log 查看 user_id
TARGET_USER_ID = os.environ.get("LINE_USER_ID", "U_REPLACE_WITH_YOUR_USER_ID")


def push_single_user(api: MessagingApi, user_id: str, text: str):
    """1. Push Message：主動發送給單一指定用戶"""
    try:
        response = api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=text)]
            )
        )
        print(f"✅ Push 單人推播成功至 [{user_id}]！")
    except Exception as e:
        print(f"❌ Push 單人推播失敗：{e}")


def multicast_users(api: MessagingApi, user_ids: list[str], text: str):
    """2. Multicast Message：主動群發給多名指定用戶清單 (上限 500 人)"""
    try:
        response = api.multicast(
            MulticastRequest(
                to=user_ids,
                messages=[TextMessage(text=text)]
            )
        )
        print(f"✅ Multicast 多人推播成功至 {len(user_ids)} 位用戶！")
    except Exception as e:
        print(f"❌ Multicast 多人推播失敗：{e}")


def broadcast_all(api: MessagingApi, text: str):
    """3. Broadcast Message：全體好友主動廣播（注意：會扣除官方帳號的免費訊息額度）"""
    try:
        response = api.broadcast(
            BroadcastRequest(
                messages=[TextMessage(text=text)]
            )
        )
        print("✅ Broadcast 全好友廣播成功！")
    except Exception as e:
        print(f"❌ Broadcast 全好友廣播失敗：{e}")


def main():
    if not LINE_TOKEN:
        print("❌ 請先在 .env 設定 LINE_CHANNEL_ACCESS_TOKEN！")
        return

    configuration = Configuration(access_token=LINE_TOKEN)

    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)

        print("🚀 LINE 主動推播展示中...")
        message_content = "📢 這是來自 LINE Bot 的主動推播測試通知！"

        # 示範 1：單人 Push（請確保已在 .env 設定有效的 LINE_USER_ID）
        if TARGET_USER_ID and not TARGET_USER_ID.startswith("U_REPLACE"):
            print(f"\n--- 1. 執行單人 Push 推播至 {TARGET_USER_ID} ---")
            push_single_user(api, TARGET_USER_ID, message_content)
        else:
            print("\n⚠️ 未設定 LINE_USER_ID，略過單人 Push 範例。")

        # 示範 2：多人 Multicast（解除註解並填入多位好友 User ID 即可測試）
        # sample_users = ["U111...", "U222..."]
        # multicast_users(api, sample_users, message_content)

        # 示範 3：全好友 Broadcast（解除註解即可發送給所有好友）
        # broadcast_all(api, "📢 全體好友廣播：今日最新優惠上線囉！")


if __name__ == "__main__":
    main()
