# 简单的React Native环境安装脚本

Write-Host "=== React Native环境安装 ===" -ForegroundColor Green

# 1. 检查Node.js
Write-Host "`n1. 检查Node.js..." -ForegroundColor Cyan
node --version
npm --version

# 2. 检查Java
Write-Host "`n2. 检查Java..." -ForegroundColor Cyan
try {
    java --version
    Write-Host "Java已安装" -ForegroundColor Green
} catch {
    Write-Host "Java未安装" -ForegroundColor Red
    Write-Host "请手动安装Java JDK 17或更高版本" -ForegroundColor Yellow
    Write-Host "推荐：Amazon Corretto 17" -ForegroundColor Yellow
    Write-Host "下载：https://corretto.aws/downloads/latest/amazon-corretto-17-x64-windows-jdk.msi" -ForegroundColor Yellow
}

# 3. 安装React Native CLI
Write-Host "`n3. 安装React Native CLI..." -ForegroundColor Cyan
npm install -g react-native-cli

# 4. 设置环境变量
Write-Host "`n4. 设置环境变量..." -ForegroundColor Cyan
Write-Host "设置ANDROID_HOME和ANDROID_SDK_ROOT" -ForegroundColor Yellow

# 创建环境变量设置脚本
$envScript = @'
# 设置React Native环境变量
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "$env:LOCALAPPDATA\Android\Sdk", "User")
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", "$env:LOCALAPPDATA\Android\Sdk", "User")
Write-Host "环境变量已设置" -ForegroundColor Green
'@

Set-Content -Path "set_env_vars.ps1" -Value $envScript

Write-Host "`n=== 安装完成 ===" -ForegroundColor Green
Write-Host "`n下一步操作：" -ForegroundColor Yellow
Write-Host "1. 手动安装Android Studio" -ForegroundColor Yellow
Write-Host "   下载：https://developer.android.com/studio" -ForegroundColor Yellow
Write-Host "2. 安装Android Studio后，运行 set_env_vars.ps1 设置环境变量" -ForegroundColor Yellow
Write-Host "3. 将以下路径添加到PATH：" -ForegroundColor Yellow
Write-Host "   - %ANDROID_HOME%\platform-tools" -ForegroundColor Yellow
Write-Host "   - %ANDROID_HOME%\tools" -ForegroundColor Yellow
Write-Host "   - %ANDROID_HOME%\tools\bin" -ForegroundColor Yellow
Write-Host "4. 创建React Native项目：" -ForegroundColor Yellow
Write-Host "   npx react-native init MyApp" -ForegroundColor Yellow