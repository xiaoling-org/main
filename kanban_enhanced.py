"""
🎯 小灵同学看板系统 v3.0 - 增强版
功能：标签分类、搜索过滤、评论讨论、导入导出、工具集成
作者：小灵同学助理
日期：2026-02-10
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import csv
from datetime import datetime
import uuid

app = Flask(__name__)

# 数据文件路径
DATA_FILE = 'kanban_data.json'
BACKUP_DIR = 'backups'

# 确保备份目录存在
os.makedirs(BACKUP_DIR, exist_ok=True)

# 预定义标签
PREDEFINED_TAGS = [
    {"id": "urgent", "name": "紧急", "color": "#ff4444"},
    {"id": "important", "name": "重要", "color": "#ffaa00"},
    {"id": "routine", "name": "日常", "color": "#44aa44"},
    {"id": "longterm", "name": "长期", "color": "#4488ff"},
    {"id": "bug", "name": "Bug", "color": "#ff44aa"},
    {"id": "feature", "name": "功能", "color": "#aa44ff"}
]

# 初始化数据
def init_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "boards": {
                "default": {
                    "name": "默认看板",
                    "columns": {
                        "todo": {"id": "todo", "name": "待处理", "tasks": []},
                        "doing": {"id": "doing", "name": "进行中", "tasks": []},
                        "done": {"id": "done", "name": "已完成", "tasks": []}
                    }
                }
            },
            "tags": PREDEFINED_TAGS,
            "custom_tags": [],
            "users": [],
            "activity_log": []
        }
        save_data(data)
    return load_data()

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return init_data()

def save_data(data):
    # 创建备份
    backup_file = os.path.join(BACKUP_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    if os.path.exists(DATA_FILE):
        import shutil
        shutil.copy2(DATA_FILE, backup_file)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_activity(action, details):
    data = load_data()
    activity = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    }
    data["activity_log"].append(activity)
    save_data(data)

# 路由定义
@app.route('/')
def index():
    return render_template('index_enhanced.html')

# API: 获取看板数据
@app.route('/api/board')
def get_board():
    data = load_data()
    return jsonify(data)

# API: 更新任务位置
@app.route('/api/move_task', methods=['POST'])
def move_task():
    data = load_data()
    task_id = request.json.get('taskId')
    from_col = request.json.get('fromColumn')
    to_col = request.json.get('toColumn')
    index = request.json.get('index', 0)
    
    # 查找并移动任务
    for col_id, column in data['boards']['default']['columns'].items():
        for i, task in enumerate(column['tasks']):
            if task['id'] == task_id:
                if col_id == from_col:
                    # 从原列移除
                    moved_task = column['tasks'].pop(i)
                    # 添加到目标列
                    data['boards']['default']['columns'][to_col]['tasks'].insert(index, moved_task)
                    
                    # 记录活动
                    log_activity("move_task", {
                        "task_id": task_id,
                        "from_column": from_col,
                        "to_column": to_col,
                        "task_title": moved_task.get('title', '')
                    })
                    
                    save_data(data)
                    return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Task not found"})

# API: 添加任务
@app.route('/api/add_task', methods=['POST'])
def add_task():
    data = load_data()
    task_data = request.json
    
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "title": task_data.get('title', '新任务'),
        "description": task_data.get('description', ''),
        "tags": task_data.get('tags', []),
        "priority": task_data.get('priority', 'medium'),
        "due_date": task_data.get('due_date'),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "comments": [],
        "attachments": []
    }
    
    column_id = task_data.get('column', 'todo')
    data['boards']['default']['columns'][column_id]['tasks'].append(new_task)
    
    # 记录活动
    log_activity("add_task", {
        "task_id": task_id,
        "title": new_task['title'],
        "column": column_id
    })
    
    save_data(data)
    return jsonify({"success": True, "task": new_task})

# API: 更新任务
@app.route('/api/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    data = load_data()
    updates = request.json
    
    # 查找任务
    for col_id, column in data['boards']['default']['columns'].items():
        for task in column['tasks']:
            if task['id'] == task_id:
                # 更新任务字段
                for key, value in updates.items():
                    if key not in ['id', 'created_at']:
                        task[key] = value
                task['updated_at'] = datetime.now().isoformat()
                
                # 记录活动
                log_activity("update_task", {
                    "task_id": task_id,
                    "updates": list(updates.keys()),
                    "title": task.get('title', '')
                })
                
                save_data(data)
                return jsonify({"success": True, "task": task})
    
    return jsonify({"success": False, "error": "Task not found"})

# API: 删除任务
@app.route('/api/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    data = load_data()
    
    # 查找并删除任务
    for col_id, column in data['boards']['default']['columns'].items():
        for i, task in enumerate(column['tasks']):
            if task['id'] == task_id:
                deleted_task = column['tasks'].pop(i)
                
                # 记录活动
                log_activity("delete_task", {
                    "task_id": task_id,
                    "title": deleted_task.get('title', ''),
                    "column": col_id
                })
                
                save_data(data)
                return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Task not found"})

# API: 添加评论
@app.route('/api/add_comment/<task_id>', methods=['POST'])
def add_comment(task_id):
    data = load_data()
    comment_data = request.json
    
    # 查找任务
    for col_id, column in data['boards']['default']['columns'].items():
        for task in column['tasks']:
            if task['id'] == task_id:
                comment = {
                    "id": str(uuid.uuid4()),
                    "user": comment_data.get('user', '匿名'),
                    "content": comment_data.get('content', ''),
                    "timestamp": datetime.now().isoformat(),
                    "mentions": comment_data.get('mentions', [])
                }
                
                if 'comments' not in task:
                    task['comments'] = []
                task['comments'].append(comment)
                task['updated_at'] = datetime.now().isoformat()
                
                # 记录活动
                log_activity("add_comment", {
                    "task_id": task_id,
                    "task_title": task.get('title', ''),
                    "comment_user": comment['user']
                })
                
                save_data(data)
                return jsonify({"success": True, "comment": comment})
    
    return jsonify({"success": False, "error": "Task not found"})

# API: 搜索任务
@app.route('/api/search')
def search_tasks():
    data = load_data()
    query = request.args.get('q', '').lower()
    tag_filter = request.args.get('tag', '')
    status_filter = request.args.get('status', '')
    
    results = []
    
    for col_id, column in data['boards']['default']['columns'].items():
        for task in column['tasks']:
            # 关键词搜索
            matches_query = (query in task.get('title', '').lower() or 
                           query in task.get('description', '').lower())
            
            # 标签过滤
            matches_tag = True
            if tag_filter:
                matches_tag = tag_filter in task.get('tags', [])
            
            # 状态过滤
            matches_status = True
            if status_filter:
                matches_status = (status_filter == 'todo' and col_id == 'todo') or \
                                (status_filter == 'doing' and col_id == 'doing') or \
                                (status_filter == 'done' and col_id == 'done')
            
            if matches_query and matches_tag and matches_status:
                result_task = task.copy()
                result_task['column'] = col_id
                result_task['column_name'] = column['name']
                results.append(result_task)
    
    return jsonify({"results": results})

# API: 获取所有标签
@app.route('/api/tags')
def get_tags():
    data = load_data()
    all_tags = data.get('tags', []) + data.get('custom_tags', [])
    return jsonify({"tags": all_tags})

# API: 添加自定义标签
@app.route('/api/add_tag', methods=['POST'])
def add_tag():
    data = load_data()
    tag_data = request.json
    
    new_tag = {
        "id": str(uuid.uuid4()),
        "name": tag_data.get('name', '新标签'),
        "color": tag_data.get('color', '#888888')
    }
    
    if 'custom_tags' not in data:
        data['custom_tags'] = []
    data['custom_tags'].append(new_tag)
    
    save_data(data)
    return jsonify({"success": True, "tag": new_tag})

# API: 导出数据
@app.route('/api/export/<format_type>')
def export_data(format_type):
    data = load_data()
    
    if format_type == 'json':
        # 导出为JSON
        export_file = 'kanban_export.json'
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log_activity("export_data", {"format": "json"})
        return send_file(export_file, as_attachment=True)
    
    elif format_type == 'csv':
        # 导出为CSV
        export_file = 'kanban_export.csv'
        with open(export_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入标题行
            writer.writerow(['ID', '标题', '描述', '状态', '标签', '优先级', '截止日期', '创建时间', '更新时间'])
            
            # 写入任务数据
            for col_id, column in data['boards']['default']['columns'].items():
                for task in column['tasks']:
                    writer.writerow([
                        task.get('id', ''),
                        task.get('title', ''),
                        task.get('description', ''),
                        column['name'],
                        ','.join(task.get('tags', [])),
                        task.get('priority', ''),
                        task.get('due_date', ''),
                        task.get('created_at', ''),
                        task.get('updated_at', '')
                    ])
        
        log_activity("export_data", {"format": "csv"})
        return send_file(export_file, as_attachment=True)
    
    return jsonify({"success": False, "error": "Unsupported format"})

# API: 导入Trello数据
@app.route('/api/import/trello', methods=['POST'])
def import_trello():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"})
    
    try:
        trello_data = json.load(file)
        data = load_data()
        
        # 简单的Trello导入逻辑（可根据实际Trello导出格式调整）
        # 这里假设Trello导出为JSON格式
        imported_count = 0
        
        if 'cards' in trello_data:
            for card in trello_data['cards']:
                task_id = str(uuid.uuid4())
                new_task = {
                    "id": task_id,
                    "title": card.get('name', '导入的任务'),
                    "description": card.get('desc', ''),
                    "tags": [label.get('name', '') for label in card.get('labels', []) if label.get('name')],
                    "priority": 'medium',
                    "due_date": card.get('due'),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "comments": [],
                    "attachments": []
                }
                
                # 根据列表名称决定放入哪一列
                list_name = card.get('list', {}).get('name', '').lower()
                if 'done' in list_name or '完成' in list_name:
                    column_id = 'done'
                elif 'doing' in list_name or '进行' in list_name:
                    column_id = 'doing'
                else:
                    column_id = 'todo'
                
                data['boards']['default']['columns'][column_id]['tasks'].append(new_task)
                imported_count += 1
        
        save_data(data)
        log_activity("import_trello", {"count": imported_count})
        
        return jsonify({
            "success": True, 
            "message": f"成功导入 {imported_count} 个任务",
            "count": imported_count
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# API: 获取活动日志
@app.route('/api/activity')
def get_activity():
    data = load_data()
    limit = int(request.args.get('limit', 50))
    activities = data.get('activity_log', [])[-limit:]
    return jsonify({"activities": list(reversed(activities))})

# API: 系统状态
@app.route('/api/status')
def system_status():
    data = load_data()
    total_tasks = 0
    for column in data['boards']['default']['columns'].values():
        total_tasks += len(column['tasks'])
    
    return jsonify({
        "version": "3.0",
        "total_tasks": total_tasks,
        "total_tags": len(data.get('tags', [])) + len(data.get('custom_tags', [])),
        "last_backup": sorted(os.listdir(BACKUP_DIR))[-1] if os.path.exists(BACKUP_DIR) and os.listdir(BACKUP_DIR) else "无",
        "uptime": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # 初始化数据
    init_data()
    
    print("=" * 60)
    print("🎯 小灵同学看板系统 v3.0 - 增强版")
    print("=" * 60)
    print("🚀 启动系统...")
    print("🌐 电脑访问: http://localhost:5000")
    print("📱 手机访问: http://192.168.0.64:5000")
    print("=" * 60)
    print("✨ 新增功能:")
    print("  • 任务标签/分类系统")
    print("  • 搜索过滤功能")
    print("  • 任务评论/讨论")
    print("  • 导入/导出数据")
    print("  • 活动日志记录")
    print("=" * 60)
    print("按 Ctrl+C 停止系统")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)