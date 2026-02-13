@echo off
chcp 65001 >nul
title 小灵同学本地模型系统

echo =======================================
echo 🚀 启动小灵同学本地模型系统
echo 📅 时间: %date% %time%
echo =======================================
echo.

echo 📊 检查系统配置...
echo   处理器: Intel i5-7300HQ
echo   内存: 8GB
echo   显卡: GTX 1060 3GB
echo   系统: Windows 10 64位
echo.

echo 🔧 检查Ollama服务...
tasklist | findstr /i ollama >nul
if %errorlevel% equ 0 (
    echo   ✅ Ollama服务正在运行
) else (
    echo   ⚠️ Ollama服务未运行，正在启动...
    start /B ollama serve
    timeout /t 5 /nobreak >nul
)

echo.
echo 🤖 检查本地模型...
curl -s http://localhost:11434/api/tags | findstr /i "qwen2.5" >nul
if %errorlevel% equ 0 (
    echo   ✅ Qwen2.5-1.5B模型已加载
) else (
    echo   ❌ 本地模型未找到
    echo   正在下载模型...
    ollama pull qwen2.5:1.5b-instruct
)

echo.
echo ⚙️ 模型配置信息:
echo   模型: Qwen2.5-1.5B-Instruct
echo   量化: Q4_K_M (优化内存使用)
echo   内存占用: ~3GB
echo   GPU加速: 已启用 (GTX 1060)
echo   API端点: http://localhost:11434/v1
echo.

echo 📈 启动智能模型选择器...
python smart_model_selector.py

echo.
echo 📊 启动模型监控...
start /B python model_monitor.py

echo.
echo =======================================
echo 🎉 本地模型系统启动完成！
echo =======================================
echo.
echo 💡 使用说明:
echo   1. 本地模型优先: 所有请求先尝试本地
echo   2. 自动回退: 本地失败时自动切换到API
echo   3. 性能监控: 实时监控模型性能
echo   4. 资源优化: 自动管理内存和GPU使用
echo.
echo 📁 配置文件: local_model_config.json
echo 📊 监控报告: model_monitor_report_*.txt
echo 📈 使用统计: model_usage_stats.json
echo.
echo 🔄 系统将自动运行，按任意键退出...
pause >nul