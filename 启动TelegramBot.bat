@echo off
echo ========================================
echo 小灵同学看板系统 Telegram Bot
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装！
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

echo 正在检查依赖...
cd /d "C:\Users\czp\openclaw\kanban-telegram-bot"
pip install python-telegram-bot requests python-dotenv >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 依赖安装失败，尝试手动安装...
    pip install python-telegram-bot requests python-dotenv
)

echo ✅ 依赖检查完成
echo.

echo ⚠️ 重要：需要Telegram Bot Token
echo.
echo 创建Bot步骤：
echo 1. 在Telegram中搜索 @BotFather
echo 2. 发送 /newbot 创建新机器人
echo 3. 设置名称：小灵同学看板助手
echo 4. 设置用户名：XiaoLing_Kanban_Bot
echo 5. 复制Bot Token
echo.
echo 创建环境配置文件：
echo 1. 复制 .env.example 为 .env
echo 2. 编辑 .env 文件
echo 3. 设置 TELEGRAM_BOT_TOKEN=你的Token
echo.

if not exist ".env" (
    echo ❌ .env 配置文件不存在
    echo 正在创建示例配置文件...
    copy .env.example .env
    echo.
    echo ⚠️ 请编辑 .env 文件设置Bot Token
    echo 然后重新运行此脚本
    pause
    exit /b 1
)

echo 正在启动Telegram Bot...
echo.
echo 🤖 Bot信息：
echo • 项目路径：kanban-telegram-bot
echo • 配置文件：.env
echo • 日志文件：bot.log
echo • 状态：启动中...
echo.
echo 📱 使用说明：
echo 1. 在Telegram中搜索你的Bot用户名
echo 2. 发送 /start 开始使用
echo 3. 使用 /help 查看命令
echo.
echo 🔗 需要配合看板系统后端：
echo • 确保后端服务已启动
echo • API地址：http://localhost:5000
echo • 使用 /login 命令登录系统
echo ========================================
echo.

:: 启动Bot
python bot.py

if errorlevel 1 (
    echo.
    echo ❌ Bot启动失败！
    echo 可能原因：
    echo 1. Bot Token无效
    echo 2. 网络连接问题
    echo 3. Python依赖问题
    echo.
    echo 检查步骤：
    echo 1. 确认 .env 文件中的Token
    echo 2. 检查网络连接
    echo 3. 重新安装依赖：pip install -r requirements.txt
    pause
)