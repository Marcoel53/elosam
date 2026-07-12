@echo off
title Instalador EloSam OS

cd /d "%~dp0"

echo ==========================================
echo       INSTALANDO ELOSAM OS DESKTOP
echo ==========================================
echo.

python --version

if errorlevel 1 (
    echo.
    echo ERRO: Python nao encontrado.
    echo Instale Python 3.11 ou 3.12.
    echo Marque Add Python to PATH.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

echo.
echo Atualizando pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip

echo.
echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo.
echo ==========================================
echo       INSTALACAO CONCLUIDA
echo ==========================================
echo.
echo Agora execute:
echo INICIAR_ELOSAM.bat
echo.

pause
