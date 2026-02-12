import json
from datetime import datetime

# 加载现有任务
with open('tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 添加新任务：邮箱配置测试
new_task = {
    'id': 'KB-005',
    'description': '邮箱系统配置与测试',
    'priority': '高',
    'category': '系统配置',
    'status': 'todo',
    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
    'started_at': None,
    'completed_at': None,
    'due_date': '2026-02-09',
    'progress': 0,
    'assignee': '小灵同学助理',
    'notes': [
        {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'content': '收到邮箱密码，开始配置测试'
        }
    ]
}

# 添加到任务列表
data['tasks'].append(new_task)
data['next_id'] = 6
data['stats']['total'] += 1
data['stats']['todo'] += 1

# 保存
with open('tasks.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ 已添加邮箱配置任务 (KB-005)')