# 💬 LINE Bot 連線方式與機器人開發實戰

LINE 是台灣、日本與東南亞普及率最高、商業應用最廣泛的通訊管道。不論是企業官方帳號 (Official Account)、個人品牌、電商售後、會員通知或 AI 智慧管家，LINE 都是不可或缺的接觸點。

- ⚡ **現代化 SDK 架構**：採用官方最新 `line-bot-sdk` v3，支援模組化 API 客戶端與型別安全。
- 🌐 **事件驅動 (Event-Driven)**：採用 Webhook 機制接收即時事件（加好友、傳送訊息、點擊選單），搭配非同步高速框架 **FastAPI** 與 **Uvicorn**。
- 🔗 **極速本機測試**：搭配 **ngrok** 穿牆工具，30 秒內即可將本地開發伺服器對外暴露為 HTTPS 網址，無需部屬伺服器即可直接真機測試！
- 🤖 **最新 AI 整合**：完整串接 Google Gemini 3.7 Flash 最新 Interactions API 與結構化輸出。

本章節分為**「基礎教學篇」**（打穩核心 Webhook、事件處理、推播與多模態卡片觀念）與**「實務應用說明」**，協助學生循序漸進打造出具商業價值的 LINE AI 機器人。

---

## 🔑 快速申請 LINE Bot（Messaging API）

### 步驟 1：登入 LINE Developers Console
1. 前往 **[LINE Developers Console](https://developers.line.biz/console/)**。
2. 使用個人的 LINE 帳號登入。

### 步驟 2：建立 Provider（提供者）與 Channel（頻道）
1. 點擊 **Create a new provider**，輸入提供者名稱（例如：`Gemini-Agent-Dev`）。
2. 在 Provider 頁面內，點擊 **Create a Messaging API channel**。
3. 填寫頻道基本資料：
   - **Channel name**：機器人名稱（如 `Gemini 智慧管家`）。
   - **Channel description**：簡短介紹。
   - **Category / Subcategory**：選擇合適的分類。
   - 勾選同意服務條款後點擊 **Create**。

### 步驟 3：取得金鑰並設定權限
1. **取得 Channel Secret**：
   - 在 **Basic settings** 分頁中，找到 **Channel secret** 並複製。
2. **取得 Channel Access Token**：
   - 切換至 **Messaging API** 分頁。
   - 滑動至最下方 **Channel access token (long-lived)**，點擊 **Issue** 產生長效 Token 並複製。
3. **關閉官方自動回應（避免與 AI 衝突）**：
   - 在 **Messaging API** 分頁中，找到 **LINE Official Account features**。
   - 點擊 **Auto-reply messages** 旁邊的 **Edit**（會跳轉至 LINE Official Account Manager）。
   - 將 **自動回應訊息 (Auto-response)** 設為 **「停用」**。
   - 將 **Webhook** 設為 **「開啟」**。

### 步驟 4：配置專案環境變數 (`.env`)
將取得的金鑰填入專案根目錄的 `.env` 檔案中：
```env
LINE_CHANNEL_SECRET=your_line_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
GEMINI_API_KEY=your_gemini_api_key_here

# （選填）推播目標 User ID（可在好友加入或傳送訊息時於後台 log 取得，格式為 U 開頭的 33 碼字串）
LINE_USER_ID=U1234567890abcdef1234567890abcdef
```

---

## 🛠️ 安裝必要套件

```bash
# 透過 pip 安裝
pip install line-bot-sdk fastapi uvicorn python-dotenv google-genai pydantic

# 或在 uv 虛擬環境中安裝
uv pip install line-bot-sdk fastapi uvicorn python-dotenv google-genai pydantic
```

---

## 🌐 本地開發穿牆神器：ngrok 設定

LINE 官方伺服器需要透過 **HTTPS** 的 Webhook URL 將訊息推送給您的伺服器。在本地開發階段，我們使用免費的 **ngrok** 來建立安全隧道：

1. 前往 **[ngrok 官網](https://ngrok.com/)** 免費註冊並下載安裝（macOS 可直接執行 `brew install ngrok`）。
2. 開啟終端機啟動本地 FastAPI 伺服器（預設 port 8000）：
   ```bash
   python line_bot/01_basic_bot.py
   # 或使用 uvicorn 指令
   uvicorn line_bot.01_basic_bot:app --host 0.0.0.0 --port 8000 --reload
   ```
3. 開啟另一個終端機視窗，啟動 ngrok 轉發 8000 連接埠：
   ```bash
   ngrok http 8000
   ```
4. ngrok 會產生專屬的 Forwarding 網址（例如：`https://abc1-23-45-67-89.ngrok-free.app`）。
5. 回到 **LINE Developers Console** -> **Messaging API** 分頁：
   - 在 **Webhook URL** 欄位填入：`https://abc1-23-45-67-89.ngrok-free.app/callback`
   - 點擊 **Update** 儲存。
   - 點擊 **Verify** 測試連線（顯示 `Success` 代表驗證成功）。
   - 將 **Use webhook** 開關切換為 **開啟 (Enabled)**。

現在拿起手機掃描 Messaging API 分頁中的 QR Code 加入好友，即可開始測試！

---

## 📚 第一階段：基礎教學篇（核心元件與操作）

每個基礎範例專注於單一核心觀念，使用官方推薦的 `line-bot-sdk` v3，代碼架構乾淨、註解詳盡：

| 檔案 | 核心技術與說明 | 執行方式 |
|---|---|---|
| [`01_basic_bot.py`](./01_basic_bot.py) | **基礎架構與 Echo**：認識 FastAPI Webhook 機制、簽章驗證（`WebhookHandler`）、加好友歡迎事件（`FollowEvent`）與文字鏡像回覆。 | `python line_bot/01_basic_bot.py` |
| [`02_gemini_bot.py`](./02_gemini_bot.py) | **Gemini 3.7 AI 私聊**：串接最新 Interactions API、顯示 LINE 載入中動畫（Loading Animation `ShowLoadingAnimationRequest`）、繁中流暢對答。 | `python line_bot/02_gemini_bot.py` |
| [`03_broadcast_message.py`](./03_broadcast_message.py) | **全方位主動推播**：利用 Messaging API 主動推送訊息，涵蓋 Push（指定單人）、Multicast（指定多人群發）、Broadcast（全好友廣播）。 | `python line_bot/03_broadcast_message.py` |
| [`04_rich_broadcast.py`](./04_rich_broadcast.py) | **圖文與 Flex Message 卡片推播**：發送高品質圖片、按鈕範本訊息（`ButtonsTemplate`）與高質感 Flex Message 現代化氣泡卡片。 | `python line_bot/04_rich_broadcast.py` |
| [`05_gemini_sentiment_analysis.py`](./05_gemini_sentiment_analysis.py) | **Gemini 客服情緒分析核心**：純 Python 呼叫 Gemini 結構化輸出（JSON Mode / Pydantic），識別 4 種情緒等級、信心分數與是否需真人客服介入。 | `python line_bot/05_gemini_sentiment_analysis.py` |

---

## 🚀 第二階段：實務應用延伸指引

有了基礎篇的 5 大核心積木後，您可以進一步擴展出完整的商業級 LINE AI 助理應用：

1. **LINE 社群 / 多人群組 AI 助理**：
   - 監聽 `JoinEvent`（加入群組）與 `MemberJoinedEvent`。
   - 設計「防洗版判斷」：在群組中只在使用者發送特定前綴指令（如 `/ai`）或提及時才呼叫 Gemini 回覆。
2. **LINE 智慧客服與緊急客訴真人轉接**：
   - 結合 `05_gemini_sentiment_analysis.py` 的情緒分析能力。
   - 若客戶情緒強烈不滿（`requires_human_agent = True`），自動調用 `03_broadcast_message.py` 發送 Push 訊息通知管理員 LINE 或轉發內部 Slack/Telegram 告警。
3. **Flex Message 互動型報表與選單 (Rich Menu)**：
   - 結合 LINE Flex Message Simulator 自由設計外觀如訂單確認單、飯店預約確認、每日科技新聞卡片等。
4. **雲端伺服器 7x24 常駐部屬**：
   - 在雲端主機（GCP Cloud Run / AWS EC2 / Render）使用 Docker 或 systemd 常駐執行 FastAPI 服務，並配置正式網域 SSL 憑證。
