@echo off
echo ========================================
echo React Native 开发环境检查工具
echo ========================================
echo.

echo 1. 检查 Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装
    echo 请下载: https://nodejs.org/
) else (
    echo ✅ Node.js 已安装
)

echo.
echo 2. 检查 npm...
npm --version
if %errorlevel% neq 0 (
    echo ❌ npm 未安装
) else (
    echo ✅ npm 已安装
)

echo.
echo 3. 检查 Java...
where java >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Java JDK 未安装
    echo 请下载: https://www.oracle.com/java/technologies/downloads/#jdk17-windows
    echo 或安装 Android Studio (自带JDK)
) else (
    echo ✅ Java 已安装
    java -version
)

echo.
echo 4. 检查 React Native CLI...
where react-native >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ React Native CLI 未安装
    echo 运行: npm install -g react-native-cli
) else (
    echo ✅ React Native CLI 已安装
    react-native --version
)

echo.
echo 5. 检查 Android 环境...
where adb >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Android SDK 未安装
    echo 请下载 Android Studio: https://developer.android.com/studio
) else (
    echo ✅ Android SDK 已安装
)

echo.
echo ========================================
echo 安装指南:
echo 1. 安装 Java JDK 17 (如果未安装)
echo 2. 安装 Android Studio (如果未安装)
echo 3. 设置环境变量:
echo    - JAVA_HOME: JDK安装路径
echo    - ANDROID_HOME: Android SDK路径
echo 4. 安装 React Native CLI: npm install -g react-native-cli
echo ========================================

pause