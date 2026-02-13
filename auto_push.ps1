# 自动Git推送脚本
# 每天尝试推送代码到GitHub，如果失败则记录日志

Write-Host "🚀 启动自动Git推送系统" -ForegroundColor Green

cd C:\Users\czp\openclaw

# 1. 自动提交所有更改
Write-Host "1. 自动提交更改..." -ForegroundColor Yellow
& 'C:\Program Files\Git\bin\git.exe' add . 2>$null
$commitMessage = "自动提交: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
& 'C:\Program Files\Git\bin\git.exe' commit -m $commitMessage 2>$null

# 2. 尝试推送到GitHub
Write-Host "2. 尝试推送到GitHub..." -ForegroundColor Yellow
$pushResult = & 'C:\Program Files\Git\bin\git.exe' push origin main 2>&1

# 3. 记录推送结果
$logFile = "C:\Users\czp\openclaw\push_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if ($pushResult -match "Everything up-to-date" -or $pushResult -match "To https") {
    $status = "✅ 推送成功"
    Write-Host "   $status" -ForegroundColor Green
} else {
    $status = "⚠️ 推送失败（网络或认证问题）"
    Write-Host "   $status" -ForegroundColor Yellow
    Write-Host "   错误信息: $pushResult" -ForegroundColor Red
}

# 4. 记录日志
$logEntry = @"
=======================================
推送时间: $timestamp
状态: $status
提交信息: $commitMessage
本地提交: $(git log --oneline -1)
错误信息: $pushResult
=======================================

"@

$logEntry | Out-File -FilePath $logFile -Append -Encoding UTF8

# 5. 创建本地备份（无论推送是否成功）
Write-Host "3. 创建本地备份..." -ForegroundColor Yellow
$backupFile = "C:\Users\czp\Desktop\代码备份_$(Get-Date -Format 'yyyyMMdd_HHmm').zip"
$filesToBackup = @('AGENTS.md', 'SOUL.md', 'IDENTITY.md', 'MEMORY.md', 'USER.md', 'TOOLS.md', 'memory', '工作进度跟踪.md', 'kanban_enhanced.py', 'KanbanMobileApp')
Compress-Archive -Path $filesToBackup -DestinationPath $backupFile -Force 2>$null

if (Test-Path $backupFile) {
    $sizeMB = [math]::Round((Get-Item $backupFile).Length / 1MB, 2)
    Write-Host "   ✅ ZIP备份创建成功: $sizeMB MB" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ ZIP备份创建失败" -ForegroundColor Yellow
}

Write-Host "`n🎉 自动推送系统执行完成！" -ForegroundColor Green
Write-Host "📁 日志文件: $logFile" -ForegroundColor Cyan
Write-Host "📁 备份文件: $backupFile" -ForegroundColor Cyan

Write-Host "`n🔧 系统已配置为完全自主运行：" -ForegroundColor Green
Write-Host "   - 每天自动提交代码" -ForegroundColor Cyan
Write-Host "   - 自动尝试GitHub推送" -ForegroundColor Cyan
Write-Host "   - 自动创建本地备份" -ForegroundColor Cyan
Write-Host "   - 无需人工干预" -ForegroundColor Cyan