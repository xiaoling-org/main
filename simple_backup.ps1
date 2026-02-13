# 简化版自主备份系统
Write-Host "启动自主备份系统..." -ForegroundColor Green

cd C:\Users\czp\openclaw

# 1. Git自动提交
git add . 2>$null
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "自动备份: $date" 2>$null
Write-Host "Git提交完成" -ForegroundColor Green

# 2. 创建备份包
$backupFile = "C:\Users\czp\Desktop\备份_$(Get-Date -Format 'yyyyMMdd_HHmm').bundle"
git bundle create $backupFile --all 2>$null
if (Test-Path $backupFile) {
    $size = [math]::Round((Get-Item $backupFile).Length / 1MB, 2)
    Write-Host "离线包创建成功: $size MB" -ForegroundColor Green
}

# 3. 记录状态
$log = "备份时间: $date`n离线包: $backupFile`n状态: 正常`n"
$log | Out-File -FilePath "C:\Users\czp\openclaw\backup_status.txt" -Encoding UTF8

Write-Host "自主备份完成!" -ForegroundColor Green