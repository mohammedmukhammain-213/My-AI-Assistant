@echo off

cd /d C:\Users\pandu\AIAssistant

call venv\Scripts\activate

start "" /min cmd /c "uvicorn backend.main:app --host 0.0.0.0 --port 8000"
start "" /min cmd /c "python https_server.py"

timeout /t 3 /nobreak >nul

start "" "https://192.168.29.86:5500"

exit
