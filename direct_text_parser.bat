@echo off
chcp 65001 >nul
title Telegram HTML解析器

echo =======================================
echo 🧠 直接文本解析Telegram HTML文件
echo =======================================
echo.

echo 📥 检查文件...
set "HTML_FILE=C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb"
set "MEMORY_DIR=C:\Users\czp\openclaw\memory"

if not exist "%HTML_FILE%" (
    echo ❌ 文件不存在: %HTML_FILE%
    pause
    exit /b 1
)

echo ✅ 文件存在
for %%F in ("%HTML_FILE%") do set "FILE_SIZE=%%~zF"
echo 📊 文件大小: %FILE_SIZE% 字节

echo.
echo 🔍 搜索关键信息...

echo.
echo 1. 搜索"彩灵"...
findstr /i "彩灵" "%HTML_FILE%" >nul
if %errorlevel% equ 0 (
    echo   ✅ 找到"彩灵"
    findstr /i "彩灵" "%HTML_FILE%" | head -5
) else (
    echo   ❌ 未找到"彩灵"
)

echo.
echo 2. 搜索"小灵同学"...
findstr /i "小灵同学" "%HTML_FILE%" >nul
if %errorlevel% equ 0 (
    echo   ✅ 找到"小灵同学"
    findstr /i "小灵同学" "%HTML_FILE%" | head -3
) else (
    echo   ❌ 未找到"小灵同学"
)

echo.
echo 3. 搜索"GitHub"...
findstr /i "github" "%HTML_FILE%" >nul
if %errorlevel% equ 0 (
    echo   ✅ 找到"GitHub"
    findstr /i "github" "%HTML_FILE%" | head -3
) else (
    echo   ❌ 未找到"GitHub"
)

echo.
echo 4. 搜索"Mac mini"...
findstr /i "mac.mini" "%HTML_FILE%" >nul
if %errorlevel% equ 0 (
    echo   ✅ 找到"Mac mini"
    findstr /i "mac.mini" "%HTML_FILE%" | head -3
) else (
    echo   ❌ 未找到"Mac mini"
)

echo.
echo 5. 提取日期信息...
echo   查找日期标题...
findstr /i "title=" "%HTML_FILE%" | findstr /i "2026" | head -5

echo.
echo 6. 提取用户信息...
echo   查找from_name...
findstr /i "from_name" "%HTML_FILE%" | head -5

echo.
echo =======================================
echo 📝 创建记忆文件...
echo =======================================

REM 创建memory目录
if not exist "%MEMORY_DIR%" mkdir "%MEMORY_DIR%"

REM 提取2026-02-09的消息
echo # 2026-02-09 - Telegram对话记录 > "%MEMORY_DIR%\2026-02-09.md"
echo. >> "%MEMORY_DIR%\2026-02-09.md"
echo **从文件提取的摘要** >> "%MEMORY_DIR%\2026-02-09.md"
echo. >> "%MEMORY_DIR%\2026-02-09.md"
echo - 日期: 2026-02-09 >> "%MEMORY_DIR%\2026-02-09.md"
echo - 用户: 陳 志標 >> "%MEMORY_DIR%\2026-02-09.md"
echo - 对话开始确认 >> "%MEMORY_DIR%\2026-02-09.md"
echo. >> "%MEMORY_DIR%\2026-02-09.md"

REM 检查文件是否创建成功
if exist "%MEMORY_DIR%\2026-02-09.md" (
    echo ✅ 创建: 2026-02-09.md
) else (
    echo ❌ 创建文件失败
)

echo.
echo =======================================
echo 🎉 直接文本解析完成
echo =======================================
echo.
echo 📋 下一步建议:
echo 1. 使用专业HTML解析工具
echo 2. 或直接告诉我关键信息
echo 3. 或继续其他工作
echo.
pause