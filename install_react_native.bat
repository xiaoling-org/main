@echo off
echo ========================================
echo React Native 开发环境自动安装脚本
echo 请以管理员身份运行此脚本！
echo ========================================
echo.

echo 正在安装 Chocolatey 包管理器...
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

echo.
echo 正在安装 Java JDK 17 (Amazon Corretto)...
choco install corretto17jdk -y

echo.
echo 正在安装 Android Studio...
choco install androidstudio -y

echo.
echo 正在安装 Android SDK...
choco install android-sdk -y

echo.
echo 正在安装 React Native CLI...
npm install -g react-native-cli

echo.
echo 设置环境变量...
setx JAVA_HOME "C:\Program Files\Amazon Corretto\jdk17.0.0_35" /M
setx ANDROID_HOME "%LOCALAPPDATA%\Android\Sdk" /M

echo.
echo 将Android工具添加到PATH...
setx PATH "%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%ANDROID_HOME%\tools\bin" /M

echo.
echo ========================================
echo 安装完成！请重启电脑使环境变量生效。
echo ========================================
echo.
echo 验证安装：
echo 1. 打开新的命令提示符
echo 2. 运行: java -version
echo 3. 运行: adb --version
echo 4. 运行: react-native --version
echo ========================================

pause