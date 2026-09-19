# ⏱️ Linux / 樹莓派 (Raspberry Pi) 系統級定時排程服務

本目錄提供透過 Linux 原生 **systemd timer** 實現定時自動執行 [`app_news_broadcast_bot.py`](../app_news_broadcast_bot.py) 的設定檔。

相比於傳統 `crontab` 或在 Python 裡面寫 `while True: sleep(3600)`，使用 systemd 有以下優勢：
- 🛡️ **開機自動啟動**：主機重開機後無需手動重啟。
- 🔄 **失敗自動防護**：單次推播結束即釋放記憶體，不會因 Python 長時間常駐而發生記憶體洩漏 (OOM)。
- 📜 **統一標準日誌**：使用 `journalctl` 統一管理日誌輸出與錯誤追蹤。
- ⏰ **補償機制 (Persistent=true)**：若關機期間錯過排程時間，開機後會自動補發。

---

## 📁 檔案清單

| 檔案 | 說明 |
|---|---|
| `gemini-news-bot.service` | 定義執行的 Python 指令、虛擬環境路徑與工作目錄 |
| `gemini-news-bot.timer` | 設定排程頻率（如每小時一次，或每日固定時間） |
| `install-service.sh` | 一鍵安裝並啟動 timer 服務 |
| `check-service.sh` | 檢查 timer 狀態與查看最近推播日誌 |
| `uninstall-service.sh` | 一鍵停止並移除服務 |

---

## 🚀 部署步驟

### 步驟 1：修改 service 設定檔中的路徑與使用者
開啟 `gemini-news-bot.service`，將其中的路徑修改為您主機的實際路徑：
```ini
User=pi
WorkingDirectory=/home/pi/gemini-agent-toolkit
Environment="PATH=/home/pi/gemini-agent-toolkit/.venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/pi/gemini-agent-toolkit/.venv/bin/python /home/pi/gemini-agent-toolkit/telegram_bot/app_news_broadcast_bot.py
```

### 步驟 2：執行安裝腳本
賦予執行權限並安裝：
```bash
chmod +x install-service.sh check-service.sh uninstall-service.sh
./install-service.sh
```

### 步驟 3：查看執行狀態與日誌
```bash
./check-service.sh
```
若需要手動立即測試執行一次 service（不等待 timer）：
```bash
sudo systemctl start gemini-news-bot.service
sudo journalctl -u gemini-news-bot.service -f
```
