@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul

set PYTHON_CMD=
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=python
    goto run_app
)

py --version >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=py
    goto run_app
)

python3 --version >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=python3
    goto run_app
)

echo 未找到Python，请先安装Python 3.7+
pause
exit /b 1

:run_app
!PYTHON_CMD! app.py
if !errorlevel! neq 0 pause
