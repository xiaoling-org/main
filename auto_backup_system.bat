@echo off
echo ========================================
echo 小灵同学自动备份系统 v1.0
echo 备份时间: %date% %time%
echo ========================================

REM 切换到工作目录
cd /d "C:\Users\czp\openclaw"

REM 检查Git状态
echo [1/5] 检查Git状态...
"C:\Program Files\Git\bin\git.exe" status

REM 添加所有更改
echo [2/5] 添加所有更改...
"C:\Program Files\Git\bin\git.exe" add .

REM 提交更改
echo [3/5] 提交更改...
"C:\Program Files\Git\bin\git.exe" commit -m "自动备份: %date% %time%" || echo 无更改可提交

REM 尝试推送到GitHub
echo [4/5] 尝试推送到GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

if %errorlevel% equ 0 (
    echo [5/5] ✅ 备份成功！已推送到GitHub
) else (
    echo [5/5] ⚠️ GitHub推送失败，创建本地备份...
    
    REM 创建本地备份
    set BACKUP_DIR="C:\Users\czp\Desktop\小灵同学本地备份"
    if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%
    
    set BACKUP_FILE="小灵同学备份_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.zip"
    powershell -Command "Compress-Archive -Path 'C:\Users\czp\openclaw\*' -DestinationPath '%BACKUP_DIR%\%BACKUP_FILE%' -Force"
    
    echo ✅ 本地备份已创建: %BACKUP_DIR%\%BACKUP_FILE%
)

echo ========================================
echo 备份完成！
echo ========================================
pause