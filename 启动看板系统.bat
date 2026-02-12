@echo off
echo ========================================
echo 小灵同学看板系统启动脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装！
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

echo 正在检查依赖...
cd /d "C:\Users\czp\openclaw\kanban-backend"
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 依赖安装失败，尝试手动安装...
    pip install flask flask-jwt-extended flask-socketio flask-cors
)

echo ✅ 依赖检查完成
echo.

echo 正在启动看板系统后端...
echo.
echo 📊 服务信息：
echo • 后端API: http://localhost:5000
echo • WebSocket: ws://localhost:5000
echo • 数据库: SQLite3 (kanban.db)
echo • 文件上传: uploads/ 目录
echo.
echo 📋 API文档：kanban-backend\API文档.md
echo.

echo 按 Ctrl+C 停止服务
echo ========================================
echo.

:: 启动Flask应用
python app.py

if errorlevel 1 (
    echo.
    echo ❌ 服务启动失败！
    echo 可能原因：
    echo 1. 端口5000被占用
    echo 2. Python依赖问题
    echo 3. 数据库文件损坏
    echo.
    echo 尝试解决方案：
    echo 1. 检查端口：netstat -ano | findstr :5000
    echo 2. 重新安装依赖：pip install -r requirements.txt
    echo 3. 删除数据库文件重新初始化
    pause
)