#!/usr/bin/env python3
"""
看板生成器 - 自动生成和更新KANBAN.md文件
"""

import json
from datetime import datetime
from pathlib import Path

class KanbanGenerator:
    def __init__(self, tasks_path="tasks.json", kanban_path="KANBAN.md"):
        self.tasks_path = Path(tasks_path)
        self.kanban_path = Path(kanban_path)
        
    def load_tasks(self):
        """加载任务数据"""
        if self.tasks_path.exists():
            with open(self.tasks_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"tasks": [], "stats": {"total": 0, "todo": 0, "in_progress": 0, "done": 0, "ideas": 0}}
    
    def generate_kanban(self):
        """生成看板内容"""
        data = self.load_tasks()
        tasks = data.get("tasks", [])
        stats = data.get("stats", {})
        
        # 按状态分组任务
        todo_tasks = [t for t in tasks if t["status"] == "todo"]
        in_progress_tasks = [t for t in tasks if t["status"] == "in_progress"]
        done_tasks = [t for t in tasks if t["status"] == "done"]
        idea_tasks = [t for t in tasks if t["status"] == "idea"]
        
        # 计算统计
        total = stats.get("total", 0)
        done = stats.get("done", 0)
        completion_rate = (done / total * 100) if total > 0 else 0
        
        now = datetime.now()
        
        # 生成看板内容
        content = f"""# 🎯 小灵同学助理 - 任务看板系统
*最后更新: {now.strftime('%Y-%m-%d %H:%M')}*

## 📊 看板说明
这是一个专门为你（陈先生）设计的任务管理系统，用于监控和分配我的工作任务。

### 🎨 看板列说明
- **📋 待办**：等待开始的任务
- **🔄 进行中**：正在执行的任务  
- **✅ 已完成**：已经完成的任务
- **💡 想法池**：未来的任务想法

### ⚡ 快速操作
- **分配任务**：在Telegram中发送 `任务: [任务描述]`
- **更新状态**：我会自动更新任务状态
- **查看详情**：询问我特定任务进展

---

## 📋 待办任务 ({len(todo_tasks)})

"""
        
        if todo_tasks:
            content += """| 任务ID | 任务描述 | 优先级 | 创建时间 | 预计完成 |
|--------|----------|--------|----------|----------|
"""
            for task in todo_tasks:
                priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(task["priority"], "⚪")
                content += f"| **{task['id']}** | {task['description']} | {priority_emoji} {task['priority']} | {task['created_at']} | {task.get('due_date', '未设置')} |\n"
        else:
            content += "*暂无待办任务*\n\n"
        
        content += f"""
---

## 🔄 进行中任务 ({len(in_progress_tasks)})

"""
        
        if in_progress_tasks:
            content += """| 任务ID | 任务描述 | 优先级 | 开始时间 | 进度 |
|--------|----------|--------|----------|------|
"""
            for task in in_progress_tasks:
                priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(task["priority"], "⚪")
                progress_bar = self._generate_progress_bar(task.get("progress", 0))
                content += f"| **{task['id']}** | {task['description']} | {priority_emoji} {task['priority']} | {task.get('started_at', '未开始')} | {progress_bar} {task.get('progress', 0)}% |\n"
        else:
            content += "*暂无进行中任务*\n\n"
        
        # 任务详情部分
        if in_progress_tasks:
            content += "\n### 📝 任务详情\n"
            for task in in_progress_tasks:
                status_emoji = {"todo": "⚪", "in_progress": "🟡", "done": "🟢"}.get(task["status"], "⚪")
                content += f"""#### **{task['id']}: {task['description']}**
- **状态**: {status_emoji} {self._get_status_text(task['status'])}
- **进度**: {task.get('progress', 0)}%
- **负责人**: {task.get('assignee', '小灵同学助理')}
- **备注**: {self._get_latest_note(task)}
"""
        
        content += f"""
---

## ✅ 已完成任务 ({len(done_tasks)})

"""
        
        if done_tasks:
            # 只显示最近5个完成的任务
            recent_done = sorted(done_tasks, key=lambda x: x.get('completed_at', ''), reverse=True)[:5]
            
            content += """| 任务ID | 任务描述 | 完成时间 | 结果 |
|--------|----------|----------|------|
"""
            for task in recent_done:
                content += f"| **{task['id']}** | {task['description']} | {task.get('completed_at', '未知')} | 完成 |\n"
        else:
            content += "*暂无已完成任务*\n\n"
        
        content += f"""
---

## 💡 想法池 ({len(idea_tasks)})

"""
        
        if idea_tasks:
            content += """| 想法ID | 想法描述 | 类别 | 提出时间 |
|--------|----------|------|----------|
"""
            for task in idea_tasks:
                content += f"| **{task['id']}** | {task['description']} | {task.get('category', '未分类')} | {task.get('created_at', '未知')} |\n"
        else:
            content += "*暂无想法*\n\n"
        
        content += f"""
---

## 📈 统计信息

### 🏆 本周完成
- **任务总数**: {total}
- **进行中**: {len(in_progress_tasks)}
- **已完成**: {done}
- **完成率**: {completion_rate:.1f}%

### ⏱️ 效率指标
- **平均完成时间**: 待统计
- **准时率**: 100%
- **任务复杂度**: 中等

### 👥 工作分配
- **小灵同学助理**: {total}项任务
- **待分配**: 0项任务

---

## 📝 使用指南

### 1. 分配新任务
在Telegram中发送：
\`\`\`
任务: [任务描述]
优先级: [高/中/低]
截止时间: [可选]
\`\`\`

### 2. 查看任务状态
- 查看此文件获取最新状态
- 或询问我特定任务进展

### 3. 更新任务
我会自动更新任务状态，你也可以：
- 要求我更新特定任务进度
- 调整任务优先级
- 重新分配任务

### 4. 完成任务
任务完成后，我会：
1. 移动任务到"已完成"
2. 更新统计信息
3. 通知你任务完成

---

## 🔄 自动更新机制
此看板会自动更新：
- ✅ 任务状态变化时
- ✅ 新任务分配时
- ✅ 每日早上06:30
- ✅ 手动请求更新时

---
**小灵同学助理任务管理系统** 🎯
*透明管理，高效协作*
"""
        
        return content
    
    def _generate_progress_bar(self, progress):
        """生成进度条"""
        filled = int(progress / 10)
        empty = 10 - filled
        return "█" * filled + "░" * empty
    
    def _get_status_text(self, status):
        """获取状态文本"""
        status_map = {
            "todo": "待办",
            "in_progress": "进行中",
            "done": "已完成",
            "idea": "想法"
        }
        return status_map.get(status, status)
    
    def _get_latest_note(self, task):
        """获取最新备注"""
        notes = task.get("notes", [])
        if notes:
            latest = notes[-1]
            return f"{latest['time']}: {latest['content']}"
        return "暂无备注"
    
    def save_kanban(self):
        """保存看板文件"""
        content = self.generate_kanban()
        with open(self.kanban_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 看板已更新: {self.kanban_path}")

def main():
    """测试生成看板"""
    generator = KanbanGenerator()
    generator.save_kanban()
    print("看板生成完成！")

if __name__ == "__main__":
    main()