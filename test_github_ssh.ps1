# GitHub SSH连接测试脚本

Write-Host "测试GitHub SSH连接..." -ForegroundColor Green

# 1. 测试SSH连接
Write-Host "1. 测试SSH连接到GitHub..." -ForegroundColor Yellow
$sshTest = ssh -T git@github.com 2>&1
if ($LASTEXITCODE -eq 1) {
    Write-Host "✅ SSH连接成功！GitHub响应：" -ForegroundColor Green
    Write-Host $sshTest -ForegroundColor Cyan
} else {
    Write-Host "❌ SSH连接失败" -ForegroundColor Red
    Write-Host "错误信息: $sshTest" -ForegroundColor Red
}

# 2. 测试Git远程连接
Write-Host "`n2. 测试Git远程仓库访问..." -ForegroundColor Yellow
$gitRemote = git ls-remote git@github.com:xiaoling-org/main.git 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Git远程仓库访问成功" -ForegroundColor Green
} else {
    Write-Host "❌ Git远程仓库访问失败" -ForegroundColor Red
    Write-Host "错误信息: $gitRemote" -ForegroundColor Red
}

# 3. 切换远程URL到SSH
Write-Host "`n3. 切换Git远程URL到SSH..." -ForegroundColor Yellow
git remote set-url origin git@github.com:xiaoling-org/main.git
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 远程URL已切换到SSH" -ForegroundColor Green
    
    # 验证远程配置
    $remoteConfig = git remote -v
    Write-Host "当前远程配置:" -ForegroundColor Cyan
    Write-Host $remoteConfig -ForegroundColor Cyan
} else {
    Write-Host "❌ 切换远程URL失败" -ForegroundColor Red
}

Write-Host "`n测试完成！" -ForegroundColor Green