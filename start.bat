@echo off
echo =======================================================
echo Starting AI-Powered Smart Car Assistance Full-Stack...
echo =======================================================
echo.
echo Starting FastAPI Backend...
start "FastAPI Backend" cmd /k "python -m uvicorn app.main:app --port 8000"

echo.
echo Both servers are starting up in separate terminal windows!
echo - Backend: http://127.0.0.1:8000

echo.
pause
