"""
智能休息系统 - Telegram控制模块
可以通过Telegram远程控制电脑休息时间
"""

import os
import json
import time
import schedule
import threading
from datetime import datetime, timedelta
import subprocess
import configparser

# 配置路径
CONFIG_DIR = "C:\\SmartRest"
CONFIG_FILE = os.path.join(CONFIG_DIR, "telegram_config.ini")
SCHEDULE_FILE = os.path.join(CONFIG_DIR, "rest_schedule.json")
LOG_FILE = os.path.join(CONFIG_DIR, "Logs", "telegram_control.log")

# 确保目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(os.path.join(CONFIG_DIR, "Logs"), exist_ok=True)

def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except:
        pass
    
    print(log_entry.strip())

def load_config():
    """加载配置"""
    config = configparser.ConfigParser()
    
    # 默认配置
    default_config = {
        'Telegram': {
            'bot_token': 'YOUR_BOT_TOKEN_HERE',
            'chat_id': 'YOUR_CHAT_ID_HERE',
            'enabled': '0'
        },
        'RestSchedule': {
            'default_time': '03:00',
            'default_duration': '60',
            'auto_restart': '1'
        }
    }
    
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding='utf-8')
    else:
        config.read_dict(default_config)
        save_config(config)
    
    return config

def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)

def load_schedule():
    """加载休息时间表"""
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    
    # 默认时间表
    default_schedule = {
        "daily": [
            {"time": "03:00", "duration": 60, "restart": True, "enabled": True}
        ],
        "weekly": [
            {"day": 0, "time": "04:00", "duration": 120, "restart": True, "enabled": True}  # 周日
        ],
        "custom": []
    }
    
    save_schedule(default_schedule)
    return default_schedule

def save_schedule(schedule_data):
    """保存时间表"""
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule_data, f, indent=2, ensure_ascii=False)

def start_rest(duration_minutes=60, restart=True):
    """开始休息"""
    log_message(f"开始电脑休息，时长：{duration_minutes}分钟，重启：{restart}")
    
    # 1. 停止Clawdbot服务
    try:
        log_message("正在停止Clawdbot服务...")
        subprocess.run(["openclaw-cn", "gateway", "stop"], 
                      capture_output=True, text=True, timeout=10)
        time.sleep(5)
    except Exception as e:
        log_message(f"停止服务时出错：{str(e)}")
    
    # 2. 进入睡眠模式（如果支持）
    try:
        log_message("电脑进入睡眠模式...")
        # 使用Windows睡眠命令
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], 
                      capture_output=True, timeout=5)
    except:
        log_message("睡眠模式不可用，等待指定时间")
        # 如果睡眠不可用，只是等待
        time.sleep(duration_minutes * 60)
    
    # 3. 如果设置了重启，则重启电脑
    if restart:
        log_message(f"休息结束，准备重启电脑...")
        time.sleep(10)  # 给系统一些时间
        
        try:
            subprocess.run(["shutdown", "/r", "/t", "30", "/c", "智能休息系统：电脑休息结束，正在重启..."], 
                          capture_output=True, timeout=5)
        except Exception as e:
            log_message(f"重启命令失败：{str(e)}")

def schedule_daily_rest(rest_time, duration, restart):
    """安排每日休息"""
    def job():
        start_rest(duration, restart)
    
    schedule.every().day.at(rest_time).do(job)
    log_message(f"已安排每日休息：{rest_time}，时长：{duration}分钟")

def schedule_weekly_rest(day, rest_time, duration, restart):
    """安排每周休息"""
    def job():
        start_rest(duration, restart)
    
    # 映射星期几
    days = {
        0: schedule.every().sunday,
        1: schedule.every().monday,
        2: schedule.every().tuesday,
        3: schedule.every().wednesday,
        4: schedule.every().thursday,
        5: schedule.every().friday,
        6: schedule.every().saturday
    }
    
    if day in days:
        days[day].at(rest_time).do(job)
        log_message(f"已安排每周休息：星期{day} {rest_time}，时长：{duration}分钟")

def update_rest_schedule(new_schedule):
    """更新休息时间表"""
    try:
        save_schedule(new_schedule)
        
        # 清除现有计划
        schedule.clear()
        
        # 重新安排每日休息
        for daily in new_schedule.get("daily", []):
            if daily.get("enabled", False):
                schedule_daily_rest(
                    daily["time"],
                    daily["duration"],
                    daily.get("restart", True)
                )
        
        # 重新安排每周休息
        for weekly in new_schedule.get("weekly", []):
            if weekly.get("enabled", False):
                schedule_weekly_rest(
                    weekly["day"],
                    weekly["time"],
                    weekly["duration"],
                    weekly.get("restart", True)
                )
        
        log_message("休息时间表已更新")
        return True
    except Exception as e:
        log_message(f"更新时间表时出错：{str(e)}")
        return False

def get_schedule_status():
    """获取当前时间表状态"""
    schedule_data = load_schedule()
    status = {
        "daily_schedule": [],
        "weekly_schedule": [],
        "next_rest": None
    }
    
    # 获取每日计划
    for daily in schedule_data.get("daily", []):
        if daily.get("enabled", False):
            status["daily_schedule"].append({
                "time": daily["time"],
                "duration": daily["duration"],
                "restart": daily.get("restart", True)
            })
    
    # 获取每周计划
    for weekly in schedule_data.get("weekly", []):
        if weekly.get("enabled", False):
            day_names = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
            status["weekly_schedule"].append({
                "day": day_names[weekly["day"]],
                "time": weekly["time"],
                "duration": weekly["duration"],
                "restart": weekly.get("restart", True)
            })
    
    return status

def format_schedule_message():
    """格式化时间表消息"""
    status = get_schedule_status()
    
    message = "📅 当前休息时间表：\n\n"
    
    if status["daily_schedule"]:
        message += "🕐 每日休息：\n"
        for sched in status["daily_schedule"]:
            message += f"  • {sched['time']} - {sched['duration']}分钟"
            if sched['restart']:
                message += " (重启)"
            message += "\n"
        message += "\n"
    
    if status["weekly_schedule"]:
        message += "📆 每周休息：\n"
        for sched in status["weekly_schedule"]:
            message += f"  • {sched['day']} {sched['time']} - {sched['duration']}分钟"
            if sched['restart']:
                message += " (重启)"
            message += "\n"
        message += "\n"
    
    if not status["daily_schedule"] and not status["weekly_schedule"]:
        message += "⚠️ 当前没有安排休息时间\n\n"
    
    message += "💡 命令：\n"
    message += "/setschedule - 设置休息时间\n"
    message += "/restnow - 立即休息\n"
    message += "/status - 查看状态\n"
    message += "/help - 帮助信息\n"
    
    return message

def schedule_worker():
    """计划任务工作线程"""
    log_message("计划任务工作线程启动")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
        except Exception as e:
            log_message(f"计划任务出错：{str(e)}")
            time.sleep(300)  # 出错后等待5分钟

def main():
    """主函数"""
    log_message("智能休息系统启动")
    
    # 加载配置
    config = load_config()
    schedule_data = load_schedule()
    
    # 初始化计划任务
    update_rest_schedule(schedule_data)
    
    # 启动计划任务线程
    worker_thread = threading.Thread(target=schedule_worker, daemon=True)
    worker_thread.start()
    
    log_message("系统已启动，按 Ctrl+C 停止")
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(3600)  # 每小时检查一次
    except KeyboardInterrupt:
        log_message("系统停止")
    except Exception as e:
        log_message(f"系统异常：{str(e)}")

if __name__ == "__main__":
    main()