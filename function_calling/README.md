# 🛠️ 函式呼叫 (Function Calling & Tool Use)

透過 **函式呼叫 (Function Calling)**，您可以將自訂的 Python 函式、外部 API、資料庫操作或物聯網設備控制介面提供給 Gemini。模型能根據使用者的自然語言提問，**智慧判斷是否需要調用工具、提取精確參數並自動執行**，是打造自主 AI Agent 的核心支柱。

> 📖 **官方說明**：
> Google GenAI SDK 支援將 Python 函式直接傳入 `tools` 清單，SDK 會自動解析函式的 Docstring 與型別標註生成 JSON Schema，並支援平行工具調用（Parallel Function Calling）與 Google Search 聯網混合。
> 官方文件：[Function calling - Google AI for Developers](https://ai.google.dev/gemini-api/docs/function-calling)

---

## 📑 目錄導覽

1. [會議預約外部動作執行 (01_meeting_scheduler.py)](#1-會議預約外部動作執行-01_meeting_schedulerpy)
2. [即時天氣查詢工具整合 (02_weather_assistant.py)](#2-即時天氣查詢工具整合-02_weather_assistantpy)
3. [多工具平行呼叫 (03_parallel_function_calling.py)](#3-多工具平行呼叫-03_parallel_function_callingpy)
4. [聯網搜尋 + 自訂工具混合調用 (04_multi_tool_search_and_function.py)](#4-聯網搜尋--自訂工具混合調用-04_multi_tool_search_and_functionpy)
5. [課堂互動筆記本 (Jupyter Notebooks)](#5-課堂互動筆記本-jupyter-notebooks)

---

## 1. 會議預約外部動作執行 (`01_meeting_scheduler.py`)

定義外部 Python 函式並交由 Gemini 決定何時調用與提取參數：

- 核心程式檔案：[`01_meeting_scheduler.py`](./01_meeting_scheduler.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
from google import genai
from google.genai import types

client = genai.Client()

def schedule_meeting(topic: str, date: str, participants_count: int) -> dict:
    """在行事曆中預約新會議。"""
    return {"status": "success", "room": "101 會議室", "topic": topic}

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="請幫我預約下週三 2026-09-02 的『Q4 產品策略會議』，預計 8 人參加。",
    config=types.GenerateContentConfig(
        tools=[schedule_meeting],
    ),
)

print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我開發 Gradio 智慧控制台：
1. 定義航班查詢與冷氣控制函式。
2. 傳入 Gemini Function Calling，介面接收用戶指令並展示工具執行的總結回覆。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit AI 智慧管家：
1. 定義飯店查詢與電影票訂購函式。
2. 使用 st.chat_input 接收用戶需求，調用 Gemini 執行對應工具並以 Markdown 渲染。
```

**Telegram Bot 工具管家 Prompt：**
```text
請幫我將 Function Calling 整合至 Telegram 機器人：
1. 定義天氣查詢與提醒設定函式。
2. 接收用戶訊息自動調用函式並將結果回應用戶。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 POST /api/agent 端點：
1. 傳入即時加密貨幣價格查詢函式。
2. 呼叫 Gemini 執行函式並將回覆封裝為 JSON 回傳。
```
</details>

---

## 2. 即時天氣查詢工具整合 (`02_weather_assistant.py`)

- 核心程式檔案：[`02_weather_assistant.py`](./02_weather_assistant.py)

---

## 3. 多工具平行呼叫 (`03_parallel_function_calling.py`)

- 核心程式檔案：[`03_parallel_function_calling.py`](./03_parallel_function_calling.py)

---

## 4. 聯網搜尋 + 自訂工具混合調用 (`04_multi_tool_search_and_function.py`)

- 核心程式檔案：[`04_multi_tool_search_and_function.py`](./04_multi_tool_search_and_function.py)
- 實務進階應用：[`app_telegram_multi_tool_search_bot.py`](./app_telegram_multi_tool_search_bot.py)

---

## 📱 實務應用專案：Telegram AI 智慧特助與工具管家

將 Gemini 3.7 Flash 的 Function Calling 能力無縫整合至 Telegram 機器人，讓學生透過真實對話體驗工具調用的震撼效果：

| 應用檔案 | 核心亮點與工具支援 | 執行指令 |
|---|---|---|
| [`app_telegram_bot.py`](./app_telegram_bot.py) | **全能生活與差旅特助**：內建四大工具（即時天氣、外幣匯率計算、個人待辦清單持久化、會議預約登記）。支援**平行呼叫 (Parallel Function Calling)**，一句話同時觸發多工具！ | `python function_calling/app_telegram_bot.py` |
| [`app_telegram_multi_tool_search_bot.py`](./app_telegram_multi_tool_search_bot.py) | **聯網搜尋 + 自訂動作雙核心管家**：同時掛載 Google Search 即時聯網與本地訂位/記帳函式。模型自主決定先上網查資料、再調用本地函式完成操作！ | `python function_calling/app_telegram_multi_tool_search_bot.py` |
| [`app_gradio.py`](./app_gradio.py) | **Gradio 網頁智慧控制台**：視覺化展示 Function Calling 調用過程與結果。 | `python function_calling/app_gradio.py` |
| [`app_streamlit.py`](./app_streamlit.py) | **Streamlit AI 智慧管家儀表板**：提供互動式對話視窗與即時工具狀態指示。 | `streamlit run function_calling/app_streamlit.py` |
| [`app_fastapi.py`](./app_fastapi.py) | **FastAPI 工具 API 端點**：提供後端微服務呼叫介面。 | `python function_calling/app_fastapi.py` |

### 💡 學生最驚艷的測試範例（複製即可在 Telegram 測試）：
- **多任務平行調用**：
  > `我明天要帶 3 位客戶去東京洽公，幫我查東京現在天氣，換算 5 萬日圓大概是多少台幣，並幫我預約下週一下午 2 點 4 個人的出差檢討會，順便把『準備出差簡報』加入待辦清單！`
- **聯網查最新資料 + 本地動作執行**：
  > `請幫我上網查一下台北信義區目前評分最高的義大利餐廳，並幫我預訂今天晚上 19:00 兩位用餐！`

---

## 5. 課堂互動筆記本 (Jupyter Notebooks)

- [`basic_function_calling.ipynb`](./basic_function_calling.ipynb)：基礎函式呼叫教學筆記本
- [`multi_function_calling.ipynb`](./multi_function_calling.ipynb)：多函式自動路由筆記本
- [`parallel_function_calling.ipynb`](./parallel_function_calling.ipynb)：平行函式呼叫筆記本
- [`chat_function_history.ipynb`](./chat_function_history.ipynb)：對話歷史與函式呼叫整合筆記本

