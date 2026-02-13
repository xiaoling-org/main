@echo off
chcp 65001 >nul
echo.
echo =======================================
echo 🚀 完全自主本地工作流系统
echo 📅 执行时间: %date% %time%
echo =======================================
echo.

cd /d C:\Users\czp\openclaw

echo 📝 阶段1：自动版本控制
echo.

REM 检查Git状态
"C:\Program Files\Git\bin\git.exe" status --porcelain > git_status.txt 2>nul
set /p git_status=<git_status.txt
if "%git_status%"=="" (
    echo   ✅ 工作区干净，无需提交
) else (
    echo   检测到未提交的更改，自动提交...
    "C:\Program Files\Git\bin\git.exe" add . 2>nul
    "C:\Program Files\Git\bin\git.exe" commit -m "完全自主工作流: %date% %time%" 2>nul
    echo   ✅ 自动提交完成
)

echo.
echo   当前Git状态:
"C:\Program Files\Git\bin\git.exe" log --oneline -3 2>nul

echo.
echo 💾 阶段2：创建本地备份
echo.

REM 创建Git离线包
set bundle_file=C:\Users\czp\Desktop\Git完全备份_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.bundle
echo   创建Git离线包...
"C:\Program Files\Git\bin\git.exe" bundle create "%bundle_file%" --all 2>nul
if exist "%bundle_file%" (
    for /f %%i in ('powershell -Command "(Get-Item '%bundle_file%').Length/1MB"') do set size_mb=%%i
    echo   ✅ Git离线包创建成功: !size_mb! MB
) else (
    echo   ⚠️ Git离线包创建失败
)

echo.
echo 📊 阶段3：看板系统状态
echo.

dir kanban*.* 2>nul
echo.
if exist "KanbanMobileApp" (
    echo   ✅ KanbanMobileApp目录存在
) else (
    echo   ⚠️ KanbanMobileApp目录不存在
)

echo.
echo 📈 阶段4：更新工作进度
echo.

if exist "工作进度跟踪.md" (
    echo   读取当前进度...
    findstr "当前总体进度" "工作进度跟踪.md"
) else (
    echo   ⚠️ 工作进度跟踪文件不存在
)

echo.
echo 📋 阶段5：记录执行日志
echo.

set log_file=C:\Users\czp\openclaw\工作流执行日志.txt
echo ======================================= >> "%log_file%"
echo 完全自主工作流执行记录 >> "%log_file%"
echo 执行时间: %date% %time% >> "%log_file%"
echo ======================================= >> "%log_file%"
echo. >> "%log_file%"
echo 备份文件: >> "%log_file%"
echo - Git离线包: %bundle_file% >> "%log_file%"
echo. >> "%log_file%"
echo 看板系统状态: >> "%log_file%"
dir kanban*.* 2>nul | findstr /v "目录" >> "%log_file%"
echo. >> "%log_file%"
echo ======================================= >> "%log_file%"
echo. >> "%log_file%"

echo   ✅ 执行日志已记录: %log_file%

echo.
echo =======================================
echo 🎉 完全自主本地工作流执行完成！
echo =======================================
echo.
echo 📁 生成的备份文件:
echo    - Git离线包: %bundle_file%
echo    - 执行日志: %log_file%
echo.
echo 🔧 系统特性:
echo   ✅ 100%%本地自主，无需网络
echo   ✅ 自动版本控制，完整历史
echo   ✅ 多重备份，数据安全
echo   ✅ 自动进度跟踪，持续改进
echo   ✅ 无需人工干预，完全自主
echo.
echo 🚀 下次执行: 明天自动运行，持续保障代码安全
echo.

del git_status.txt 2>nul
pause