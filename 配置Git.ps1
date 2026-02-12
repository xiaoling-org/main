#!/usr/bin/env pwsh
<#
Git配置脚本
用于配置czp1388的Git环境
#>

# 配置信息
$gitUserName = "czp1388"
$gitUserEmail = "1210878296@qq.com"

function Write-Status {
    param([string]$Message, [string]$Type = "INFO")
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $color = @{
        "INFO" = "Green"
        "WARN" = "Yellow"
        "ERROR" = "Red"
        "SUCCESS" = "Cyan"
    }[$Type]
    
    Write-Host "[$timestamp] " -NoNewline
    Write-Host $Message -ForegroundColor $color
}

function Test-GitInstallation {
    Write-Status "测试Git安装..." "INFO"
    
    try {
        $gitVersion = git --version
        if ($gitVersion) {
            Write-Status "Git已安装: $gitVersion" "SUCCESS"
            return $true
        }
    }
    catch {
        Write-Status "Git未安装或不在PATH中" "ERROR"
        return $false
    }
}

function Configure-GitUser {
    param(
        [string]$UserName,
        [string]$UserEmail
    )
    
    Write-Status "配置Git用户信息..." "INFO"
    
    # 设置用户名
    try {
        git config --global user.name $UserName
        Write-Status "设置用户名: $UserName" "SUCCESS"
    }
    catch {
        Write-Status "设置用户名失败: $_" "ERROR"
    }
    
    # 设置邮箱
    try {
        git config --global user.email $UserEmail
        Write-Status "设置邮箱: $UserEmail" "SUCCESS"
    }
    catch {
        Write-Status "设置邮箱失败: $_" "ERROR"
    }
    
    # 设置其他配置
    $configs = @{
        "core.editor" = "code --wait"
        "core.autocrlf" = "true"
        "credential.helper" = "manager"
        "init.defaultBranch" = "main"
        "github.user" = $UserName
        "pull.rebase" = "false"
    }
    
    foreach ($key in $configs.Keys) {
        try {
            git config --global $key $configs[$key]
            Write-Status "设置 $key = $($configs[$key])" "INFO"
        }
        catch {
            Write-Status "设置 $key 失败: $_" "WARN"
        }
    }
}

function Test-GitHubConnection {
    Write-Status "测试GitHub连接..." "INFO"
    
    $testRepos = @(
        "https://github.com/czp1388/LotteryAnalysisTool.git",
        "https://github.com/czp1388/OmniMarket-Financial-Monitor.git"
    )
    
    foreach ($repo in $testRepos) {
        Write-Status "测试仓库: $repo" "INFO"
        
        try {
            # 只测试连接，不克隆
            $result = git ls-remote $repo --heads 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Status "  连接成功" "SUCCESS"
            }
            else {
                Write-Status "  连接失败: $result" "ERROR"
            }
        }
        catch {
            Write-Status "  测试异常: $_" "ERROR"
        }
    }
}

function Show-GitConfig {
    Write-Status "显示Git配置..." "INFO"
    
    try {
        $config = git config --list
        Write-Status "当前Git配置:" "INFO"
        $config | ForEach-Object { Write-Host "  $_" }
    }
    catch {
        Write-Status "获取配置失败: $_" "ERROR"
    }
}

function Create-ProjectStructure {
    Write-Status "创建项目目录结构..." "INFO"
    
    $baseDir = "C:\Users\czp\openclaw\projects\github"
    $projects = @(
        "LotteryAnalysisTool",
        "OmniMarket-Financial-Monitor"
    )
    
    # 创建基础目录
    if (-not (Test-Path $baseDir)) {
        try {
            New-Item -Path $baseDir -ItemType Directory -Force | Out-Null
            Write-Status "创建目录: $baseDir" "SUCCESS"
        }
        catch {
            Write-Status "创建目录失败: $_" "ERROR"
            return
        }
    }
    
    # 创建项目目录
    foreach ($project in $projects) {
        $projectDir = Join-Path $baseDir $project
        if (-not (Test-Path $projectDir)) {
            try {
                New-Item -Path $projectDir -ItemType Directory -Force | Out-Null
                Write-Status "创建项目目录: $project" "SUCCESS"
            }
            catch {
                Write-Status "创建项目目录失败 ($project): $_" "WARN"
            }
        }
        else {
            Write-Status "项目目录已存在: $project" "INFO"
        }
    }
}

function Main {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Git配置脚本 - czp1388" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # 1. 测试Git安装
    if (-not (Test-GitInstallation)) {
        Write-Status "请先安装Git" "ERROR"
        return
    }
    
    # 2. 配置用户信息
    Configure-GitUser -UserName $gitUserName -UserEmail $gitUserEmail
    
    # 3. 显示配置
    Show-GitConfig
    
    # 4. 测试连接
    Test-GitHubConnection
    
    # 5. 创建目录结构
    Create-ProjectStructure
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "配置完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "下一步建议:" -ForegroundColor Yellow
    Write-Host "1. 克隆现有仓库到项目目录" -ForegroundColor White
    Write-Host "2. 分析项目结构和需求" -ForegroundColor White
    Write-Host "3. 开始开发或维护工作" -ForegroundColor White
}

# 运行主函数
Main