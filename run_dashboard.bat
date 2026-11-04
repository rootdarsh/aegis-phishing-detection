@echo off
title AEGIS Web Telemetry Dashboard (Streamlit)
cd /d "%~dp0dashboard"
echo =========================================================
echo       AEGIS Threat Assessment Dashboard (Streamlit)
echo =========================================================
echo Starting Streamlit app at http://localhost:8501 ...
python -m streamlit run app.py
pause
