#!/bin/bash
# 移除 Gemini News Bot 服務

echo "🛑 正在停止並移除 Gemini News Bot 服務..."

sudo systemctl stop gemini-news-bot.timer
sudo systemctl disable gemini-news-bot.timer

sudo rm -f /etc/systemd/system/gemini-news-bot.service
sudo rm -f /etc/systemd/system/gemini-news-bot.timer

sudo systemctl daemon-reload
echo "✅ 已成功移除服務！"
