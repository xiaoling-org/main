@echo off
echo ========================================
echo 小灵同学即时备份系统
echo 备份时间: %date% %time%
echo ========================================

echo [1/4] 切换到工作目录...
cd /d "C:\Users\czp\openclaw"

echo [2/4] 检查Git状态...
"C:\Program Files\Git\bin\git.exe" status

echo [3/4] 添加所有更改...
"C:\Program Files\Git\bin\git.exe" add .

echo [4/4] 提交并推送到GitHub...
"C:\Program Files\Git\bin\git.exe" commit -m "即时备份: %date% %time%" || echo 无更改可提交
"C:\Program Files\Git\bin\git.exe" push origin main

echo ========================================
echo 备份完成！
echo ========================================
pause