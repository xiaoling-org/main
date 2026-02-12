@echo off
echo ========================================
echo 创建系统级唤醒服务
echo ========================================
echo.

:: 创建服务脚本
echo Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2") > "C:\Users\czp\openclaw\wake_service.vbs"
echo Set objStartup = objWMIService.Get("Win32_ProcessStartup") >> "C:\Users\czp\openclaw\wake_service.vbs"
echo Set objConfig = objStartup.SpawnInstance_ >> "C:\Users\czp\openclaw\wake_service.vbs"
echo objConfig.ShowWindow = 0 >> "C:\Users\czp\openclaw\wake_service.vbs"
echo Set objProcess = GetObject("winmgmts:root\cimv2:Win32_Process") >> "C:\Users\czp\openclaw\wake_service.vbs"
echo objProcess.Create "powershell.exe -WindowStyle Hidden -Command `"while($true){Add-Type -TypeDefinition '[DllImport(\`"kernel32.dll\`")]public static extern uint SetThreadExecutionState(uint esFlags);' -Name Sys -Namespace Win; [Win.Sys]::SetThreadExecutionState(0x80000003); Start-Sleep -Seconds 300}`"", Null, objConfig, intProcessID >> "C:\Users\czp\openclaw\wake_service.vbs"

:: 运行服务脚本
echo 正在启动唤醒服务...
cscript //nologo "C:\Users\czp\openclaw\wake_service.vbs"

echo.
echo ✅ 唤醒服务已启动
echo.
echo 电脑将永不休眠！
echo 小灵同学24小时待命！ 🎯
echo ========================================

pause