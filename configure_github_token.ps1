# GitHub令牌配置脚本
# 使用方法：.\configure_github_token.ps1 -Token "您的GitHub令牌"

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

Write-Host "正在配置GitHub令牌..." -ForegroundColor Green

# 1. 配置Git使用令牌
$gitConfig = @"
[credential]
    helper = store
"@

# 写入Git配置
$gitConfig | Out-File -FilePath "$env:USERPROFILE\.gitconfig" -Append -Encoding UTF8

# 2. 创建凭据文件
$credentialUrl = "https://${Token}:x-oauth-basic@github.com"
$credentialContent = $credentialUrl

# 存储凭据（Windows凭据管理器方式）
cmdkey /generic:git:https://github.com /user:$Token /pass

Write-Host "✅ Git配置已更新" -ForegroundColor Green

# 3. 测试连接
Write-Host "测试GitHub连接..." -ForegroundColor Yellow
try {
    $result = git ls-remote https://github.com/xiaoling-org/main.git 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ GitHub连接测试成功" -ForegroundColor Green
    } else {
        Write-Host "❌ GitHub连接测试失败" -ForegroundColor Red
        Write-Host "错误信息: $result" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 测试过程中出错: $_" -ForegroundColor Red
}

Write-Host "`n配置完成！" -ForegroundColor Green
Write-Host "现在可以运行: git push -u origin main" -ForegroundColor Cyan