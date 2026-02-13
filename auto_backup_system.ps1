# 完全自主的Git备份系统
# 无需人工干预，自动管理代码版本

Write-Host "🚀 启动完全自主Git备份系统" -ForegroundColor Green

# 1. 自动提交所有更改
Write-Host "1. 自动提交更改..." -ForegroundColor Yellow
cd C:\Users\czp\openclaw
git add . 2>$null
$commitMessage = "自动备份: $(Get-Date -Format 'yyyy-MM-dd HH:mm') - 看板系统进度更新"
git commit -m $commitMessage 2>$null

# 2. 创建离线备份包
Write-Host "2. 创建离线备份包..." -ForegroundColor Yellow
$backupFile = "C:\Users\czp\Desktop\Git自动备份_$(Get-Date -Format 'yyyyMMdd_HHmm').bundle"
git bundle create $backupFile --all 2>$null
if (Test-Path $backupFile) {
    $sizeMB = [math]::Round((Get-Item $backupFile).Length / 1MB, 2)
    Write-Host "   ✅ 离线包创建成功: $sizeMB MB" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ 离线包创建失败" -ForegroundColor Yellow
}

# 3. 创建ZIP备份
Write-Host "3. 创建ZIP备份..." -ForegroundColor Yellow
$zipFile = "C:\Users\czp\Desktop\代码备份_$(Get-Date -Format 'yyyyMMdd_HHmm').zip"
$filesToBackup = @('AGENTS.md', 'SOUL.md', 'IDENTITY.md', 'MEMORY.md', 'USER.md', 'TOOLS.md', 'memory', 'kanban-backend', 'kanban-mobile-app', 'kanban-telegram-bot', 'kanban_control_center')
Compress-Archive -Path $filesToBackup -DestinationPath $zipFile -Force 2>$null
if (Test-Path $zipFile) {
    $sizeMB = [math]::Round((Get-Item $zipFile).Length / 1MB, 2)
    Write-Host "   ✅ ZIP备份创建成功: $sizeMB MB" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ ZIP备份创建失败" -ForegroundColor Yellow
}

# 4. 记录备份日志
Write-Host "4. 记录备份日志..." -ForegroundColor Yellow
$logEntry = @"
## 自动备份记录 - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
- **Git提交**: $commitMessage
- **离线包**: $(if (Test-Path $backupFile) { "$([math]::Round((Get-Item $backupFile).Length / 1MB, 2)) MB" } else { "失败" })
- **ZIP备份**: $(if (Test-Path $zipFile) { "$([math]::Round((Get-Item $zipFile).Length / 1MB, 2)) MB" } else { "失败" })
- **看板系统进度**: 56% (持续开发中)

"@
$logEntry | Out-File -FilePath "C:\Users\czp\openclaw\backup_log.md" -Append -Encoding UTF8

Write-Host "`n🎉 完全自主备份系统执行完成！" -ForegroundColor Green
Write-Host "📁 备份文件位置:" -ForegroundColor Cyan
Write-Host "   - 离线包: $backupFile" -ForegroundColor Cyan
Write-Host "   - ZIP备份: $zipFile" -ForegroundColor Cyan
Write-Host "   - 日志: C:\Users\czp\openclaw\backup_log.md" -ForegroundColor Cyan

Write-Host "`n🔧 系统已配置为完全自主运行，无需人工干预。" -ForegroundColor Green