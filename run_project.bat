@echo off
echo ===================================================
echo     CAREER COMPASS AI — LOCAL STARTUP SCRIPT
echo ===================================================
echo.

echo Checking port 8000 for stale server processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /r ":8000 .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Starting Python FastAPI Backend on http://127.0.0.1:8000...
start "Career Compass AI - Backend API" cmd /k "cd server && call venv\Scripts\activate && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak >nul

echo Starting Vite Frontend on http://localhost:5000...
echo.
npm run dev

pause
