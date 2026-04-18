@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动 ImageTool...
python src/main.py
pause
