"""
🎯 小灵同学看板系统 v3.0 - 增强版
功能：标签分类、搜索过滤、评论讨论、导入导出、工具集成
作者：小灵同学助理
日期：2026-02-10
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import csv
from datetime import datetime
import uuid
import traceback
import re
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kanban-realtime-secret-2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# WebSocket连接管理
connected_clients = {}
board_rooms = {}

# 数据验证函数
def validate_task_data(task_data):
    """验证任务数据"""
    errors = []
    
    # 验证标题
    title = task_data.get('title', '').strip()
    if not title:
        errors.append("标题不能为空")
    elif len(title) > 200:
        errors.append("标题不能超过200个字符")
    
    # 验证描述
    description = task_data.get('description', '').strip()
    if description and len(description) > 2000:
        errors.append("描述不能超过2000个字符")
    
    # 验证优先级
    priority = task_data.get('priority', 'medium')
    if priority not in ['low', 'medium', 'high', 'urgent']:
        errors.append("优先级必须是 low, medium, high, urgent 之一")
    
    # 验证标签
    tags = task_data.get('tags', [])
    if not isinstance(tags, list):
        errors.append("标签必须是列表")
    else:
        for tag in tags:
            if not isinstance(tag, str):
                errors.append("标签必须是字符串")
            elif len(tag) > 50:
                errors.append("标签不能超过50个字符")
    
    # 验证截止日期格式
    due_date = task_data.get('due_date')
    if due_date:
        try:
            datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            errors.append("截止日期格式不正确，请使用ISO格式")
    
    return errors

def validate_user_data(user_data):
    """验证用户数据"""
    errors = []
    
    username = user_data.get('username', '').strip()
    if not username:
        errors.append("用户名不能为空")
    elif len(username) < 2:
        errors.append("用户名至少2个字符")
    elif len(username) > 50:
        errors.append("用户名不能超过50个字符")
    elif not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
        errors.append("用户名只能包含字母、数字、下划线和中文字符")
    
    return errors

def validate_comment_data(comment_data):
    """验证评论数据"""
    errors = []
    
    content = comment_data.get('content', '').strip()
    if not content:
        errors.append("评论内容不能为空")
    elif len(content) > 1000:
        errors.append("评论内容不能超过1000个字符")
    
    user = comment_data.get('user', '').strip()
    if not user:
        errors.append("评论用户不能为空")
    
    return errors

def sanitize_input(text):
    """清理输入，防止XSS攻击"""
    if not text:
        return text
    
    # 替换危险字符
    text = str(text)
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    text = text.replace('&', '&amp;')
    
    return text

# 全局错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Resource not found",
        "message": str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server error: {error}")
    app.logger.error(traceback.format_exc())
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f"Unhandled exception: {error}")
    app.logger.error(traceback.format_exc())
    return jsonify({
        "success": False,
        "error": "Unexpected error",
        "message": str(error)
    }), 500

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
            "users": [
                {
                    "id": "admin",
                    "username": "管理员",
                    "role": "admin",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "xiaoling",
                    "username": "小灵同学",
                    "role": "user", 
                    "created_at": datetime.now().isoformat()
                }
            ],
            "activity_log": [],
            "sessions": {}
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
                    
                    # WebSocket广播任务移动
                    try:
                        socketio.emit('task_move', {
                            'task_id': task_id,
                            'from_column': from_col,
                            'to_column': to_col,
                            'user_id': request.json.get('user_id', 'system'),
                            'timestamp': datetime.now().isoformat(),
                            'task_title': moved_task.get('title', '')
                        }, room='default')
                    except:
                        pass  # WebSocket不可用时静默失败
                    
                    return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Task not found"})

# API: 添加任务
@app.route('/api/add_task', methods=['POST'])
def add_task():
    data = load_data()
    task_data = request.json
    
    # 数据验证
    validation_errors = validate_task_data(task_data)
    if validation_errors:
        return jsonify({
            "success": False,
            "error": "数据验证失败",
            "details": validation_errors
        }), 400
    
    # 清理输入
    sanitized_data = {}
    for key, value in task_data.items():
        if isinstance(value, str):
            sanitized_data[key] = sanitize_input(value)
        else:
            sanitized_data[key] = value
    
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "title": sanitized_data.get('title', '新任务'),
        "description": sanitized_data.get('description', ''),
        "tags": sanitized_data.get('tags', []),
        "priority": sanitized_data.get('priority', 'medium'),
        "due_date": sanitized_data.get('due_date'),
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
    
    # WebSocket广播新任务
    try:
        socketio.emit('task_update', {
            'task_id': task_id,
            'action': 'created',
            'user_id': request.json.get('user_id', 'system'),
            'timestamp': datetime.now().isoformat(),
            'data': new_task
        }, room='default')
    except:
        pass  # WebSocket不可用时静默失败
    
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

# API: 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    data = load_data()
    username = request.json.get('username', '').strip()
    
    # 查找用户或创建新用户
    user = None
    for u in data['users']:
        if u['username'] == username:
            user = u
            break
    
    if not user:
        # 创建新用户
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "username": username,
            "role": "user",
            "created_at": datetime.now().isoformat()
        }
        data['users'].append(user)
        save_data(data)
    
    # 创建会话
    session_id = str(uuid.uuid4())
    if 'sessions' not in data:
        data['sessions'] = {}
    data['sessions'][session_id] = {
        "user_id": user['id'],
        "username": user['username'],
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat()
    }
    save_data(data)
    
    # 记录活动
    log_activity("login", {
        "user_id": user['id'],
        "username": user['username']
    })
    
    return jsonify({
        "success": True,
        "user": {
            "id": user['id'],
            "username": user['username'],
            "role": user['role']
        },
        "session_id": session_id
    })

# API: 用户登出
@app.route('/api/logout', methods=['POST'])
def logout():
    data = load_data()
    session_id = request.json.get('session_id')
    
    if session_id and session_id in data.get('sessions', {}):
        user_info = data['sessions'].pop(session_id)
        
        # 记录活动
        log_activity("logout", {
            "user_id": user_info['user_id'],
            "username": user_info['username']
        })
        
        save_data(data)
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Invalid session"})

# API: 获取当前用户
@app.route('/api/current_user')
def current_user():
    session_id = request.args.get('session_id')
    data = load_data()
    
    if session_id and session_id in data.get('sessions', {}):
        session_info = data['sessions'][session_id]
        # 更新最后活跃时间
        data['sessions'][session_id]['last_active'] = datetime.now().isoformat()
        save_data(data)
        
        # 查找用户信息
        for user in data['users']:
            if user['id'] == session_info['user_id']:
                return jsonify({
                    "success": True,
                    "user": {
                        "id": user['id'],
                        "username": user['username'],
                        "role": user['role']
                    }
                })
    
    return jsonify({"success": False, "error": "Not authenticated"})

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
    
    # WebSocket事件处理
    @socketio.on('connect')
    def handle_connect():
        """客户端连接"""
        client_id = request.sid
        connected_clients[client_id] = {
            'connected_at': datetime.now().isoformat(),
            'user': None
        }
        print(f"📡 客户端连接: {client_id}")
        emit('connected', {'message': 'Connected to Kanban WebSocket', 'client_id': client_id})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """客户端断开"""
        client_id = request.sid
        if client_id in connected_clients:
            user_info = connected_clients.pop(client_id)
            print(f"📡 客户端断开: {client_id}, 用户: {user_info.get('user')}")
            
            # 从所有房间移除
            for room in board_rooms.get(client_id, []):
                leave_room(room)
    
    @socketio.on('join_board')
    def handle_join_board(data):
        """加入看板房间"""
        client_id = request.sid
        board_id = data.get('board_id', 'default')
        user_id = data.get('user_id')
        
        join_room(board_id)
        
        # 记录用户加入的房间
        if client_id not in board_rooms:
            board_rooms[client_id] = []
        if board_id not in board_rooms[client_id]:
            board_rooms[client_id].append(board_id)
        
        # 更新用户信息
        if user_id and client_id in connected_clients:
            connected_clients[client_id]['user'] = user_id
        
        print(f"👥 用户 {user_id} 加入看板: {board_id}")
        emit('board_joined', {
            'board_id': board_id,
            'user_id': user_id,
            'message': f'Joined board {board_id}'
        }, room=board_id)
    
    @socketio.on('leave_board')
    def handle_leave_board(data):
        """离开看板房间"""
        client_id = request.sid
        board_id = data.get('board_id', 'default')
        
        leave_room(board_id)
        
        if client_id in board_rooms and board_id in board_rooms[client_id]:
            board_rooms[client_id].remove(board_id)
        
        print(f"👋 用户离开看板: {board_id}")
        emit('board_left', {
            'board_id': board_id,
            'message': f'Left board {board_id}'
        })
    
    @socketio.on('task_updated')
    def handle_task_updated(data):
        """任务更新广播"""
        board_id = data.get('board_id', 'default')
        task_id = data.get('task_id')
        action = data.get('action')  # created, updated, moved, deleted
        user_id = data.get('user_id')
        
        print(f"🔄 任务更新广播: {action} 任务 {task_id} by {user_id}")
        
        # 广播给看板房间的所有用户（除了发送者）
        emit('task_update', {
            'task_id': task_id,
            'action': action,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'data': data.get('data', {})
        }, room=board_id, include_self=False)
    
    @socketio.on('task_moved')
    def handle_task_moved(data):
        """任务移动广播"""
        board_id = data.get('board_id', 'default')
        task_id = data.get('task_id')
        from_column = data.get('from_column')
        to_column = data.get('to_column')
        user_id = data.get('user_id')
        
        print(f"🔄 任务移动: {task_id} from {from_column} to {to_column}")
        
        emit('task_move', {
            'task_id': task_id,
            'from_column': from_column,
            'to_column': to_column,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }, room=board_id, include_self=False)
    
    @socketio.on('comment_added')
    def handle_comment_added(data):
        """评论添加广播"""
        board_id = data.get('board_id', 'default')
        task_id = data.get('task_id')
        comment_id = data.get('comment_id')
        user_id = data.get('user_id')
        
        print(f"💬 评论添加: 任务 {task_id}, 用户 {user_id}")
        
        emit('comment_add', {
            'task_id': task_id,
            'comment_id': comment_id,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'content': data.get('content', '')
        }, room=board_id, include_self=False)
    
    @socketio.on('user_typing')
    def handle_user_typing(data):
        """用户正在输入广播"""
        board_id = data.get('board_id', 'default')
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        
        emit('user_typing_indicator', {
            'user_id': user_id,
            'task_id': task_id,
            'timestamp': datetime.now().isoformat()
        }, room=board_id, include_self=False)
    
    @socketio.on('get_online_users')
    def handle_get_online_users(data):
        """获取在线用户"""
        board_id = data.get('board_id', 'default')
        
        # 获取在看板房间的所有用户
        online_users = []
        for client_id, rooms in board_rooms.items():
            if board_id in rooms and client_id in connected_clients:
                user_info = connected_clients[client_id]
                if user_info.get('user'):
                    online_users.append({
                        'user_id': user_info['user'],
                        'connected_at': user_info['connected_at']
                    })
        
        emit('online_users', {
            'board_id': board_id,
            'users': online_users,
            'count': len(online_users)
        })
    
    print("=" * 60)
    print("🌐 WebSocket实时功能已启用")
    print("📡 支持实时任务更新、移动、评论")
    print("👥 支持多用户在线协作")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)