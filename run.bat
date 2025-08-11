@echo off
setlocal enabledelayedexpansion

title Bilibili 关注管理器

echo.
echo ========================================
echo   Bilibili Follow Manager
echo ========================================
echo.

:: 检查 Python 是否安装
echo [1/4] Checking Python environment...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not detected, please install Python 3.7+
    echo.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python environment check passed

:: 检查配置文件
echo.
echo [2/4] Checking configuration file...
if not exist "config.json" (
    echo [ERROR] config.json does not exist
    echo.
    echo 请按以下步骤操作:
    echo 1. 复制 config.example.json 为 config.json
    echo 2. 编辑 config.json 填入您的登录信息
    echo.
    echo 按任意键查看详细使用说明...
    pause >nul
    if exist "USAGE.md" start "" "USAGE.md"
    exit /b 1
)
echo [OK] Configuration file check passed

:: 检查并安装依赖
echo.
echo [3/4] Checking dependencies...
python -c "import requests" >nul 2>&1
if !errorlevel! neq 0 (
    echo [INSTALL] Installing required dependencies...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies
        echo.
        echo 可能的解决方案:
        echo 1. 检查网络连接
        echo 2. 尝试手动运行: pip install requests
        echo 3. 确认 pip 已正确安装
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies check passed
)

:: 运行程序
echo.
echo [4/4] Starting program...
echo.
python main.py

echo.
echo 程序已退出，按任意键关闭窗口...
pause >nul
