' 保持电脑唤醒的VBS脚本
' 这个脚本会阻止电脑进入睡眠模式

Set WshShell = CreateObject("WScript.Shell")

Do While True
    ' 模拟按键防止休眠
    WshShell.SendKeys "{SCROLLLOCK}"
    WshShell.SendKeys "{SCROLLLOCK}"
    
    ' 每5分钟执行一次
    WScript.Sleep 300000 ' 300000毫秒 = 5分钟
    
    ' 记录日志
    LogMessage "保持唤醒状态 - " & Now()
Loop

Sub LogMessage(msg)
    On Error Resume Next
    Dim fso, logFile
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set logFile = fso.OpenTextFile("C:\Users\czp\keep_awake.log", 8, True) ' 8 = 追加模式
    logFile.WriteLine msg
    logFile.Close
End Sub