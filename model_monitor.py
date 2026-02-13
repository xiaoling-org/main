#!/usr/bin/env python3
"""
模型使用监控系统
监控本地模型性能，自动记录使用统计
"""

import json
import time
import psutil
import logging
from datetime import datetime
from typing import Dict, Any, List
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelMonitor:
    """模型性能监控器"""
    
    def __init__(self):
        self.stats_file = "model_usage_stats.json"
        self.stats = self.load_stats()
        
    def load_stats(self) -> Dict[str, Any]:
        """加载统计信息"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "total_requests": 0,
                "local_success": 0,
                "local_failed": 0,
                "api_fallback": 0,
                "avg_response_time": 0,
                "daily_stats": {},
                "model_performance": {}
            }
    
    def save_stats(self):
        """保存统计信息"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def record_request(self, model_type: str, success: bool, response_time: float):
        """记录请求统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 初始化今日统计
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {
                "local_requests": 0,
                "local_success": 0,
                "api_requests": 0,
                "api_success": 0,
                "total_response_time": 0,
                "request_count": 0
            }
        
        # 更新总体统计
        self.stats["total_requests"] += 1
        
        if model_type == "local":
            self.stats["daily_stats"][today]["local_requests"] += 1
            if success:
                self.stats["local_success"] += 1
                self.stats["daily_stats"][today]["local_success"] += 1
            else:
                self.stats["local_failed"] += 1
        else:  # api
            self.stats["daily_stats"][today]["api_requests"] += 1
            self.stats["api_fallback"] += 1
            if success:
                self.stats["daily_stats"][today]["api_success"] += 1
        
        # 更新响应时间统计
        self.stats["daily_stats"][today]["total_response_time"] += response_time
        self.stats["daily_stats"][today]["request_count"] += 1
        
        # 计算平均响应时间
        total_time = sum(day["total_response_time"] for day in self.stats["daily_stats"].values())
        total_count = sum(day["request_count"] for day in self.stats["daily_stats"].values())
        if total_count > 0:
            self.stats["avg_response_time"] = total_time / total_count
        
        self.save_stats()
    
    def check_system_resources(self) -> Dict[str, Any]:
        """检查系统资源"""
        resources = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_mb": psutil.virtual_memory().available / (1024 * 1024),
            "disk_usage": psutil.disk_usage('C:').percent
        }
        
        # 检查Ollama进程
        ollama_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                if 'ollama' in proc.info['name'].lower():
                    ollama_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        resources["ollama_processes"] = ollama_processes
        resources["ollama_count"] = len(ollama_processes)
        
        return resources
    
    def check_local_model_health(self) -> Dict[str, Any]:
        """检查本地模型健康状态"""
        health = {
            "timestamp": datetime.now().isoformat(),
            "available": False,
            "response_time": 0,
            "error": None
        }
        
        try:
            start_time = time.time()
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )
            health["response_time"] = (time.time() - start_time) * 1000  # 毫秒
            
            if response.status_code == 200:
                health["available"] = True
                models = response.json().get("models", [])
                health["model_count"] = len(models)
                if models:
                    health["primary_model"] = models[0].get("name")
            else:
                health["error"] = f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            health["error"] = "请求超时"
        except requests.exceptions.ConnectionError:
            health["error"] = "连接失败"
        except Exception as e:
            health["error"] = str(e)
        
        return health
    
    def generate_report(self) -> str:
        """生成监控报告"""
        resources = self.check_system_resources()
        health = self.check_local_model_health()
        
        report = f"""
📊 模型监控报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=======================================

📈 使用统计:
   总请求数: {self.stats['total_requests']}
   本地成功: {self.stats['local_success']}
   本地失败: {self.stats['local_failed']}
   API回退: {self.stats['api_fallback']}
   平均响应时间: {self.stats['avg_response_time']:.2f}ms

💻 系统资源:
   CPU使用率: {resources['cpu_percent']}%
   内存使用率: {resources['memory_percent']}%
   可用内存: {resources['memory_available_mb']:.1f} MB
   磁盘使用率: {resources['disk_usage']}%
   Ollama进程数: {resources['ollama_count']}

🔧 本地模型健康:
   可用状态: {'✅ 正常' if health['available'] else '❌ 异常'}
   响应时间: {health['response_time']:.1f}ms
   {f"错误信息: {health['error']}" if health.get('error') else "✅ 无错误"}

📅 今日统计 ({datetime.now().strftime('%Y-%m-%d')}):
   本地请求: {self.stats['daily_stats'].get(datetime.now().strftime('%Y-%m-%d'), {}).get('local_requests', 0)}
   本地成功: {self.stats['daily_stats'].get(datetime.now().strftime('%Y-%m-%d'), {}).get('local_success', 0)}
   API请求: {self.stats['daily_stats'].get(datetime.now().strftime('%Y-%m-%d'), {}).get('api_requests', 0)}
   API成功: {self.stats['daily_stats'].get(datetime.now().strftime('%Y-%m-%d'), {}).get('api_success', 0)}

💡 建议:
   {self.generate_suggestions(resources, health)}
=======================================
"""
        return report
    
    def generate_suggestions(self, resources: Dict, health: Dict) -> str:
        """生成优化建议"""
        suggestions = []
        
        # 内存建议
        if resources['memory_percent'] > 80:
            suggestions.append("内存使用率较高，考虑关闭不必要的程序")
        elif resources['memory_available_mb'] < 1024:  # 少于1GB
            suggestions.append("可用内存较少，模型性能可能受影响")
        
        # CPU建议
        if resources['cpu_percent'] > 80:
            suggestions.append("CPU使用率较高，模型响应可能变慢")
        
        # 模型健康建议
        if not health['available']:
            suggestions.append("本地模型不可用，检查Ollama服务是否运行")
        elif health['response_time'] > 1000:  # 1秒以上
            suggestions.append("模型响应时间较长，考虑优化或使用API")
        
        # Ollama进程建议
        if resources['ollama_count'] == 0:
            suggestions.append("未检测到Ollama进程，需要启动服务")
        elif resources['ollama_count'] > 1:
            suggestions.append("检测到多个Ollama进程，可能造成资源冲突")
        
        if not suggestions:
            suggestions.append("系统状态良好，继续使用本地模型")
        
        return " | ".join(suggestions)
    
    def monitor_loop(self, interval_seconds: int = 300):
        """监控循环（每5分钟检查一次）"""
        logger.info(f"🚀 启动模型监控系统，检查间隔: {interval_seconds}秒")
        
        try:
            while True:
                try:
                    report = self.generate_report()
                    logger.info(f"📊 监控报告生成完成")
                    
                    # 保存报告到文件
                    report_file = f"model_monitor_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    logger.info(f"📁 报告已保存: {report_file}")
                    
                except Exception as e:
                    logger.error(f"监控循环错误: {e}")
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("监控系统已停止")

def test_monitor():
    """测试监控系统"""
    print("🧪 测试模型监控系统...")
    
    monitor = ModelMonitor()
    
    # 测试资源检查
    print("💻 检查系统资源...")
    resources = monitor.check_system_resources()
    print(f"   CPU: {resources['cpu_percent']}%")
    print(f"   内存: {resources['memory_percent']}%")
    print(f"   可用内存: {resources['memory_available_mb']:.1f} MB")
    
    # 测试模型健康检查
    print("🔧 检查本地模型健康...")
    health = monitor.check_local_model_health()
    print(f"   可用: {health['available']}")
    print(f"   响应时间: {health['response_time']:.1f}ms")
    if health.get('error'):
        print(f"   错误: {health['error']}")
    
    # 生成报告
    print("📊 生成监控报告...")
    report = monitor.generate_report()
    print(report)
    
    return monitor

if __name__ == "__main__":
    monitor = test_monitor()
    print("\n🎉 模型监控系统测试完成！")
    
    # 启动监控循环（测试模式，只运行一次）
    # monitor.monitor_loop(interval_seconds=10)