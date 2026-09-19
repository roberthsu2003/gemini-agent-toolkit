# 📱 Telegram Bot 連線方式與機器人開發實戰

Telegram 是串接大語言模型與 AI Agent 最輕量、好寫且開發體驗極佳的通訊管道：
- ⚡ **免伺服器與 Webhook 設定**：開發階段使用內建的 **Polling（輪詢）** 機制即可直接在本地電腦運行，不需要公開 IP 或 ngrok 穿牆。
- ⏱️ **申請流程極快**：在 Telegram 搜尋 `@BotFather`，發送 `/newbot` 指令，30 秒內即可取得 API Token。
- 📦 **生態系成熟**：採用官方主流 `python-telegram-bot`（支援完整非同步 `async`/`await`）與最新 `google-genai` SDK。

本章節分為**「基礎教學篇」**（打穩各元件基礎觀念）與**「實務應用篇」**（依據基礎積木組合出商業級專案），協助學生從零循序漸進掌握完整的機器人開發技能。

---

## 🔑 快速申請 Telegram Bot Token

1. 在 Telegram 搜尋官方機器人管理員 **[@BotFather](https://t.me/BotFather)**。
2. 發送 `/start`，接著點擊或輸入 `/newbot`。
3. 依序輸入機器人的 **顯示名稱 (Name)** 與 **唯一帳號 (Username)**（需以 `bot` 結尾，例如 `my_gemini_agent_bot`）。
4. 建立完成後，BotFather 會回傳專屬的 **HTTP API Token**（格式如 `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`）。
5. 將 Token 儲存於專案根目錄 `.env` 檔案中：
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # （選填）推播目標 Chat ID
   TELEGRAM_USER_CHAT_ID=123456789
   TELEGRAM_GROUP_CHAT_ID=-1001234567890
   TELEGRAM_CHANNEL_CHAT_ID=@your_channel_username
   ```

---

## 🛠️ 安裝必要套件

```bash
uv add python-telegram-bot python-dotenv google-genai openpyxl pydantic
# 或使用 pip
pip install python-telegram-bot python-dotenv google-genai openpyxl pydantic
```

---

## 📚 第一階段：基礎教學篇（核心元件與操作）

每個基礎範例專注於單一核心觀念，代碼精簡，便於初學者理解機器人生命週期：

| 檔案 | 核心技術與說明 | 執行方式 |
|---|---|---|
| [`01_basic_bot.py`](./01_basic_bot.py) | **基礎架構與 Echo**：認識 Polling 輪詢、`/start` 指令處理與用戶文字原樣鏡像回傳。 | `python telegram_bot/01_basic_bot.py` |
| [`02_gemini_bot.py`](./02_gemini_bot.py) | **AI 私聊助理**：串接 Gemini 3.7 Flash Interactions API，加入輸入中狀態（`ChatAction.TYPING`）。 | `python telegram_bot/02_gemini_bot.py` |
| [`03_broadcast_message.py`](./03_broadcast_message.py) | **全方位主動推播**：利用 `Bot.send_message` 主動推送通知到個人、群組與公開/私密頻道。 | `python telegram_bot/03_broadcast_message.py` |
| [`04_rich_broadcast.py`](./04_rich_broadcast.py) | **圖文卡片與按鈕**：發送圖片（本地或網址）+ HTML 格式說明 (`caption`) + 行內互動跳轉按鈕 (`InlineKeyboardMarkup`)。 | `python telegram_bot/04_rich_broadcast.py` |
| [`05_gemini_sentiment_analysis.py`](./05_gemini_sentiment_analysis.py) | **Gemini 客服情緒分析核心**：純 Python 呼叫 Gemini 結構化輸出（JSON Mode / Pydantic），識別 4 種情緒與真人介入標記。 | `python telegram_bot/05_gemini_sentiment_analysis.py` |

---

## 🚀 第二階段：實務應用篇（組合基礎積木）

以基礎篇的模組為基石，擴展為解決真實商業情境的完整應用系統：

| 應用專案 | 核心技術與說明 | 完整原始碼連結 |
|---|---|---|
| **群組智慧 AI 助理** | 群組 @提及 / 回覆觸發防洗版機制、私聊直接對話。 | [`app_gemini_group_bot.py`](./app_gemini_group_bot.py) |
| **聯網焦點新聞自動推播** | Google Search 聯網搜尋、HTML/按鈕美化推播、定時排程。 | [`app_news_broadcast_bot.py`](./app_news_broadcast_bot.py) |
| **智慧客服情緒與告警** | 私聊情緒即時判讀、同理心安撫、緊急客訴自動轉發主管群組。 | [`app_customer_service_bot.py`](./app_customer_service_bot.py) |
| **客服日誌每日 Excel 報表** | 整合 openpyxl、每日對話與情緒指標自動寫入美化報表。 | [`app_sentiment_excel_logger.py`](./app_sentiment_excel_logger.py) |

---

### 1. 群組智慧 AI 助理（[`app_gemini_group_bot.py`](./app_gemini_group_bot.py)）
- 📄 **程式碼檔案**：👉 [`app_gemini_group_bot.py`](./app_gemini_group_bot.py)
- **應用場景**：社群/工作群組智慧秘書。
- **實務關鍵**：
  - 群組防洗版過濾：在群組中僅在被 `@BotUsername` 提及或回覆訊息時才觸發 AI 回覆。
  - 私聊情境無縫相容：私聊直接發問立即回答。
- **執行指令**：
  ```bash
  python telegram_bot/app_gemini_group_bot.py
  ```

---

### 2. Gemini 聯網焦點新聞自動推播機器人（[`app_news_broadcast_bot.py`](./app_news_broadcast_bot.py)）
- 📄 **程式碼檔案**：👉 [`app_news_broadcast_bot.py`](./app_news_broadcast_bot.py)
- **應用場景**：自動化時事情報發布台、品牌官方頻道晨報推播。
- **實務關鍵**：
  - **Google Search Grounding**：調用即時聯網工具自主搜尋當日重大焦點新聞與摘要。
  - **自動排程服務 (Linux / 樹莓派)**：可搭配專屬 [`systemd/`](./systemd/README.md) 設定檔，實現開機自啟、每小時/每日自動推播與失敗自動重試。
- **執行指令**：
  ```bash
  python telegram_bot/app_news_broadcast_bot.py
  ```

---

### 3. 智慧客服情緒辨識與後台真人告警系統（[`app_customer_service_bot.py`](./app_customer_service_bot.py)）
- 📄 **程式碼檔案**：👉 [`app_customer_service_bot.py`](./app_customer_service_bot.py)
- **應用場景**：電商、線上服務平台自動化接待與客訴預警。
- **運作架構**：
  ```mermaid
  sequenceDiagram
      actor C as 客戶 (私聊)
      participant B as Telegram Bot
      participant G as Gemini 3.7 Flash
      actor A as 後台客服主管 (管理群組)

      C->>B: 發送詢問或抱怨訊息
      B->>G: 執行語意與情緒分析 (JSON)
      G-->>B: 回傳情緒等級、判斷理由與建議回覆
      B->>C: 即時發送同理心安撫回覆
      opt 判定為緊急客訴 (requires_human_agent = True)
          B->>A: 🚨 即時轉發完整客戶資訊、客訴等級與分析報告至管理群組
      end
  ```
- **執行指令**：
  ```bash
  python telegram_bot/app_customer_service_bot.py
  ```

---

### 4. 客服通話日誌與每日 Excel 報表自動匯出（[`app_sentiment_excel_logger.py`](./app_sentiment_excel_logger.py)）
- 📄 **程式碼檔案**：👉 [`app_sentiment_excel_logger.py`](./app_sentiment_excel_logger.py)
- **應用場景**：客戶關係管理 (CRM)、客服團隊服務品質考核與客訴回溯。
- **實務關鍵**：
  - 整合 `openpyxl`，每日自動建立/累加 `chat_logs/YYYY-MM-DD.xlsx`。
  - 具備商業報表級自動美化：深藍表頭填色、微軟正黑體、自適應欄寬與自動文字換行。
  - 記錄時間、用戶 ID、用戶姓名、原始對話、情緒類型、信心值、真人標記與 AI 理由。
- **執行指令**：
  ```bash
  python telegram_bot/app_sentiment_excel_logger.py
  ```

---

## ⏱️ 系統級常駐與定時排程部署 (systemd)

若需要將推播機器人部署於 Linux 雲端主機（如 GCP / AWS）或樹莓派 (Raspberry Pi)：
詳細的開機自啟服務 `.service`、計時器 `.timer` 與一鍵管理腳本請參閱：
👉 [**Linux / 樹莓派 systemd 定時服務部署手冊**](./systemd/README.md)
