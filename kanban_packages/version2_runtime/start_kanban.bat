@echo off
chcp 65001 >nul
echo ========================================
echo   小灵同学看板系统 - 一键启动
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
if not exist "requirements.txt" (
    echo ❌ 未找到依赖文件 requirements.txt
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 正在检查Python依赖...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ⚠️  依赖安装失败，尝试使用国内镜像...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
)

REM 启动服务器
echo 🚀 正在启动看板系统...
echo.
echo ========================================
echo   访问地址：
echo   电脑：http://localhost:5000
echo   手机：http://%COMPUTERNAME%:5000
echo ========================================
echo.
echo 📱 请确保手机和电脑在同一WiFi网络
echo ⏳ 按 Ctrl+C 停止服务器
echo ========================================

python kanban_enhanced.py

pause