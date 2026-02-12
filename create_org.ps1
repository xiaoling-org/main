$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$orgName = "xiaoling-auto-$timestamp"
$body = @{
    login = $orgName
    billing_email = "xiaoling.assistant@gmail.com"
} | ConvertTo-Json -Compress

Write-Host "尝试创建组织: $orgName"
Write-Host "请求体: $body"

# 保存到临时文件
$tempFile = [System.IO.Path]::GetTempFileName() + ".json"
$body | Out-File -FilePath $tempFile -Encoding UTF8

# 使用gh CLI调用API
.\gh-cli\bin\gh.exe api --method POST /user/orgs --input $tempFile

# 清理
Remove-Item $tempFile -ErrorAction SilentlyContinue