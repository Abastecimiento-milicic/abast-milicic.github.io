@echo off
cd /d "%~dp0"
title Generar Control de Movimientos MB51 - Milicic

echo ===========================================================================
echo       CONSOLIDADOR DE CONTROL DE MOVIMIENTOS MB51 (SAP)
echo ===========================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta en el PATH.
    pause
    exit /b 1
)

python "scripts\generar_control_movimientos.py"

echo.
pause
