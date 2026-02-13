# 小灵同学看板系统 - PowerShell启动脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   小灵同学看板系统 - 一键启动" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ 检测到Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未检测到Python，请先安装Python 3.8+" -ForegroundColor Red
    Write-Host "下载地址：https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 检查依赖文件
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ 未找到依赖文件 requirements.txt" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

# 安装依赖
Write-Host "📦 正在检查Python依赖..." -ForegroundColor Cyan
try {
    pip install -r requirements.txt --quiet
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} catch {
    Write-Host "⚠️  依赖安装失败，尝试使用国内镜像..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
        Write-Host "✅ 依赖安装完成（使用镜像）" -ForegroundColor Green
    } catch {
        Write-Host "❌ 依赖安装失败，请手动安装" -ForegroundColor Red
        Write-Host "手动安装命令: pip install -r requirements.txt" -ForegroundColor Yellow
    }
}

# 获取本机IP地址
$ipAddress = ""
try {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" | Where-Object {$_.PrefixOrigin -eq "Dhcp"}).IPAddress
    if (-not $ipAddress) {
        $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"}).IPAddress | Select-Object -First 1
    }
} catch {
    $ipAddress = "192.168.x.x"
}

# 显示访问信息
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   访问地址：" -ForegroundColor Yellow
Write-Host "   电脑：http://localhost:5000" -ForegroundColor Green
Write-Host "   手机：http://$ipAddress`:5000" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 请确保手机和电脑在同一WiFi网络" -ForegroundColor Cyan
Write-Host "⏳ 按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动服务器
try {
    python kanban_enhanced.py
} catch {
    Write-Host "❌ 服务器启动失败: $_" -ForegroundColor Red
    Read-Host "按Enter键退出"
}