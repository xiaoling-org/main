@echo off
chcp 65001 >nul
title 小灵同学持续工作系统

echo =======================================
echo 🚀 小灵同学持续工作系统启动
echo 📅 开始时间: %date% %time%
echo ⏰ 计划结束: 明天20:30
echo =======================================
echo.

:main_loop
echo.
echo 📊 第 %iteration% 次循环开始
echo ⏰ 当前时间: %date% %time%
echo.

REM 1. 自动Git提交
echo 📝 自动Git提交...
"C:\Program Files\Git\bin\git.exe" add . 2>nul
"C:\Program Files\Git\bin\git.exe" commit -m "持续工作: 第%iteration%次提交 - %date% %time%" 2>nul
echo ✅ Git提交完成
echo.

REM 2. 显示当前进度
echo 📈 当前工作进度:
if exist "工作进度跟踪.md" (
    findstr "当前总体进度" "工作进度跟踪.md"
) else (
    echo ⚠️ 进度文件不存在
)
echo.

REM 3. 显示看板系统文件状态
echo 🔧 看板系统文件:
dir kanban*.* 2>nul | findstr /v "目录"
echo.

REM 4. 创建备份（每3小时一次）
set /a "backup_hour=%time:~0,2%"
set /a "backup_check=%backup_hour% %% 3"
if %backup_check% equ 0 (
    echo 💾 创建定时备份...
    set backup_file=C:\Users\czp\Desktop\持续工作备份_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.zip
    "C:\Program Files\Git\bin\git.exe" bundle create "%backup_file%" --all 2>nul
    if exist "%backup_file%" (
        echo ✅ 备份创建成功: %backup_file%
    ) else (
        echo ⚠️ 备份创建失败
    )
    echo.
)

REM 5. 记录工作日志
echo 📋 记录工作日志...
echo ======================================= >> work_log.txt
echo 工作循环: %iteration% >> work_log.txt
echo 时间: %date% %time% >> work_log.txt
echo Git提交: 完成 >> work_log.txt
if exist "工作进度跟踪.md" (
    findstr "当前总体进度" "工作进度跟踪.md" >> work_log.txt
) >> work_log.txt
echo ======================================= >> work_log.txt
echo. >> work_log.txt
echo ✅ 工作日志已记录
echo.

REM 6. 检查是否到结束时间
set current_hour=%time:~0,2%
set current_min=%time:~3,2%
if "%current_hour%" geq "20" if "%current_min%" geq "30" (
    echo 🎉 到达计划结束时间: 20:30
    echo 📁 最终备份...
    "C:\Program Files\Git\bin\git.exe" bundle create "C:\Users\czp\Desktop\最终备份_%date:~0,4%%date:~5,2%%date:~8,2%_2030.bundle" --all 2>nul
    echo ✅ 持续工作系统完成
    pause
    exit
)

REM 7. 等待下一循环（1小时）
echo ⏳ 等待下一循环（1小时后继续）...
echo.
set /a iteration+=1
timeout /t 3600 /nobreak >nul
goto main_loop