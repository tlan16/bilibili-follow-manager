@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

title Bilibili 关注管理器

echo.
echo ========================================
echo   Bilibili 关注管理器
echo ========================================
echo.

:: 检查 Python 是否安装
echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7 或更高版本
    echo.
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 环境检查通过

:: 检查配置文件
echo.
echo [2/4] 检查配置文件...
if not exist "config.json" (
    echo [错误] 配置文件 config.json 不存在
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
echo [OK] 配置文件检查通过

:: 检查并安装依赖
echo.
echo [3/4] 检查依赖包...
python -c "import requests" >nul 2>&1
if !errorlevel! neq 0 (
    echo [安装] 正在安装必要的依赖包...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [错误] 依赖包安装失败
        echo.
        echo 可能的解决方案:
        echo 1. 检查网络连接
        echo 2. 尝试手动运行: pip install requests
        echo 3. 确认 pip 已正确安装
        pause
        exit /b 1
    )
    echo [OK] 依赖包安装完成
) else (
    echo [OK] 依赖包检查通过
)

:: 运行程序
echo.
echo [4/4] 启动程序...
echo.
python main.py

echo.
echo 程序已退出，按任意键关闭窗口...
pause >nul
