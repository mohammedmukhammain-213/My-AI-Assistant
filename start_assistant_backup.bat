@echo off

cd /d C:\Users\pandu\AIAssistant

call venv\Scripts\activate

start "" /min cmd /c "uvicorn backend.main:app --reload"

start "" /min cmd /c "python -m http.server 5500 --directory website"

timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:5500"

exit