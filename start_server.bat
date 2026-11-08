@echo off
cd /d "%~dp0"
if not exist .env (
  echo Create .env from .env.example and set DEEPSEEK_AUTH_TOKEN
  pause
  exit /b 1
)
python openai_server.py
pause
