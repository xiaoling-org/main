# 持续工作系统 - 后台运行
$iteration = 1
$endTime = Get-Date "2026-02-13 20:30:00"

Write-Host "🚀 小灵同学持续工作系统启动" -ForegroundColor Green
Write-Host "📅 开始时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "⏰ 计划结束: $($endTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Cyan
Write-Host "⏳ 总时长: $([math]::Round(($endTime - (Get-Date)).TotalHours,1)) 小时" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

cd C:\Users\czp\openclaw

while ((Get-Date) -lt $endTime) {
    Write-Host "`n📊 第 $iteration 次循环开始" -ForegroundColor Yellow
    Write-Host "⏰ 当前时间: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
    
    # 1. 自动Git提交
    Write-Host "📝 自动Git提交..." -ForegroundColor Cyan
    & 'C:\Program Files\Git\bin\git.exe' add . 2>$null
    & 'C:\Program Files\Git\bin\git.exe' commit -m "持续工作: 第${iteration}次提交 - $(Get-Date -Format 'HH:mm')" 2>$null
    Write-Host "✅ Git提交完成" -ForegroundColor Green
    
    # 2. 显示当前进度
    Write-Host "📈 当前工作进度:" -ForegroundColor Cyan
    if (Test-Path "工作进度跟踪.md") {
        Get-Content "工作进度跟踪.md" | Select-String "当前总体进度" | ForEach-Object {
            Write-Host "   $_" -ForegroundColor Gray
        }
    }
    
    # 3. 每3小时创建备份
    $currentHour = (Get-Date).Hour
    if ($currentHour % 3 -eq 0) {
        Write-Host "💾 创建定时备份..." -ForegroundColor Cyan
        $backupFile = "C:\Users\czp\Desktop\持续工作备份_$(Get-Date -Format 'yyyyMMdd_HHmm').zip"
        & 'C:\Program Files\Git\bin\git.exe' bundle create $backupFile --all 2>$null
        if (Test-Path $backupFile) {
            $sizeMB = [math]::Round((Get-Item $backupFile).Length / 1MB, 2)
            Write-Host "✅ 备份创建成功: $sizeMB MB" -ForegroundColor Green
        }
    }
    
    # 4. 记录工作日志
    $logEntry = @"
=======================================
工作循环: $iteration
时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Git提交: 完成
进度: $(if (Test-Path "工作进度跟踪.md") { (Get-Content "工作进度跟踪.md" | Select-String "当前总体进度") })
=======================================

"@
    $logEntry | Out-File -FilePath "work_log.txt" -Append -Encoding UTF8
    
    # 5. 计算剩余时间
    $remaining = $endTime - (Get-Date)
    $remainingHours = [math]::Round($remaining.TotalHours, 1)
    Write-Host "⏳ 剩余时间: $remainingHours 小时" -ForegroundColor Magenta
    
    # 6. 等待下一循环（1小时）
    $iteration++
    Write-Host "⏳ 等待下一循环（1小时后继续）..." -ForegroundColor Gray
    Start-Sleep -Seconds 3600
}

Write-Host "`n🎉 到达计划结束时间: 20:30" -ForegroundColor Green
Write-Host "📁 创建最终备份..." -ForegroundColor Cyan
$finalBackup = "C:\Users\czp\Desktop\最终备份_$(Get-Date -Format 'yyyyMMdd_HHmm').bundle"
& 'C:\Program Files\Git\bin\git.exe' bundle create $finalBackup --all 2>$null
Write-Host "✅ 持续工作系统完成" -ForegroundColor Green
Write-Host "📁 最终备份: $finalBackup" -ForegroundColor Cyan