@echo off
echo 设置React Native开发环境变量
echo.

echo 1. 设置JAVA_HOME (请根据实际安装路径修改)
setx JAVA_HOME "C:\Program Files\Amazon Corretto\jdk17.0.0_35"
if errorlevel 1 (
    echo 警告: JAVA_HOME设置失败，请手动设置
)

echo.
echo 2. 设置Android环境变量
setx ANDROID_HOME "%LOCALAPPDATA%\Android\Sdk"
setx ANDROID_SDK_ROOT "%LOCALAPPDATA%\Android\Sdk"

echo.
echo 3. 更新PATH环境变量 (需要手动添加到系统PATH)
echo 请将以下路径添加到系统PATH环境变量:
echo   %ANDROID_HOME%\platform-tools
echo   %ANDROID_HOME%\tools
echo   %ANDROID_HOME%\tools\bin
echo   %JAVA_HOME%\bin

echo.
echo 环境变量设置完成!
echo 注意: 需要重启命令行窗口或系统使环境变量生效
echo.
pause