@echo off
echo ========================================
echo 小灵同学看板移动应用启动脚本
echo ========================================
echo.

echo 正在检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js未安装！
    echo 请先安装Node.js 18+
    pause
    exit /b 1
)

echo ✅ Node.js已安装
echo.

echo 正在检查React Native环境...
cd /d "C:\Users\czp\openclaw\kanban-mobile-app"
if not exist "node_modules" (
    echo ⚠️ node_modules不存在，正在安装依赖...
    npm install
) else (
    echo ✅ 依赖已安装
)

echo.
echo 正在启动React Native开发服务器...
echo.
echo 📱 应用信息：
echo • 项目路径：kanban-mobile-app
echo • 开发服务器：http://localhost:8081
echo • Metro Bundler：已启动
echo • 热重载：已启用
echo.
echo 📋 启动方式：
echo 1. Android模拟器：npx react-native run-android
echo 2. iOS模拟器：npx react-native run-ios
echo 3. 真机调试：扫描二维码
echo.
echo 🔧 常用命令：
echo • 重启服务器：npx react-native start --reset-cache
echo • 清除构建：cd android && gradlew clean
echo • 查看日志：npx react-native log-android
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

:: 启动Metro开发服务器
npx react-native start

if errorlevel 1 (
    echo.
    echo ❌ 开发服务器启动失败！
    echo 可能原因：
    echo 1. 端口8081被占用
    echo 2. Node.js版本不兼容
    echo 3. 依赖安装不完整
    echo.
    echo 尝试解决方案：
    echo 1. 检查端口：netstat -ano | findstr :8081
    echo 2. 清除缓存：npx react-native start --reset-cache
    echo 3. 重新安装依赖：npm install
    pause
)