@echo off
title AEGIS Backend API (FastAPI)
cd /d "%~dp0backend"
echo =========================================================
echo       AEGIS Phishing Detection System - Backend API
echo =========================================================
echo Starting FastAPI server at http://127.0.0.1:8000 ...
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
