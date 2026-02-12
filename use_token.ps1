# 使用GitHub令牌配置脚本
param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken
)

Write-Host "正在配置GitHub令牌..." -ForegroundColor Green

# 1. 设置远程URL包含令牌
$remoteUrl = "https://${GitHubToken}@github.com/xiaoling-org/main.git"
git remote set-url origin $remoteUrl

# 2. 测试连接
Write-Host "测试GitHub连接..." -ForegroundColor Yellow
$testResult = git ls-remote 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ GitHub连接成功" -ForegroundColor Green
} else {
    Write-Host "❌ GitHub连接失败" -ForegroundColor Red
    Write-Host $testResult -ForegroundColor Red
    exit 1
}

# 3. 推送代码
Write-Host "正在推送到GitHub..." -ForegroundColor Yellow
git push -u origin main --progress
if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 推送成功！代码已备份到GitHub" -ForegroundColor Green
} else {
    Write-Host "❌ 推送失败，尝试强制推送..." -ForegroundColor Yellow
    git push -u origin main --force
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 强制推送成功" -ForegroundColor Green
    } else {
        Write-Host "❌ 推送失败" -ForegroundColor Red
        exit 1
    }
}

# 4. 验证
Write-Host "验证推送结果..." -ForegroundColor Cyan
git log --oneline -3

Write-Host "`n✅ GitHub备份完成！" -ForegroundColor Green
Write-Host "访问：https://github.com/xiaoling-org/main" -ForegroundColor Cyan