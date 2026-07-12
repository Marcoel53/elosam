@echo off
title EloSam OS

cd /d "%~dp0"

echo ==========================================
echo          ELOSAM OS DESKTOP
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Ambiente virtual nao encontrado.
    echo Execute INSTALAR.bat primeiro.
    pause
    exit /b 1
)

start "" http://127.0.0.1:8080

".venv\Scripts\python.exe" main.py

pause
