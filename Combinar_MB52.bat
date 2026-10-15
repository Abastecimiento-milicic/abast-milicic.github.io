@echo off
cd /d "%~dp0"
title Combinar MB52 con Analisis MM - Milicic

echo ===========================================================================
echo       COMBINAR STOCK ALMACEN MB52 CON ANALISIS MM (SAP)
echo ===========================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta en el PATH.
    pause
    exit /b 1
)

python "scripts\combinar_mb52_analisis_mm.py"

echo.
pause
