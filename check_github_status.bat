@echo off
echo ========================================
echo GitHub仓库状态检查
echo ========================================

echo [1/4] 检查本地Git状态...
"C:\Program Files\Git\bin\git.exe" status
"C:\Program Files\Git\bin\git.exe" log --oneline -5

echo.
echo [2/4] 检查远程连接...
"C:\Program Files\Git\bin\git.exe" remote -v

echo.
echo [3/4] 尝试获取远程信息...
"C:\Program Files\Git\bin\git.exe" fetch origin --dry-run

echo.
echo [4/4] 比较本地和远程...
"C:\Program Files\Git\bin\git.exe" log --oneline origin/main..main 2>nul || echo 无法获取远程分支信息

echo.
echo ========================================
echo 手动检查GitHub仓库：
echo 1. 访问 https://github.com/xiaoling-org/main
echo 2. 查看是否有提交记录
echo 3. 查看文件列表
echo ========================================
echo.
echo 如果GitHub没有最新提交，请运行：
echo git push -f origin main
echo ========================================
pause