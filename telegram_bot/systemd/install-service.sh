#!/bin/bash
# 安裝並啟動 Gemini News Bot 系統排程服務

echo "📦 正在安裝 Gemini News Bot Systemd Timer 服務..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 複製 service 與 timer 檔案到 systemd 目錄
sudo cp "$SCRIPT_DIR/gemini-news-bot.service" /etc/systemd/system/
sudo cp "$SCRIPT_DIR/gemini-news-bot.timer" /etc/systemd/system/

# 重新載入 systemd 配置
echo "🔄 重新載入 systemd 設定..."
sudo systemctl daemon-reload

# 啟用並啟動 timer
echo "▶️ 啟用並啟動 gemini-news-bot.timer..."
sudo systemctl enable gemini-news-bot.timer
sudo systemctl start gemini-news-bot.timer

echo ""
echo "✅ 安裝成功！"
echo ""
echo "📊 Timer 狀態："
sudo systemctl status gemini-news-bot.timer --no-pager

echo ""
echo "📋 查看定時任務清單："
sudo systemctl list-timers gemini-news-bot.timer --no-pager
