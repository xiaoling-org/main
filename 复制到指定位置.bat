@echo off
chcp 65001 >nul
echo ========================================
echo   看板系统文件复制工具
echo ========================================
echo.

echo 📦 当前文件位置: C:\Users\czp\openclaw\kanban_control_center_v1.0.zip
echo 📊 文件大小: 19.5 KB
echo.

echo 🎯 请选择复制目标:
echo 1. 复制到桌面 (快速访问)
echo 2. 复制到下载文件夹 (推荐)
echo 3. 复制到指定路径
echo 4. 查看文件信息
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo 📋 复制到桌面...
    copy "kanban_control_center_v1.0.zip" "%USERPROFILE%\Desktop\看板系统.zip"
    echo ✅ 已复制到: %USERPROFILE%\Desktop\看板系统.zip
    goto :end
)

if "%choice%"=="2" (
    echo 📋 复制到下载文件夹...
    copy "kanban_control_center_v1.0.zip" "%USERPROFILE%\Downloads\kanban_system.zip"
    echo ✅ 已复制到: %USERPROFILE%\Downloads\kanban_system.zip
    goto :end
)

if "%choice%"=="3" (
    set /p target="请输入目标路径 (例如 D:\\): "
    echo 📋 复制到指定路径...
    copy "kanban_control_center_v1.0.zip" "%target%\kanban_system.zip"
    echo ✅ 已复制到: %target%\kanban_system.zip
    goto :end
)

if "%choice%"=="4" (
    echo 📊 文件信息:
    echo - 名称: kanban_control_center_v1.0.zip
    echo - 大小: 19.5 KB
    echo - 内容: 完整看板系统 v1.0
    echo - 包含: Flask应用 + 界面 + 脚本 + 文档
    echo.
    echo 🚀 使用步骤:
    echo 1. 解压到任意目录
    echo 2. 运行: 启动看板系统.bat
    echo 3. 访问: http://localhost:5000
    goto :end
)

echo ❌ 无效选择
goto :end

:end
echo.
echo ========================================
echo   按任意键退出...
echo ========================================
pause >nul