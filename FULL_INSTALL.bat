@echo off
echo ========================================
echo Java JDK 17 和 Android Studio 完整安装脚本
echo ========================================
echo.

echo 步骤1: 检查文件是否存在
if exist "C:\Users\czp\Downloads\amazon-corretto-17.msi" (
    echo ✓ Amazon Corretto 17 JDK 已下载
) else (
    echo ✗ Amazon Corretto 17 JDK 未找到
    goto :error
)

if exist "C:\Users\czp\Downloads\android-studio.exe" (
    echo ✓ Android Studio 已下载
) else (
    echo ✗ Android Studio 未找到
    goto :error
)

echo.
echo 步骤2: 安装Java JDK 17（需要管理员权限）
echo 请以管理员身份运行此脚本继续...
echo 按任意键继续安装Java JDK...
pause > nul

echo 正在安装Java JDK 17...
msiexec /i "C:\Users\czp\Downloads\amazon-corretto-17.msi" /quiet /norestart
if %ERRORLEVEL% EQU 0 (
    echo ✓ Java JDK 17 安装已启动
) else (
    echo ✗ Java JDK 17 安装失败
    goto :error
)

echo.
echo 步骤3: 设置环境变量
echo 正在设置环境变量...
powershell -ExecutionPolicy Bypass -File "C:\Users\czp\openclaw\set_env_vars.ps1"

echo.
echo 步骤4: 安装Android Studio
echo 按任意键启动Android Studio安装程序...
pause > nul

echo 正在启动Android Studio安装程序...
start "" "C:\Users\czp\Downloads\android-studio.exe"

echo.
echo 步骤5: 安装React Native CLI（需要Node.js）
echo 请先完成以下步骤：
echo 1. 安装Node.js（如果尚未安装）
echo 2. 重启命令提示符使环境变量生效
echo 3. 运行: powershell -ExecutionPolicy Bypass -File "C:\Users\czp\openclaw\install_react_native.ps1"
echo.

echo 安装指南已保存到: C:\Users\czp\openclaw\INSTALLATION_GUIDE.md
echo.
echo 按任意键退出...
pause > nul
exit /b 0

:error
echo.
echo 安装过程中出现错误。请查看上面的错误信息。
echo 按任意键退出...
pause > nul
exit /b 1