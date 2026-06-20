@echo off
title HackLens Launcher
echo =====================================================================
echo                    HackLens - AI-Powered Evaluator
echo =====================================================================
echo.
echo [1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "HackLens Backend" cmd /k "cd backend && .venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"

echo [2/2] Launching Vite React Frontend ...
start "HackLens Frontend" cmd /k "cd frontend && npm run dev"
echo.
echo =====================================================================
echo Services started! Keep the console windows open to view logs.
echo Press any key to exit this launcher...
echo =====================================================================
pause > nul
