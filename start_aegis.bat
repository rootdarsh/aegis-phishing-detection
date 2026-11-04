@echo off
title AEGIS Launcher
echo ========================================================
echo        STARTING AEGIS COMPLETE PROJECT DEMO
echo ========================================================
echo Launching Backend API in new window...
start "AEGIS Backend API" cmd /c "%~dp0run_backend.bat"

echo Waiting 2 seconds for API to initialize...
timeout /t 2 /nobreak >nul

echo Launching Streamlit Dashboard in new window...
start "AEGIS Dashboard" cmd /c "%~dp0run_dashboard.bat"

echo.
echo All services launched!
echo - API Docs: http://127.0.0.1:8000/docs
echo - Dashboard: http://localhost:8501
echo.
pause
