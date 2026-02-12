@echo off
echo ========================================
echo React Native 开发环境安装
echo ========================================

echo.
echo 1. 检查Node.js版本...
node --version
if errorlevel 1 (
    echo 错误: Node.js未安装或未在PATH中
    echo 请先安装Node.js: https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo 2. 检查npm版本...
call :checkNpm
if errorlevel 1 (
    echo 警告: npm检查失败，但继续安装...
)

echo.
echo 3. 检查Java...
java -version >nul 2>&1
if errorlevel 1 (
    echo Java未安装
    echo 请安装Java JDK 17或更高版本
    echo 推荐: Amazon Corretto 17
    echo 下载: https://corretto.aws/downloads/latest/amazon-corretto-17-x64-windows-jdk.msi
    echo.
) else (
    echo Java已安装
    java -version
)

echo.
echo 4. 安装React Native CLI...
echo 这可能需要几分钟...
npm install -g react-native-cli
if errorlevel 1 (
    echo 警告: 全局安装失败，尝试用户级安装...
    npm install react-native-cli
)

echo.
echo 5. 设置环境变量...
echo 创建环境变量设置脚本...
(
echo @echo off
echo echo 设置React Native环境变量...
echo setx ANDROID_HOME "%%LOCALAPPDATA%%\Android\Sdk"
echo setx ANDROID_SDK_ROOT "%%LOCALAPPDATA%%\Android\Sdk"
echo echo 环境变量已设置！
) > set_env_vars.bat

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步操作：
echo 1. 下载并安装Android Studio
echo    地址: https://developer.android.com/studio
echo.
echo 2. 安装Android Studio后，运行 set_env_vars.bat 设置环境变量
echo.
echo 3. 将以下路径添加到系统PATH环境变量：
echo    - %%ANDROID_HOME%%\platform-tools
echo    - %%ANDROID_HOME%%\tools
echo    - %%ANDROID_HOME%%\tools\bin
echo.
echo 4. 创建React Native项目：
echo    npx react-native init MyApp
echo.
pause
exit /b 0

:checkNpm
timeout /t 3 /nobreak >nul
npm --version >nul 2>&1
exit /b %errorlevel%