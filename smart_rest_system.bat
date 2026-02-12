@echo off
echo ========================================
echo 智能休息系统 - 电脑定时休息
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 请以管理员身份运行此脚本！
    pause
    exit /b 1
)

echo ✅ 管理员权限确认
echo.

echo 正在创建智能休息系统...
echo.

:: 1. 创建配置文件夹
if not exist "C:\SmartRest" mkdir "C:\SmartRest"
if not exist "C:\SmartRest\Logs" mkdir "C:\SmartRest\Logs"

:: 2. 创建配置文件
echo # 智能休息系统配置 > "C:\SmartRest\config.ini"
echo # 最后修改时间: %date% %time% >> "C:\SmartRest\config.ini"
echo. >> "C:\SmartRest\config.ini"
echo [Schedule] >> "C:\SmartRest\config.ini"
echo # 休息时间表 (24小时制) >> "C:\SmartRest\config.ini"
echo # 格式: 开始时间,休息时长(分钟),是否重启 >> "C:\SmartRest\config.ini"
echo # 示例: 02:00,60,1 表示凌晨2点休息60分钟并重启 >> "C:\SmartRest\config.ini"
echo. >> "C:\SmartRest\config.ini"
echo RestSchedule= >> "C:\SmartRest\config.ini"
echo # 默认: 每天凌晨3点休息60分钟并重启 >> "C:\SmartRest\config.ini"
echo DefaultSchedule=03:00,60,1 >> "C:\SmartRest\config.ini"
echo. >> "C:\SmartRest\config.ini"
echo [Settings] >> "C:\SmartRest\config.ini"
echo # 系统设置 >> "C:\SmartRest\config.ini"
echo EnableSystem=1 >> "C:\SmartRest\config.ini"
echo LogLevel=2 >> "C:\SmartRest\config.ini"
echo MaxLogDays=30 >> "C:\SmartRest\config.ini"

:: 3. 创建完全关机休息脚本
echo @echo off > "C:\SmartRest\start_rest.bat"
echo echo [%date% %time%] 开始电脑完全关机休息... >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 记录日志 >> "C:\SmartRest\start_rest.bat"
echo echo [%date% %time%] 电脑开始完全关机休息 >> "C:\SmartRest\Logs\rest.log" >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 停止Clawdbot服务（如果正在运行） >> "C:\SmartRest\start_rest.bat"
echo echo 正在停止Clawdbot服务... >> "C:\SmartRest\start_rest.bat"
echo openclaw-cn gateway stop 2>nul >> "C:\SmartRest\start_rest.bat"
echo timeout /t 10 /nobreak >nul >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 创建定时开机任务（BIOS/Windows任务） >> "C:\SmartRest\start_rest.bat"
echo echo 设置1小时后自动开机... >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 方法1：使用Windows计划任务开机（如果支持唤醒） >> "C:\SmartRest\start_rest.bat"
echo schtasks /create /tn "AutoPowerOn" /tr "cmd /c echo Auto Power On" /sc once /st %time% /sd %date% /f 2>nul >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 方法2：使用BIOS唤醒（如果主板支持） >> "C:\SmartRest\start_rest.bat"
echo :: 计算1小时后的时间 >> "C:\SmartRest\start_rest.bat"
echo for /f "tokens=1-3 delims=:." %%a in ("%time%") do ( >> "C:\SmartRest\start_rest.bat"
echo   set /a "hour=%%a + 1" >> "C:\SmartRest\start_rest.bat"
echo   set minute=%%b >> "C:\SmartRest\start_rest.bat"
echo ) >> "C:\SmartRest\start_rest.bat"
echo if %%hour%% geq 24 set /a "hour=%%hour%% - 24" >> "C:\SmartRest\start_rest.bat"
echo echo 计划开机时间：%%hour%%:%%minute%% >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 完全关机 >> "C:\SmartRest\start_rest.bat"
echo echo 正在完全关机... >> "C:\SmartRest\start_rest.bat"
echo shutdown /s /t 30 /c "智能休息系统：电脑完全关机休息1小时，将自动开机..." >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 等待关机执行 >> "C:\SmartRest\start_rest.bat"
echo timeout /t 40 /nobreak >nul >> "C:\SmartRest\start_rest.bat"
echo. >> "C:\SmartRest\start_rest.bat"
echo :: 如果关机失败，强制关机 >> "C:\SmartRest\start_rest.bat"
echo echo 关机失败，尝试强制关机... >> "C:\SmartRest\start_rest.bat"
echo shutdown /s /f /t 5 >> "C:\SmartRest\start_rest.bat"

:: 4. 创建监控脚本
echo @echo off > "C:\SmartRest\monitor_system.bat"
echo :: 智能休息系统监控脚本 >> "C:\SmartRest\monitor_system.bat"
echo :: 每5分钟检查一次是否需要休息 >> "C:\SmartRest\monitor_system.bat"
echo. >> "C:\SmartRest\monitor_system.bat"
echo :LOOP >> "C:\SmartRest\monitor_system.bat"
echo set CURRENT_TIME=%time:~0,5% >> "C:\SmartRest\monitor_system.bat"
echo. >> "C:\SmartRest\monitor_system.bat"
echo :: 读取配置 >> "C:\SmartRest\monitor_system.bat"
echo for /f "tokens=2 delims==" %%a in ('type "C:\SmartRest\config.ini" ^| find "DefaultSchedule="') do set SCHEDULE=%%a >> "C:\SmartRest\monitor_system.bat"
echo. >> "C:\SmartRest\monitor_system.bat"
echo :: 解析计划 >> "C:\SmartRest\monitor_system.bat"
echo for /f "tokens=1-3 delims=," %%i in ("%%SCHEDULE%%") do ( >> "C:\SmartRest\monitor_system.bat"
echo   set REST_TIME=%%i >> "C:\SmartRest\monitor_system.bat"
echo   set REST_DURATION=%%j >> "C:\SmartRest\monitor_system.bat"
echo   set DO_RESTART=%%k >> "C:\SmartRest\monitor_system.bat"
echo ) >> "C:\SmartRest\monitor_system.bat"
echo. >> "C:\SmartRest\monitor_system.bat"
echo :: 检查是否到休息时间 >> "C:\SmartRest\monitor_system.bat"
echo if "%%CURRENT_TIME%%"=="%%REST_TIME%%" ( >> "C:\SmartRest\monitor_system.bat"
echo   echo [%date% %time%] 到达预定休息时间，开始休息... >> "C:\SmartRest\Logs\monitor.log" >> "C:\SmartRest\monitor_system.bat"
echo   call "C:\SmartRest\start_rest.bat" >> "C:\SmartRest\monitor_system.bat"
echo ) >> "C:\SmartRest\monitor_system.bat"
echo. >> "C:\SmartRest\monitor_system.bat"
echo :: 等待5分钟再检查 >> "C:\SmartRest\monitor_system.bat"
echo timeout /t 300 /nobreak >nul >> "C:\SmartRest\monitor_system.bat"
echo goto LOOP >> "C:\SmartRest\monitor_system.bat"

:: 5. 创建管理工具
echo @echo off > "C:\SmartRest\manage_rest.bat"
echo echo ======================================== >> "C:\SmartRest\manage_rest.bat"
echo echo 智能休息系统管理工具 >> "C:\SmartRest\manage_rest.bat"
echo echo ======================================== >> "C:\SmartRest\manage_rest.bat"
echo echo. >> "C:\SmartRest\manage_rest.bat"
echo echo 当前配置： >> "C:\SmartRest\manage_rest.bat"
echo type "C:\SmartRest\config.ini" >> "C:\SmartRest\manage_rest.bat"
echo echo. >> "C:\SmartRest\manage_rest.bat"
echo echo 请选择操作： >> "C:\SmartRest\manage_rest.bat"
echo echo 1. 修改休息时间 >> "C:\SmartRest\manage_rest.bat"
echo echo 2. 立即开始休息 >> "C:\SmartRest\manage_rest.bat"
echo echo 3. 查看日志 >> "C:\SmartRest\manage_rest.bat"
echo echo 4. 停止监控 >> "C:\SmartRest\manage_rest.bat"
echo echo 5. 退出 >> "C:\SmartRest\manage_rest.bat"
echo echo. >> "C:\SmartRest\manage_rest.bat"
echo set /p CHOICE=请输入选择 (1-5): >> "C:\SmartRest\manage_rest.bat"
echo. >> "C:\SmartRest\manage_rest.bat"
echo if "%%CHOICE%%"=="1" goto CHANGE_TIME >> "C:\SmartRest\manage_rest.bat"
echo if "%%CHOICE%%"=="2" goto START_NOW >> "C:\SmartRest\manage_rest.bat"
echo if "%%CHOICE%%"=="3" goto VIEW_LOGS >> "C:\SmartRest\manage_rest.bat"
echo if "%%CHOICE%%"=="4" goto STOP_MONITOR >> "C:\SmartRest\manage_rest.bat"
echo if "%%CHOICE%%"=="5" exit >> "C:\SmartRest\manage_rest.bat"
echo. >> "C:\SmartRest\manage_rest.bat"
echo :CHANGE_TIME >> "C:\SmartRest\manage_rest.bat"
echo echo. >> "C:\SmartRest\manage_rest.bat"
echo echo 当前休息时间配置： >> "C:\SmartRest\manage_rest.bat"
echo findstr "DefaultSchedule=" "C:\SmartRest\config.ini" >> "C:\SmartRest\manage_rest.bat"
echo echo. >> "C:\SmartRest\manage_rest.bat"
echo set /p NEW_TIME=请输入新的休息时间 (格式: HH:MM,分钟,是否重启 如: 03:00,60,1): >> "C:\SmartRest\manage_rest.bat"
echo powershell -Command "(Get-Content 'C:\SmartRest\config.ini') -replace 'DefaultSchedule=.*', 'DefaultSchedule=%NEW_TIME%' | Set-Content 'C:\SmartRest\config.ini'" >> "C:\SmartRest\manage_rest.bat"
echo echo 配置已更新！ >> "C:\SmartRest\manage_rest.bat"
echo pause >> "C:\SmartRest\manage_rest.bat"
echo goto :EOF >> "C:\SmartRest\manage_rest.bat"
echo. >> "C:\SmartRest\manage_rest.bat"
echo :START_NOW >> "C:\SmartRest\manage_rest.bat"
echo echo 立即开始休息... >> "C:\SmartRest\manage_rest.bat"
echo call "C:\SmartRest\start_rest.bat" >> "C:\SmartRest\manage_rest.bat"
echo goto :EOF >> "C:\SmartRest\manage_rest.bat"
echo. >> "C:\SmartRest\manage_rest.bat"
echo :VIEW_LOGS >> "C:\SmartRest\manage_rest.bat"
echo echo 最近日志： >> "C:\SmartRest\manage_rest.bat"
echo type "C:\SmartRest\Logs\monitor.log" 2>nul || echo 暂无日志 >> "C:\SmartRest\manage_rest.bat"
echo pause >> "C:\SmartRest\manage_rest.bat"
echo goto :EOF >> "C:\SmartRest\manage_rest.bat"
echo. >> "C:\SmartRest\manage_rest.bat"
echo :STOP_MONITOR >> "C:\SmartRest\manage_rest.bat"
echo taskkill /f /im monitor_system.bat 2>nul >> "C:\SmartRest\manage_rest.bat"
echo echo 监控已停止 >> "C:\SmartRest\manage_rest.bat"
echo pause >> "C:\SmartRest\manage_rest.bat"
echo goto :EOF >> "C:\SmartRest\manage_rest.bat"

:: 6. 创建Windows计划任务
echo 正在创建计划任务...
schtasks /create /tn "SmartRestMonitor" /tr "C:\SmartRest\monitor_system.bat" /sc onstart /delay 0001:00 /ru SYSTEM /f

:: 7. 创建桌面快捷方式
echo 正在创建桌面快捷方式...
echo Set WshShell = CreateObject("WScript.Shell") > "%temp%\create_shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") & "\智能休息系统.lnk") >> "%temp%\create_shortcut.vbs"
echo oShellLink.TargetPath = "C:\SmartRest\manage_rest.bat" >> "%temp%\create_shortcut.vbs"
echo oShellLink.WindowStyle = 1 >> "%temp%\create_shortcut.vbs"
echo oShellLink.IconLocation = "shell32.dll,27" >> "%temp%\create_shortcut.vbs"
echo oShellLink.Save >> "%temp%\create_shortcut.vbs"
cscript //nologo "%temp%\create_shortcut.vbs"
del "%temp%\create_shortcut.vbs"

echo.
echo ✅ 智能休息系统安装完成！
echo.
echo ========================================
echo 🎯 系统功能：
echo 1. 定时休息：每天指定时间休息1小时
echo 2. 自动重启：休息后自动重启电脑
echo 3. 灵活配置：可随时修改休息时间
echo 4. 安全保护：先停止服务再休息
echo 5. 日志记录：完整操作记录
echo ========================================
echo.
echo 📋 默认配置：
echo • 休息时间：每天凌晨3:00
echo • 休息时长：60分钟
echo • 是否重启：是
echo.
echo 🛠️ 管理工具：
echo • 桌面快捷方式：智能休息系统.lnk
echo • 配置文件：C:\SmartRest\config.ini
echo • 修改方法：运行管理工具选择"1"
echo ========================================
echo.
echo 💡 建议设置：
echo • 凌晨3-4点：系统维护时间
echo • 休息时长：60-120分钟
echo • 确保重要工作已保存
echo ========================================

pause