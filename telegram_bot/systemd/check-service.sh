#!/bin/bash
# 檢查 Gemini News Bot 服務狀態

echo "📊 【Gemini News Bot Timer 狀態】"
sudo systemctl status gemini-news-bot.timer --no-pager
echo ""

echo "📋 【排程執行時間表】"
sudo systemctl list-timers gemini-news-bot.timer --no-pager
echo ""

echo "📜 【最近執行日誌 (Journal Log)】"
sudo journalctl -u gemini-news-bot.service -n 20 --no-pager
