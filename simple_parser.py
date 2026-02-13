#!/usr/bin/env python3
"""
简单解析Telegram HTML文件
"""

import os
import re
from datetime import datetime

def main():
    print("🧠 开始解析Telegram HTML文件...")
    
    # 文件路径
    html_file = r'C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb'
    memory_dir = r'C:\Users\czp\openclaw\memory'
    
    # 确保memory目录存在
    os.makedirs(memory_dir, exist_ok=True)
    
    # 读取文件
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 读取文件成功，大小: {len(content):,} 字符")
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return
    
    # 简单提取：查找所有包含日期的div
    print("\n🔍 提取消息...")
    
    # 查找日期和消息的模式
    # 模式1: <div class="pull_date">日期</div> 后面跟着消息
    date_pattern = r'<div class="pull_date">([^<]+)</div>'
    text_pattern = r'<div class="text">([^<]+)</div>'
    
    # 查找所有日期
    dates = re.findall(date_pattern, content)
    print(f"📅 找到 {len(dates)} 个日期标记")
    
    if dates:
        print("前5个日期:")
        for i, date in enumerate(dates[:5]):
            print(f"  {i+1}. {date}")
    
    # 查找所有文本
    texts = re.findall(text_pattern, content)
    print(f"📝 找到 {len(texts)} 个文本标记")
    
    if texts:
        print("前5个文本:")
        for i, text in enumerate(texts[:5]):
            print(f"  {i+1}. {text[:50]}...")
    
    # 尝试提取完整的消息块
    print("\n🔍 尝试提取完整消息块...")
    
    # 查找消息容器
    message_blocks = re.findall(r'<div class="message[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
    print(f"📦 找到 {len(message_blocks)} 个消息块")
    
    if message_blocks:
        # 处理前3个消息块作为示例
        for i, block in enumerate(message_blocks[:3]):
            print(f"\n消息块 {i+1}:")
            
            # 提取日期
            date_match = re.search(r'<div class="pull_date">([^<]+)</div>', block)
            if date_match:
                print(f"  日期: {date_match.group(1)}")
            
            # 提取发送者
            sender_match = re.search(r'<div class="from_name">([^<]+)</div>', block)
            if sender_match:
                print(f"  发送者: {sender_match.group(1)}")
            
            # 提取文本
            text_match = re.search(r'<div class="text">(.*?)</div>', block, re.DOTALL)
            if text_match:
                text = text_match.group(1)
                # 清理HTML
                text = re.sub(r'<br\s*/?>', '\n', text)
                text = re.sub(r'<[^>]+>', '', text)
                print(f"  文本: {text[:100]}...")
    
    # 创建简单的记忆文件
    print("\n💾 创建记忆文件...")
    
    # 提取所有日期并分组
    date_messages = {}
    
    # 使用更简单的模式：查找日期和紧随其后的文本
    simple_pattern = r'<div class="pull_date">([^<]+)</div>\s*<div class="text">([^<]+)</div>'
    matches = re.findall(simple_pattern, content)
    
    print(f"📊 找到 {len(matches)} 个日期-文本对")
    
    for date_str, text in matches[:10]:  # 先处理前10个
        # 清理文本
        text = re.sub(r'<br\s*/?>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.strip()
        
        # 提取日期部分（去掉时间）
        date_part = date_str.split()[0] if ' ' in date_str else date_str
        
        if date_part not in date_messages:
            date_messages[date_part] = []
        
        date_messages[date_part].append({
            'time': date_str,
            'text': text
        })
    
    # 保存到文件
    for date_str, messages in date_messages.items():
        filename = f"{date_str}.md"
        filepath = os.path.join(memory_dir, filename)
        
        content = f"# {date_str} - Telegram对话记录\n\n"
        content += f"**消息数量**: {len(messages)}\n\n"
        content += "---\n\n"
        
        for msg in messages:
            content += f"### {msg['time']}\n"
            content += f"{msg['text']}\n\n"
            content += "---\n\n"
        
        # 如果文件已存在，合并
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                existing = f.read()
            content = content + "\n\n## 原有内容\n\n" + existing
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 保存: {filename} ({len(messages)} 条消息)")
    
    print(f"\n🎉 完成！创建了 {len(date_messages)} 个记忆文件")
    
    # 搜索关键信息
    print("\n🔎 搜索关键信息...")
    
    search_terms = {
        '小灵同学': '我的名字',
        '彩灵': '我的别名',
        'GitHub': 'GitHub用户名',
        'github': 'GitHub用户名',
        'mac mini': 'Mac mini讨论',
        '陈志标': '用户姓名',
        'czp': '用户名缩写'
    }
    
    all_text = ' '.join([msg['text'] for msgs in date_messages.values() for msg in msgs])
    
    for term, description in search_terms.items():
        if term.lower() in all_text.lower():
            print(f"  🔍 找到 '{term}': {description}")
            
            # 找到包含该术语的消息
            for date_str, messages in date_messages.items():
                for msg in messages:
                    if term.lower() in msg['text'].lower():
                        print(f"    在 {date_str}: {msg['text'][:50]}...")
                        break
                break

if __name__ == "__main__":
    main()