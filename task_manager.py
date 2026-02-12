#!/usr/bin/env python3
"""
小灵同学助理 - 任务管理系统
用于管理看板任务和自动化更新
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re

class TaskManager:
    def __init__(self, kanban_path="KANBAN.md", tasks_path="tasks.json"):
        self.kanban_path = Path(kanban_path)
        self.tasks_path = Path(tasks_path)
        self.tasks = self.load_tasks()
        
    def load_tasks(self):
        """加载任务数据"""
        if self.tasks_path.exists():
            with open(self.tasks_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "tasks": [],
            "next_id": 1,
            "stats": {
                "total": 0,
                "todo": 0,
                "in_progress": 0,
                "done": 0,
                "ideas": 0
            }
        }
    
    def save_tasks(self):
        """保存任务数据"""
        with open(self.tasks_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def create_task(self, description, priority="中", category="工作", due_date=None):
        """创建新任务"""
        task_id = f"KB-{self.tasks['next_id']:03d}"
        
        task = {
            "id": task_id,
            "description": description,
            "priority": priority,
            "category": category,
            "status": "todo",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "started_at": None,
            "completed_at": None,
            "due_date": due_date,
            "progress": 0,
            "assignee": "小灵同学助理",
            "notes": []
        }
        
        self.tasks["tasks"].append(task)
        self.tasks["next_id"] += 1
        self.tasks["stats"]["total"] += 1
        self.tasks["stats"]["todo"] += 1
        
        self.save_tasks()
        self.update_kanban()
        
        return task_id
    
    def update_task_status(self, task_id, new_status, progress=None, note=None):
        """更新任务状态"""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                old_status = task["status"]
                
                # 更新统计
                if old_status != new_status:
                    self.tasks["stats"][old_status] -= 1
                    self.tasks["stats"][new_status] += 1
                
                task["status"] = new_status
                
                if new_status == "in_progress" and not task["started_at"]:
                    task["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                elif new_status == "done" and not task["completed_at"]:
                    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    task["progress"] = 100
                
                if progress is not None:
                    task["progress"] = progress
                
                if note:
                    task["notes"].append({
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "content": note
                    })
                
                self.save_tasks()
                self.update_kanban()
                return True
        
        return False
    
    def get_task(self, task_id):
        """获取任务详情"""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status):
        """按状态获取任务"""
        return [task for task in self.tasks["tasks"] if task["status"] == status]
    
    def parse_task_from_message(self, message):
        """从消息解析任务信息"""
        # 简单解析格式：任务: [描述] 优先级: [高/中/低]
        patterns = [
            r'任务[:：]\s*(.+?)(?:\s+优先级[:：]\s*(高|中|低))?',
            r'task[:：]\s*(.+?)(?:\s+priority[:：]\s*(high|medium|low))?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                description = match.group(1).strip()
                priority = match.group(2) if match.group(2) else "中"
                
                # 转换英文优先级
                priority_map = {"high": "高", "medium": "中", "low": "低"}
                if priority.lower() in priority_map:
                    priority = priority_map[priority.lower()]
                
                return {
                    "description": description,
                    "priority": priority
                }
        
        return None
    
    def update_kanban(self):
        """更新看板文件"""
        # 这里会调用生成看板的函数
        # 简化版：先标记需要更新
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 看板需要更新")
        return True
    
    def generate_stats(self):
        """生成统计信息"""
        stats = self.tasks["stats"]
        total = stats["total"]
        
        if total == 0:
            completion_rate = 0
        else:
            completion_rate = (stats["done"] / total) * 100
        
        return {
            "total_tasks": total,
            "todo": stats["todo"],
            "in_progress": stats["in_progress"],
            "done": stats["done"],
            "ideas": stats["ideas"],
            "completion_rate": f"{completion_rate:.1f}%"
        }

def main():
    """主函数 - 测试用"""
    manager = TaskManager()
    
    # 测试创建任务
    task_id = manager.create_task(
        description="测试任务：验证看板系统功能",
        priority="高",
        category="测试"
    )
    
    print(f"创建任务: {task_id}")
    
    # 测试更新任务
    manager.update_task_status(task_id, "in_progress", progress=50)
    print(f"更新任务状态: 进行中")
    
    # 测试获取统计
    stats = manager.generate_stats()
    print(f"统计信息: {stats}")

if __name__ == "__main__":
    main()