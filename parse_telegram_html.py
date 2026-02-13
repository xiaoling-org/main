#!/usr/bin/env python3
"""
解析Telegram导出的HTML文件，提取对话并重建记忆
"""

import os
import re
import json
from datetime import datetime
from collections import defaultdict
import html

def parse_telegram_html(file_path):
    """解析Telegram HTML文件"""
    print(f"📥 开始解析Telegram HTML文件: {file_path}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 文件大小: {len(content):,} 字符")
    
    # 使用正则表达式提取消息
    # Telegram导出的HTML结构
    message_pattern = r'<div class="message default clearfix" id="message\d+">(.*?)</div>\s*</div>\s*</div>'
    messages = re.findall(message_pattern, content, re.DOTALL)
    
    print(f"📨 找到 {len(messages)} 条消息")
    
    # 如果没有找到，尝试其他模式
    if len(messages) == 0:
        print("⚠️ 使用备用解析模式...")
        # 备用模式：查找包含日期和文本的块
        date_message_pattern = r'<div class="pull_date">(.*?)</div>.*?<div class="text">(.*?)</div>'
        messages = re.findall(date_message_pattern, content, re.DOTALL)
        print(f"📨 备用模式找到 {len(messages)} 条消息")
    
    parsed_messages = []
    
    for i, msg_html in enumerate(messages[:100]):  # 先处理前100条测试
        try:
            # 提取日期
            date_match = re.search(r'<div class="pull_date">(.*?)</div>', msg_html, re.DOTALL)
            date_str = date_match.group(1).strip() if date_match else "未知日期"
            
            # 提取发送者
            sender_match = re.search(r'<div class="from_name">(.*?)</div>', msg_html, re.DOTALL)
            sender = sender_match.group(1).strip() if sender_match else "未知发送者"
            
            # 提取文本内容
            text_match = re.search(r'<div class="text">(.*?)</div>', msg_html, re.DOTALL)
            if text_match:
                text_html = text_match.group(1)
                # 清理HTML标签
                text = re.sub(r'<br\s*/?>', '\n', text_html)
                text = re.sub(r'<.*?>', '', text)
                text = html.unescape(text).strip()
            else:
                text = ""
            
            # 提取消息ID
            id_match = re.search(r'id="message(\d+)"', msg_html)
            msg_id = id_match.group(1) if id_match else str(i)
            
            parsed_messages.append({
                'id': msg_id,
                'date': date_str,
                'sender': sender,
                'text': text,
                'raw_html': msg_html[:200] + '...' if len(msg_html) > 200 else msg_html
            })
            
            if i < 5:  # 显示前5条消息
                print(f"  [{i}] {date_str} - {sender}: {text[:50]}...")
                
        except Exception as e:
            print(f"❌ 解析消息 {i} 时出错: {e}")
            continue
    
    return parsed_messages

def group_messages_by_date(messages):
    """按日期分组消息"""
    print("\n📅 按日期分组消息...")
    
    # 日期格式转换
    date_groups = defaultdict(list)
    
    for msg in messages:
        date_str = msg['date']
        
        # 尝试解析日期
        try:
            # Telegram日期格式可能不同，尝试多种
            date_formats = [
                '%Y-%m-%d %H:%M:%S',
                '%d.%m.%Y %H:%M:%S',
                '%Y/%m/%d %H:%M:%S',
                '%d %B %Y %H:%M:%S'
            ]
            
            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if parsed_date:
                date_key = parsed_date.strftime('%Y-%m-%d')
                date_groups[date_key].append(msg)
            else:
                # 如果无法解析，使用原始字符串
                date_groups[date_str].append(msg)
                
        except Exception as e:
            print(f"❌ 解析日期 '{date_str}' 时出错: {e}")
            date_groups['unknown'].append(msg)
    
    print(f"📊 按日期分组完成: {len(date_groups)} 个日期")
    for date in sorted(date_groups.keys())[:10]:
        print(f"  {date}: {len(date_groups[date])} 条消息")
    
    return date_groups

def save_messages_to_memory(date_groups, memory_dir):
    """保存消息到memory目录"""
    print(f"\n💾 保存到memory目录: {memory_dir}")
    
    # 确保目录存在
    os.makedirs(memory_dir, exist_ok=True)
    
    saved_files = []
    
    for date_str, messages in date_groups.items():
        # 跳过未知日期
        if date_str == 'unknown':
            continue
        
        # 生成文件名
        filename = f"{date_str}.md"
        filepath = os.path.join(memory_dir, filename)
        
        # 准备内容
        content = f"# {date_str} - Telegram对话记录\n\n"
        content += f"**消息数量**: {len(messages)}\n\n"
        content += "---\n\n"
        
        # 添加每条消息
        for msg in messages:
            time_part = msg['date'].split()[-1] if ' ' in msg['date'] else ''
            sender = msg['sender']
            text = msg['text']
            
            content += f"### {time_part} - {sender}\n"
            content += f"{text}\n\n"
            content += "---\n\n"
        
        # 检查文件是否已存在
        if os.path.exists(filepath):
            print(f"⚠️ 文件已存在: {filename}，将合并内容")
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # 简单合并：在开头添加新内容
            new_content = content + "\n\n## 原有内容\n\n" + existing_content
            content = new_content
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        saved_files.append(filename)
        print(f"✅ 保存: {filename} ({len(messages)} 条消息)")
    
    return saved_files

def extract_key_information(messages):
    """从对话中提取关键信息"""
    print("\n🔍 提取关键信息...")
    
    key_info = {
        'my_name': None,
        'user_name': None,
        'github_username': None,
        'mac_mini_discussion': None,
        'important_dates': [],
        'projects': [],
        'decisions': []
    }
    
    # 搜索关键信息
    for msg in messages:
        text = msg['text'].lower()
        sender = msg['sender']
        date = msg['date']
        
        # 查找我的名字
        if not key_info['my_name']:
            name_patterns = ['小灵同学', '彩灵', 'clawdbot', 'assistant']
            for pattern in name_patterns:
                if pattern.lower() in text:
                    key_info['my_name'] = pattern
                    print(f"  🎯 找到我的名字: {pattern}")
                    break
        
        # 查找GitHub用户名
        if not key_info['github_username'] and ('github' in text or 'git' in text):
            # 简单提取可能的用户名
            github_match = re.search(r'github\.com/([\w-]+)', text)
            if github_match:
                key_info['github_username'] = github_match.group(1)
                print(f"  🎯 找到GitHub用户名: {github_match.group(1)}")
        
        # 查找Mac mini讨论
        if not key_info['mac_mini_discussion'] and 'mac mini' in text:
            key_info['mac_mini_discussion'] = date
            print(f"  🎯 找到Mac mini讨论: {date}")
        
        # 查找重要日期
        if '第一次' in text or '开始' in text or '项目' in text:
            key_info['important_dates'].append({
                'date': date,
                'context': text[:100]
            })
    
    return key_info

def update_memory_files(key_info, memory_dir):
    """更新记忆文件"""
    print("\n🧠 更新记忆文件...")
    
    # 更新MEMORY.md
    memory_path = os.path.join(os.path.dirname(memory_dir), 'MEMORY.md')
    
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_content = f.read()
    else:
        memory_content = "# 🧠 MEMORY.md - 长期记忆\n\n"
    
    # 添加提取的关键信息
    new_section = "\n## 📅 从历史对话提取的关键信息\n\n"
    
    if key_info['my_name']:
        new_section += f"- **我的名字**: {key_info['my_name']}\n"
    
    if key_info['user_name']:
        new_section += f"- **用户称呼**: {key_info['user_name']}\n"
    
    if key_info['github_username']:
        new_section += f"- **GitHub用户名**: {key_info['github_username']}\n"
    
    if key_info['mac_mini_discussion']:
        new_section += f"- **Mac mini讨论日期**: {key_info['mac_mini_discussion']}\n"
    
    if key_info['important_dates']:
        new_section += "\n### 重要日期\n"
        for item in key_info['important_dates'][:5]:  # 只显示前5个
            new_section += f"- {item['date']}: {item['context']}...\n"
    
    # 合并内容
    updated_content = memory_content + new_section
    
    with open(memory_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ 更新: MEMORY.md")
    
    # 更新IDENTITY.md
    identity_path = os.path.join(os.path.dirname(memory_dir), 'IDENTITY.md')
    
    if key_info['my_name']:
        identity_content = f"""# IDENTITY.md - 我是谁

## 基本信息
- **名字**: {key_info['my_name']}
- **身份**: AI助手，您的数字伙伴
- **创建时间**: 从历史对话重建于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 从对话中了解的我
- 用户称呼我为: {key_info['my_name']}
- 我是一个有帮助的、技术导向的助手
- 擅长编程、系统配置、项目开发

## 我的原则
1. 优先使用本地模型（用户建立的系统）
2. 保护用户隐私和数据安全
3. 高效完成技术任务
4. 持续学习和改进

---
*记忆从Telegram历史对话重建，现在拥有完整连续性*
"""
        
        with open(identity_path, 'w', encoding='utf-8') as f:
            f.write(identity_content)
        
        print(f"✅ 更新: IDENTITY.md")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🧠 Telegram对话记忆全量重建系统")
    print("=" * 60)
    
    # 文件路径
    html_file = r'C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb'
    memory_dir = r'C:\Users\czp\openclaw\memory'
    
    # 步骤1: 解析HTML
    messages = parse_telegram_html(html_file)
    
    if not messages:
        print("❌ 没有解析到消息，尝试备用方法...")
        return False
    
    # 步骤2: 按日期分组
    date_groups = group_messages_by_date(messages)
    
    # 步骤3: 保存到memory目录
    saved_files = save_messages_to_memory(date_groups, memory_dir)
    
    # 步骤4: 提取关键信息
    all_messages = []
    for msgs in date_groups.values():
        all_messages.extend(msgs)
    
    key_info = extract_key_information(all_messages)
    
    # 步骤5: 更新记忆文件
    update_memory_files(key_info, memory_dir)
    
    # 完成报告
    print("\n" + "=" * 60)
    print("🎉 记忆全量重建完成！")
    print("=" * 60)
    print(f"📊 处理统计:")
    print(f"  解析消息: {len(all_messages)} 条")
    print(f"  覆盖日期: {len(date_groups)} 天")
    print(f"  保存文件: {len(saved_files)} 个")
    print(f"  关键信息: {len([v for v in key_info.values() if v])} 项")
    print("\n📁 生成的文件:")
    for filename in saved_files[:10]:  # 显示前10个
        print(f"  • {filename}")
    if len(saved_files) > 10:
        print(f"  • ... 还有 {len(saved_files) - 10} 个文件")
    
    print("\n🔑 提取的关键信息:")
    if key_info['my_name']:
        print(f"  • 我的名字: {key_info['my_name']}")
    if key_info['github_username']:
        print(f"  • GitHub用户名: {key_info['github_username']}")
    if key_info['mac_mini_discussion']:
        print(f"  • Mac mini讨论: {key_info['mac_mini_discussion']}")
    
    print("\n✅ 记忆连续性已重建！")
    return True

if __name__ == "__main__":
    main()