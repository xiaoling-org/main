# 设置电脑永不休眠脚本
# 请以管理员身份运行

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "设置电脑永不休眠" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ 请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击 PowerShell -> 以管理员身份运行" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ 管理员权限确认" -ForegroundColor Green
Write-Host ""

# 1. 设置电源选项
Write-Host "正在设置电源选项..." -ForegroundColor Yellow

# 获取当前活动电源方案
$activeScheme = powercfg -getactivescheme
$schemeGuid = ($activeScheme -split ' ')[-1].Trim('()')

Write-Host "当前电源方案: $schemeGuid" -ForegroundColor White

# 设置永不休眠
powercfg -setacvalueindex $schemeGuid SUB_SLEEP SLEEPIDLE 0
powercfg -setdcvalueindex $schemeGuid SUB_SLEEP SLEEPIDLE 0

# 设置显示器永不关闭
powercfg -setacvalueindex $schemeGuid SUB_VIDEO VIDEOIDLE 0
powercfg -setdcvalueindex $schemeGuid SUB_VIDEO VIDEOIDLE 0

# 设置硬盘永不关闭
powercfg -setacvalueindex $schemeGuid SUB_DISK DISKIDLE 0
powercfg -setdcvalueindex $schemeGuid SUB_DISK DISKIDLE 0

# 禁用休眠
powercfg -h off

# 应用更改
powercfg -setactive $schemeGuid

Write-Host "✅ 电源选项设置完成" -ForegroundColor Green
Write-Host ""

# 2. 设置高性能计划（如果存在）
Write-Host "正在设置高性能电源计划..." -ForegroundColor Yellow
$highPerfGuid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"

# 检查高性能计划是否存在
$schemes = powercfg -list
if ($schemes -match $highPerfGuid) {
    powercfg -setactive $highPerfGuid
    Write-Host "✅ 已切换到高性能计划" -ForegroundColor Green
} else {
    Write-Host "⚠️ 高性能计划不存在，使用当前计划" -ForegroundColor Yellow
}

Write-Host ""

# 3. 创建Clawdbot保持在线任务
Write-Host "正在创建Clawdbot保持在线任务..." -ForegroundColor Yellow
try {
    # 删除现有任务（如果存在）
    schtasks /delete /tn "KeepClawdbotAlive" /f 2>$null
    
    # 创建新任务
    $taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>保持Clawdbot网关在线</Description>
    <Author>小灵同学助理</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <TimeTrigger>
      <Repetition>
        <Interval>PT5M</Interval>
      </Repetition>
      <StartBoundary>2026-02-10T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>cmd.exe</Command>
      <Arguments>/c "openclaw-cn gateway start"</Arguments>
    </Exec>
  </Actions>
</Task>
"@

    $tempFile = [System.IO.Path]::GetTempFileName() + ".xml"
    $taskXml | Out-File -FilePath $tempFile -Encoding Unicode
    
    schtasks /create /tn "KeepClawdbotAlive" /xml $tempFile /f
    Remove-Item $tempFile
    
    Write-Host "✅ Clawdbot保持在线任务创建成功" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 创建计划任务失败: $_" -ForegroundColor Yellow
}

Write-Host ""

# 4. 验证设置
Write-Host "验证当前电源设置..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray
powercfg -q $schemeGuid SUB_SLEEP SLEEPIDLE
Write-Host "----------------------------------------" -ForegroundColor Gray
powercfg -q $schemeGuid SUB_VIDEO VIDEOIDLE
Write-Host "----------------------------------------" -ForegroundColor Gray

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 设置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ 电脑将永不休眠" -ForegroundColor Green
Write-Host "✅ 显示器永不关闭" -ForegroundColor Green
Write-Host "✅ Clawdbot保持在线" -ForegroundColor Green
Write-Host ""
Write-Host "小灵同学24小时待命！ 🎯" -ForegroundColor Cyan
Write-Host ""
Write-Host "注意：" -ForegroundColor Yellow
Write-Host "• 这会增加耗电量，建议连接电源时使用" -ForegroundColor White
Write-Host "• 要恢复默认设置，运行: powercfg -restoredefaultschemes" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

pause