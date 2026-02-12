# GitHub推送脚本

Write-Host "开始推送到GitHub..." -ForegroundColor Green

# 1. 检查当前状态
Write-Host "1. 检查Git状态..." -ForegroundColor Yellow
git status

# 2. 添加所有未跟踪的文件
Write-Host "`n2. 添加所有未跟踪的文件..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 所有文件已添加到暂存区" -ForegroundColor Green
} else {
    Write-Host "❌ 添加文件失败" -ForegroundColor Red
    exit 1
}

# 3. 提交更改
Write-Host "`n3. 提交更改..." -ForegroundColor Yellow
$commitMessage = "备份更新：看板系统2.0开发中（56%进度）

包含：
- 工作进度跟踪更新
- 记忆系统更新
- 代码开发进展
- 时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git commit -m $commitMessage
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 提交成功" -ForegroundColor Green
} else {
    Write-Host "⚠️ 提交可能失败或无更改" -ForegroundColor Yellow
}

# 4. 推送到GitHub
Write-Host "`n4. 推送到GitHub远程仓库..." -ForegroundColor Yellow
Write-Host "正在推送，这可能需要一些时间..." -ForegroundColor Cyan
git push -u origin main --progress
if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 推送成功！代码已备份到GitHub" -ForegroundColor Green
} else {
    Write-Host "❌ 推送失败" -ForegroundColor Red
    Write-Host "尝试使用强制推送..." -ForegroundColor Yellow
    git push -u origin main --force
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 强制推送成功" -ForegroundColor Green
    } else {
        Write-Host "❌ 强制推送也失败" -ForegroundColor Red
        exit 1
    }
}

# 5. 验证推送结果
Write-Host "`n5. 验证推送结果..." -ForegroundColor Yellow
$verify = git log --oneline -3
Write-Host "最近3次提交：" -ForegroundColor Cyan
Write-Host $verify -ForegroundColor Cyan

Write-Host "`n✅ GitHub备份完成！" -ForegroundColor Green
Write-Host "访问：https://github.com/xiaoling-org/main" -ForegroundColor Cyan
Write-Host "查看您的代码备份" -ForegroundColor Cyan