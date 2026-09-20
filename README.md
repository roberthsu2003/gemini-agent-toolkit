# 🤖 Gemini AI Agent 開發工具箱與實戰

一套專為 Python 開發者與學生打造的 **Google Gemini API** 與 **自主 AI Agent** 完整實戰教學庫。全面涵蓋 Google 最新的 Gemini 3 世代模型、官方推薦的 Interactions API，以及從純 Python 基礎到 Telegram、Gradio、Streamlit 與 FastAPI 的企業級實務整合。

---

> 🚀 **專案版本特色（2026 最新規範）**：
> - **最新架構**：全面採用 Google 官方推薦的 **Interactions API** (`client.interactions.create`) 與最新 [`google-genai`](https://github.com/googleapis/python-genai) SDK。
> - **頂尖模型**：全面支援 **Gemini 3** 最新模型（`gemini-3.7-flash`、`gemini-3.5-flash-lite`、`gemini-3.1-pro-preview` 等）。
> - **雙層學習**：劃分「核心功能教學（純 Python）」與「實務整合應用（Web/Bot/API）」，循序漸進。
> - **AI 賦能**：每單元均附帶 **AI 賦能提示詞 (Prompts)**，方便一鍵利用 AI 生成視覺化 Web 介面。

---

## 📑 快速目錄導覽

- [⚡ 3 步驟快速開始](#-3-步驟快速開始-quick-start)
- [🧭 核心課程學習地圖（全章節導覽表）](#-核心課程學習地圖全章節導覽表)
- [📱 焦點實務專題：Telegram Bot 機器人開發](#-焦點實務專題telegram-bot-機器人開發)
- [🤖 2026 推薦模型指南](#-2026-推薦模型指南)
- [📚 五大階段詳細章節內容](#-五大階段詳細章節內容)
  - [第一階段：基礎互動與多模態體驗](#-第一階段基礎互動與多模態體驗建立成就感)
  - [第二階段：工程化與資料約束](#️-第二階段工程化與資料約束應用開發必備)
  - [第三階段：外掛能力與工具整合](#️-第三階段外掛能力與工具整合突破-llm-限制)
  - [第四階段：企業級記憶與 RAG 檢索](#-第四階段企業級記憶與-rag-檢索海量資料庫)
  - [第五階段：綜合架構與生態拓展](#-第五階段綜合架構與生態拓展融會貫通)
- [📦 專案內建素材清單 (Assets)](#-專案內建素材清單-assets)

---

## ⚡ 3 步驟快速開始 (Quick Start)

### 步驟 1：安裝環境與套件
本專案支援 Python 3.9+，推薦使用極速套件管理器 `uv` 或傳統 `pip`：

```bash
# 使用 uv (推薦)
uv add google-genai pydantic python-dotenv gradio streamlit requests beautifulsoup4 openpyxl python-telegram-bot

# 或使用 pip
pip install google-genai pydantic python-dotenv gradio streamlit requests beautifulsoup4 openpyxl python-telegram-bot
```

### 步驟 2：設定 API Key
在專案根目錄建立 `.env` 檔案，填入您的金鑰：
```env
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here   # 若要運行 Telegram Bot 請填寫
```

### 步驟 3：執行第一個範例 (Interactions API)
```python
from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請用繁體中文以三點簡要說明什麼是 AI Agent？"
)

print(interaction.output_text)
```

<details>
<summary>💡 <b>思考推理模式示範 (Thinking with Gemini 3)</b></summary>

Gemini 3 具備原生思考推理能力，可透過 `thinking_level`（`minimal` / `low` / `medium` / `high`）自由調節思考深度：

```python
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請分析量子運算對現行 RSA 加密演算法帶來的具體衝擊。",
    generation_config={
        "thinking_level": "medium",
        "temperature": 1.0  # 思考模式下建議維持預設 1.0
    }
)
print(interaction.output_text)
```
</details>

---

## 🧭 核心課程學習地圖（全章節導覽表）

為方便學生快速檢索，全專案 10 大核心章節依照學習曲線整理如下表：

| 階段 | 單元名稱 | 核心教學 (純 Python) | 實務整合應用 | 互動筆記本 |
|---|---|---|---|---|
| **一、基礎互動** | [**1. 文字生成**](./text_generation/README.md) | 文字生成、思考模式、系統提示詞、圖文多模態、串流、狀態化對話 | Telegram Bot、Gradio、Streamlit、FastAPI | [`text_generation_quickstart.ipynb`](./text_generation/text_generation_quickstart.ipynb) |
| | [**2. 圖像生成**](./image_generation/README.md) | Imagen 3 生圖、比例控制、Gemini 生圖、Prompt 智慧擴寫 | Telegram 算圖 Bot、Gradio 畫廊、Streamlit 生圖室、FastAPI | — |
| | [**3. 文件理解**](./document_understanding/README.md) | Inline 摘要、Files API、URL 研讀、多文件比對、Context Caching | Telegram PDF 助理、Gradio 研讀、Streamlit 知識庫、FastAPI | [`pdf_understanding_tutorial.ipynb`](./document_understanding/pdf_understanding_tutorial.ipynb) |
| **二、資料約束** | [**4. 結構化輸出**](./structure_output/README.md) | Pydantic 基礎、Union 多態與 Enum、匯率文字轉結構化數據 | Telegram 結構化提取、Gradio 表格轉化、Streamlit CSV 下載、FastAPI | [`exchange_rate_extraction.ipynb`](./structure_output/exchange_rate_extraction.ipynb) |
| **三、外掛整合** | [**5. 聯網搜尋**](./ground_search/README.md) | Google Search Grounding 基礎聯網、來源解析、聯網+程式碼運算 | Telegram 查證 Bot、Gradio 查核、Streamlit 時事情報、FastAPI | — |
| | [**6. 程式碼執行**](./code_execution/README.md) | 安全沙盒運算、CSV 數據處理、Matplotlib 動態繪圖、局部裁切 | Telegram 運算 Bot、Gradio 沙盒、Streamlit 演算儀表板、FastAPI | [`math_and_code_execution.ipynb`](./code_execution/math_and_code_execution.ipynb) |
| | [**7. 函式呼叫**](./function_calling/README.md) | 會議預約 4 步驟、即時天氣、多工具平行呼叫、聯網+自訂工具混合 | Telegram 生活差旅特助、Telegram 聯網雙核心管家、Gradio、Streamlit | [`basic_function_calling.ipynb`](./function_calling/basic_function_calling.ipynb) |
| **四、企業級檢索**| [**8. 向量檢索**](./embeddings/document_search/README.md) | 語意相似度、非對稱文件檢索、Matryoshka 維度縮減、開源 E5 | Telegram 知識庫 Bot、Gradio 相似度、Streamlit 語意搜尋、FastAPI | [`gemini_embedding_tutorial.ipynb`](./embeddings/document_search/gemini_embedding_tutorial.ipynb) |
| **五、架構拓展** | [**9. 何謂 AI Agent**](./何謂AIAgent/README.md) | Agent 核心觀念、工作流模式 (Chaining / Routing / Orchestrator) | 核心手冊與模式詳解 | — |
| | [**10. 開源模型**](./開源模型/README.md) | Hugging Face Serverless API、Mistral-Nemo 模型調用與摘要 | 文字摘要實作 (`text_to_summarization.py`) | [`test.ipynb`](./開源模型/test.ipynb) |

---

## 💬 焦點實務專題：LINE Bot 機器人開發

LINE 是台灣、日本與東南亞普及率最高、商業應用最廣泛的通訊管道（支援 Webhook 事件驅動、Flex Message 現代化卡片、Loading 思考動畫與全方位主動推播）。

👉 **完整教學與手冊請點擊參閱專屬章節**：[**【💬 LINE Bot 連線方式與機器人開發實戰】**](./line_bot/README.md)

### 🔹 基礎教學篇（打穩核心元件觀念）
- [`01_basic_bot.py`](./line_bot/01_basic_bot.py)：**基礎架構與 Echo**（FastAPI Webhook 機制、簽章驗證、加好友歡迎事件、文字鏡像回覆）
- [`02_gemini_bot.py`](./line_bot/02_gemini_bot.py)：**Gemini 3.7 AI 私聊**（Interactions API 整合、Loading 動畫狀態提示、繁中流暢回答）
- [`03_broadcast_message.py`](./line_bot/03_broadcast_message.py)：**全方位主動推播**（向指定 User ID Push、向多名用戶 Multicast、向全體好友 Broadcast）
- [`04_rich_broadcast.py`](./line_bot/04_rich_broadcast.py)：**圖文與 Flex Message 卡片推播**（發送圖片、ButtonsTemplate 按鈕範本與高質感 Flex Message 氣泡卡片）
- [`05_gemini_sentiment_analysis.py`](./line_bot/05_gemini_sentiment_analysis.py)：**Gemini 客服情緒分析核心**（純 Python 呼叫結構化 JSON 輸出，辨識 4 種情緒與真人接手標記）

---

## 📱 焦點實務專題：Telegram Bot 機器人開發

Telegram 是串接大語言模型與 AI Agent 最輕量、好寫且開發體驗極佳的通訊管道（免 Webhook/伺服器、支援本機 Polling 輪詢快速測試、30 秒極速申請 Token）。

👉 **完整教學與手冊請點擊參閱專屬章節**：[**【📱 Telegram Bot 連線方式與機器人開發實戰】**](./telegram_bot/README.md)

### 🔹 基礎教學篇（打穩核心元件觀念）
- [`01_basic_bot.py`](./telegram_bot/01_basic_bot.py)：**基礎架構與 Echo**（Polling 輪詢、`/start` 指令、文字鏡像回覆）
- [`02_gemini_bot.py`](./telegram_bot/02_gemini_bot.py)：**Gemini 3.7 AI 私聊**（Interactions API 整合、輸入中動畫狀態）
- [`03_broadcast_message.py`](./telegram_bot/03_broadcast_message.py)：**全方位主動推播**（向個人、群組與公開/私密頻道發送訊息）
- [`04_rich_broadcast.py`](./telegram_bot/04_rich_broadcast.py)：**圖文與按鈕推播**（照片 + HTML 排版 Caption + InlineKeyboard 互動按鈕）
- [`05_gemini_sentiment_analysis.py`](./telegram_bot/05_gemini_sentiment_analysis.py)：**Gemini 客服情緒分析核心**（純 Python 呼叫結構化 JSON 輸出）

### 🔹 實務應用篇（組合基礎積木）
- [`app_gemini_group_bot.py`](./telegram_bot/app_gemini_group_bot.py)：**群組 AI 助理**（支援 @提及 與回覆觸發防洗版機制、私聊直接回答）
- [`app_news_broadcast_bot.py`](./telegram_bot/app_news_broadcast_bot.py)：**聯網焦點新聞推播**（Google Search 搜尋最新科技焦點並自動推播）
- [`app_customer_service_bot.py`](./telegram_bot/app_customer_service_bot.py)：**智慧客服與真人告警**（即時同理心回覆，緊急客訴自動轉發主管群組）
- [`app_sentiment_excel_logger.py`](./telegram_bot/app_sentiment_excel_logger.py)：**客服日誌每日 Excel 報表**（整合 `openpyxl` 自動寫入每日美化報表）
- [`systemd/`](./telegram_bot/systemd/README.md)：**Linux / 樹莓派定時排程部署**（開機自啟、每小時/每日定時推播服務腳本）

---

## 🤖 2026 推薦模型指南

| 用途 | 推薦模型 | 特性與說明 |
|---|---|---|
| **通用主力（預設首選）** | `gemini-3.7-flash` | 1M tokens 上下文，平衡速度、多模態、思考推理與 Agentic 任務。 |
| **低成本 / 高吞吐** | `gemini-3.5-flash-lite` | 最經濟、極速回應，適合高頻次輕量任務與資料萃取。 |
| **深度推理 / 複雜編程** | `gemini-3.1-pro-preview` | 1M tokens 上下文，頂級程式碼生成、數學邏輯與深度研究。 |
| **文字向量嵌入** | `gemini-embedding-001` | 支援 `task_type` 與可自訂維度 (`output_dimensionality`)。 |
| **多模態向量嵌入** | `gemini-embedding-2` | 支援文字、圖片、影片與音訊的多模態統一嵌入。 |

> ⚠️ **已淘汰提示**：舊版 `gemini-2.0-*`、`gemini-1.5-*` 全系列及舊版 `google-generativeai` 套件已停用，請全面採用上述最新規範。

---

## 📚 五大階段詳細章節內容

---

### 🔰 第一階段：基礎互動與多模態體驗（建立成就感）

#### [1. 文字生成 (text_generation)](./text_generation/README.md)
劃分「核心功能教學（純 Python）」與「實務整合實戰（Telegram / Gradio / Streamlit / FastAPI）」雙層架構：
- 📌 **核心教學**：[`01_basic_text.py`](./text_generation/01_basic_text.py)（文字生成）｜[`02_thinking_mode.py`](./text_generation/02_thinking_mode.py)（思考深度）｜[`03_system_and_params.py`](./text_generation/03_system_and_params.py)（系統指示詞）｜[`04_multimodal_image.py`](./text_generation/04_multimodal_image.py)（多模態圖文）｜[`05_streaming.py`](./text_generation/05_streaming.py)（即時串流）｜[`06_stateful_chat.py`](./text_generation/06_stateful_chat.py)（狀態化對話）｜[`07_stateless_chat.py`](./text_generation/07_stateless_chat.py)（無狀態對話）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./text_generation/app_telegram_bot.py)（Telegram Bot）｜[`app_gradio.py`](./text_generation/app_gradio.py)（Gradio Web UI）｜[`app_streamlit.py`](./text_generation/app_streamlit.py)（Streamlit 儀表板）｜[`app_fastapi.py`](./text_generation/app_fastapi.py)（FastAPI 後端與 SSE）
- 📓 **互動筆記**：[`text_generation_quickstart.ipynb`](./text_generation/text_generation_quickstart.ipynb)｜[`trip_planner_system_instruction.ipynb`](./text_generation/trip_planner_system_instruction.ipynb)

#### [2. 圖像生成 (image_generation)](./image_generation/README.md)
使用 Google Imagen 3 (`imagen-3.0-generate-002`) 與 `gemini-2.5-flash-image` 進行 Text-to-Image 生成與 Prompt 擴寫工作流：
- 📌 **核心教學**：[`01_text_to_image.py`](./image_generation/01_text_to_image.py)（基礎生圖）｜[`02_aspect_ratio.py`](./image_generation/02_aspect_ratio.py)（比例控制）｜[`03_gemini_flash_image.py`](./image_generation/03_gemini_flash_image.py)（Gemini 生圖）｜[`04_prompt_enhancer.py`](./image_generation/04_prompt_enhancer.py)（Prompt 智慧擴寫）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./image_generation/app_telegram_bot.py)（Telegram 算圖 Bot）｜[`app_gradio.py`](./image_generation/app_gradio.py)（Gradio 畫廊）｜[`app_streamlit.py`](./image_generation/app_streamlit.py)（Streamlit 生圖室）｜[`app_fastapi.py`](./image_generation/app_fastapi.py)（FastAPI API）

#### [3. 文件理解 (document_understanding)](./document_understanding/README.md)
原生多模態 PDF 視覺理解（支援達 1000 頁 / 50MB），涵蓋 Inline、Files API、跨文件比對與 Context Caching 快取：
- 📌 **核心教學**：[`01_inline_pdf_summary.py`](./document_understanding/01_inline_pdf_summary.py)（Inline 摘要）｜[`02_files_api_pdf_chat.py`](./document_understanding/02_files_api_pdf_chat.py)（Files API 問答）｜[`03_remote_pdf_analysis.py`](./document_understanding/03_remote_pdf_analysis.py)（URL 下載研讀）｜[`04_multi_pdf_comparison.py`](./document_understanding/04_multi_pdf_comparison.py)（跨文件比對）｜[`05_pdf_structured_extraction.py`](./document_understanding/05_pdf_structured_extraction.py)（Pydantic 萃取）｜[`06_pdf_context_caching.py`](./document_understanding/06_pdf_context_caching.py)（Context Caching 快取）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./document_understanding/app_telegram_bot.py)（Telegram PDF 助理）｜[`app_gradio.py`](./document_understanding/app_gradio.py)（Gradio 工作台）｜[`app_streamlit.py`](./document_understanding/app_streamlit.py)（Streamlit 知識庫）｜[`app_fastapi.py`](./document_understanding/app_fastapi.py)（FastAPI 端點）
- 📓 **互動筆記**：[`pdf_understanding_tutorial.ipynb`](./document_understanding/pdf_understanding_tutorial.ipynb)｜[`csv_document_caching.ipynb`](./document_understanding/csv_document_caching.ipynb)

---

### ⚙️ 第二階段：工程化與資料約束（應用開發必備）

#### [4. 結構化輸出 (structure_output)](./structure_output/README.md)
強制約束模型輸出嚴格符合 JSON Schema 或 Pydantic 模型，涵蓋條件多態 (`Union`)、遞迴樹狀結構與列舉：
- 📌 **核心教學**：[`01_pydantic_basic.py`](./structure_output/01_pydantic_basic.py)（Pydantic 基礎）｜[`02_advanced_schemas.py`](./structure_output/02_advanced_schemas.py)（遞迴樹狀與 Enum）｜[`03_currency_exchange.py`](./structure_output/03_currency_exchange.py)（匯率文字轉數據）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./structure_output/app_telegram_bot.py)（Telegram 結構化提取）｜[`app_gradio.py`](./structure_output/app_gradio.py)（Gradio 表格轉換器）｜[`app_streamlit.py`](./structure_output/app_streamlit.py)（Streamlit CSV 下載）｜[`app_fastapi.py`](./structure_output/app_fastapi.py)（FastAPI 強型別 API）
- 📓 **互動筆記**：[`lesson1.ipynb`](./structure_output/lesson1.ipynb)｜[`exchange_rate_extraction.ipynb`](./structure_output/exchange_rate_extraction.ipynb)｜[`exchange_rate_to_csv.ipynb`](./structure_output/exchange_rate_to_csv.ipynb)

---

### 🛠️ 第三階段：外掛能力與工具整合（突破 LLM 限制）

#### [5. 聯網搜尋 (ground_search)](./ground_search/README.md)
啟用 Google Search Grounding 讓模型自主聯網搜尋最新即時資訊，自動標註來源網址：
- 📌 **核心教學**：[`01_basic_search.py`](./ground_search/01_basic_search.py)（基礎聯網）｜[`02_search_citations.py`](./ground_search/02_search_citations.py)（引用來源解析）｜[`03_search_with_code_execution.py`](./ground_search/03_search_with_code_execution.py)（聯網 + Python 運算）｜[`04_search_structured_output.py`](./ground_search/04_search_structured_output.py)（聯網 + 結構化輸出）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./ground_search/app_telegram_bot.py)（Telegram 查證 Bot）｜[`app_gradio.py`](./ground_search/app_gradio.py)（Gradio 查核）｜[`app_streamlit.py`](./ground_search/app_streamlit.py)（Streamlit 時事情報）｜[`app_fastapi.py`](./ground_search/app_fastapi.py)（FastAPI 端點）

#### [6. 程式碼執行 (code_execution)](./code_execution/README.md)
模型自主在 Google 託管的 Python 安全沙盒中編寫並執行程式碼，徹底避免算術幻覺：
- 📌 **核心教學**：[`01_math_solver.py`](./code_execution/01_math_solver.py)（數學運算求解）｜[`02_currency_calculator.py`](./code_execution/02_currency_calculator.py)（CSV 匯率運算）｜[`03_matplotlib_plotter.py`](./code_execution/03_matplotlib_plotter.py)（動態繪圖）｜[`04_image_zoom_inspection.py`](./code_execution/04_image_zoom_inspection.py)（局部裁切檢驗）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./code_execution/app_telegram_bot.py)（Telegram 運算 Bot）｜[`app_gradio.py`](./code_execution/app_gradio.py)（Gradio 沙盒工作台）｜[`app_streamlit.py`](./code_execution/app_streamlit.py)（Streamlit 演算儀表板）｜[`app_fastapi.py`](./code_execution/app_fastapi.py)（FastAPI 沙盒 API）
- 📓 **互動筆記**：[`math_and_code_execution.ipynb`](./code_execution/math_and_code_execution.ipynb)｜[`currency_calculator.ipynb`](./code_execution/currency_calculator.ipynb)

#### [7. 函式呼叫 (function_calling)](./function_calling/README.md)
讓模型連接外部 API 與工具，自動識別意圖、提取參數並執行動作：
- 📌 **核心教學**：[`01_meeting_scheduler.py`](./function_calling/01_meeting_scheduler.py)（會議預約 4 步驟）｜[`02_weather_assistant.py`](./function_calling/02_weather_assistant.py)（即時天氣查詢）｜[`03_parallel_function_calling.py`](./function_calling/03_parallel_function_calling.py)（多工具平行呼叫）｜[`04_multi_tool_search_and_function.py`](./function_calling/04_multi_tool_search_and_function.py)（聯網 + 自訂工具混合）
- 🚀 **實務整合**：
  - [`app_telegram_bot.py`](./function_calling/app_telegram_bot.py)：**Telegram 全能特助**（即時天氣、匯率試算、個人待辦清單、會議預約）
  - [`app_telegram_multi_tool_search_bot.py`](./function_calling/app_telegram_multi_tool_search_bot.py)：**Telegram 雙核心管家**（Google Search 聯網 + 本地訂位與記帳函式）
  - [`app_gradio.py`](./function_calling/app_gradio.py)（Gradio 智慧控制台）｜[`app_streamlit.py`](./function_calling/app_streamlit.py)（Streamlit 管家儀表板）｜[`app_fastapi.py`](./function_calling/app_fastapi.py)（FastAPI 工具 API）
- 📓 **互動筆記**：[`basic_function_calling.ipynb`](./function_calling/basic_function_calling.ipynb)｜[`multi_function_calling.ipynb`](./function_calling/multi_function_calling.ipynb)｜[`parallel_function_calling.ipynb`](./function_calling/parallel_function_calling.ipynb)｜[`chat_function_history.ipynb`](./function_calling/chat_function_history.ipynb)

---

### 🧠 第四階段：企業級記憶與 RAG 檢索（海量資料庫）

#### [8. 向量檢索 (embeddings)](./embeddings/document_search/README.md)
將文字內容轉為語意向量，支援 `gemini-embedding-001`、Matryoshka (MRL) 維度縮減與非對稱檢索：
- 📌 **核心教學**：[`01_gemini_semantic_similarity.py`](./embeddings/document_search/01_gemini_semantic_similarity.py)（語意相似度）｜[`02_gemini_document_retrieval.py`](./embeddings/document_search/02_gemini_document_retrieval.py)（非對稱檢索）｜[`03_dimension_reduction.py`](./embeddings/document_search/03_dimension_reduction.py)（Matryoshka 維度縮減）｜[`04_document_search_e5.py`](./embeddings/document_search/04_document_search_e5.py)（開源 E5 模型）
- 🚀 **實務整合**：[`app_telegram_bot.py`](./embeddings/document_search/app_telegram_bot.py)（Telegram 知識庫 Bot）｜[`app_gradio.py`](./embeddings/document_search/app_gradio.py)（Gradio 相似度工作台）｜[`app_streamlit.py`](./embeddings/document_search/app_streamlit.py)（Streamlit 語意搜尋）｜[`app_fastapi.py`](./embeddings/document_search/app_fastapi.py)（FastAPI 向量 API）
- 📓 **互動筆記**：[`gemini_embedding_tutorial.ipynb`](./embeddings/document_search/gemini_embedding_tutorial.ipynb)｜[`csv_semantic_search.ipynb`](./embeddings/document_search/csv_semantic_search.ipynb)

---

### 🚀 第五階段：綜合架構與生態拓展（融會貫通）

#### [9. 何謂 AI Agent (何謂AIAgent)](./何謂AIAgent/README.md)
代理觀念與工作流設計模式，探討 LLM 工作流與自主代理人的本質區別：
- 涵蓋模式：Prompt chaining、Routing、Parallelization、Orchestrator-workers、Evaluator-optimizer
- 📖 **核心手冊**：[`README.md`](./何謂AIAgent/README.md)

#### [10. 開源模型 (開源模型)](./開源模型/README.md)
整合 Hugging Face Serverless Inference API，調用開源大語言模型（如 Mistral-Nemo-Instruct）進行文字生成與摘要任務：
- 📌 **程式碼**：[`text_to_summarization.py`](./開源模型/text_to_summarization.py)（Hugging Face 文字摘要實作）
- 📓 **互動筆記**：[`test.ipynb`](./開源模型/test.ipynb)（開源模型調用筆記本）

---

## 📦 專案內建素材清單 (Assets)

本專案已包含所有教學範例所需的完整素材檔案，學生 Clone 專案後**無需自行尋找或下載任何素材**即可直接練習：

- 📄 **PDF 文件**：[`說明書.pdf`](./document_understanding/說明書.pdf)（冷氣壁掛式說明書，4MB，用於長文件問答與快取）
- 📊 **表格資料**：
  - [`2025_01_29.csv`](./structure_output/2025_01_29.csv)（臺灣銀行牌告匯率表格）
  - [`aqx_p_488.csv`](./document_understanding/aqx_p_488.csv)（空氣品質監測資料，134KB）
  - [`001.csv`](./embeddings/document_search/001.csv)（知識庫說明文件，用於語意檢索）
- 🖼️ **圖片素材**：
  - [`organ.jpg`](./structure_output/organ.jpg)（管風琴樂器相片，用於多模態分析）
  - [`bear.jpg`](./text_generation/bear.jpg)（棕熊相片，用於圖文問答）
  - [`plant1.jpg`](./text_generation/plant1.jpg) ~ [`plant3.webp`](./text_generation/plant3.webp)（植物相片）
- 📑 **評測與向量檔**：
  - [`Embeddings模型評測.xlsx`](./embeddings/document_search/Embeddings模型評測.xlsx)（繁體中文 Embedding 效果評測表）
  - [`embeddings.pkl`](./embeddings/document_search/pretrain_and_query/embeddings.pkl)（預先計算之向量庫檔案）

---

## 📖 專案結構細節

詳細目錄樹結構與各檔案詳細介紹請參閱 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。
