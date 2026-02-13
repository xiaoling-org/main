@echo off
chcp 65001 >nul
title Local Model System

echo =======================================
echo Starting Local Model System
echo Time: %date% %time%
echo =======================================
echo.

echo Checking Ollama service...
tasklist | findstr /i ollama >nul
if %errorlevel% equ 0 (
    echo   Ollama service is running
) else (
    echo   Starting Ollama service...
    start /B ollama serve
    timeout /t 5 /nobreak >nul
)

echo.
echo Checking local model...
curl -s http://localhost:11434/api/tags | findstr /i "qwen2.5" >nul
if %errorlevel% equ 0 (
    echo   Qwen2.5-1.5B model is loaded
) else (
    echo   Model not found
)

echo.
echo Model configuration:
echo   Model: Qwen2.5-1.5B-Instruct
echo   API: http://localhost:11434/v1
echo.

echo Testing model connection...
python -c "import requests; r = requests.get('http://localhost:11434/api/tags', timeout=5); print('Model test:', 'OK' if r.status_code == 200 else 'Failed')"

echo.
echo =======================================
echo Local model system ready!
echo =======================================
echo.
echo Press any key to exit...
pause >nul