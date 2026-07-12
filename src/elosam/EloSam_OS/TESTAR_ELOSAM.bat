@echo off
title Teste EloSam OS

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Execute INSTALAR.bat primeiro.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -c "from elosam.kernel.kernel import Kernel; print('IMPORT DO KERNEL: OK')"

pause
