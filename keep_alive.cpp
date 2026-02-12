// 保持系统唤醒的C++程序
#include <windows.h>
#include <iostream>
#include <fstream>

void LogMessage(const std::string& message) {
    std::ofstream logFile("C:\\Users\\czp\\keep_alive.log", std::ios::app);
    if (logFile.is_open()) {
        SYSTEMTIME st;
        GetLocalTime(&st);
        logFile << st.wYear << "-" << st.wMonth << "-" << st.wDay << " "
                << st.wHour << ":" << st.wMinute << ":" << st.wSecond << " - "
                << message << std::endl;
        logFile.close();
    }
}

int main() {
    LogMessage("开始保持系统唤醒");
    
    // 设置执行状态，防止系统进入睡眠
    SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED);
    
    // 创建互斥体，防止多个实例运行
    HANDLE hMutex = CreateMutex(NULL, TRUE, L"KeepAliveMutex");
    if (GetLastError() == ERROR_ALREADY_EXISTS) {
        LogMessage("程序已在运行中");
        return 0;
    }
    
    LogMessage("系统唤醒保持已启用");
    
    // 主循环
    while (true) {
        // 每10分钟记录一次状态
        Sleep(600000); // 10分钟
        LogMessage("系统保持唤醒状态");
        
        // 重置执行状态
        SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED);
    }
    
    // 清理
    ReleaseMutex(hMutex);
    CloseHandle(hMutex);
    
    return 0;
}