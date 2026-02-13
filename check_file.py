#!/usr/bin/env python3
"""
检查接收的文件格式
"""

import os
import json

def check_file_format(file_path):
    """检查文件格式"""
    print(f"📁 检查文件: {file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print("❌ 文件不存在")
        return False
    
    # 获取文件大小
    file_size = os.path.getsize(file_path)
    print(f"📊 文件大小: {file_size:,} 字节 ({file_size/1024:.2f} KB)")
    
    # 读取文件开头判断格式
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            second_line = f.readline().strip()
            
        print(f"📝 第一行: {first_line[:100]}...")
        print(f"📝 第二行: {second_line[:100]}...")
        
        # 判断文件类型
        if first_line.startswith('<!DOCTYPE html>'):
            print("🔍 文件类型: HTML (Telegram导出的HTML格式)")
            return 'html'
        elif first_line.startswith('{') or second_line.startswith('{'):
            print("🔍 文件类型: JSON")
            return 'json'
        else:
            print("🔍 文件类型: 未知")
            return 'unknown'
            
    except UnicodeDecodeError:
        # 可能是二进制文件
        with open(file_path, 'rb') as f:
            header = f.read(100)
        print(f"🔍 二进制文件，头部: {header[:50]}...")
        return 'binary'
    except Exception as e:
        print(f"❌ 读取文件错误: {e}")
        return False

def extract_html_content(file_path):
    """从HTML文件中提取对话内容"""
    print("\n🔧 开始解析HTML文件...")
    
    try:
        from bs4 import BeautifulSoup
        import re
        from datetime import datetime
        
        # 读取HTML文件
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找消息容器
        messages = []
        
        # 尝试不同的选择器
        # Telegram导出的HTML通常有特定的类名
        message_divs = soup.find_all('div', class_=re.compile(r'message|msg'))
        
        print(f"📊 找到 {len(message_divs)} 个消息元素")
        
        # 如果没有找到，尝试其他方法
        if len(message_divs) == 0:
            # 查找所有包含日期和文本的div
            all_divs = soup.find_all('div')
            print(f"📊 总div数量: {len(all_divs)}")
            
            # 简单提取：查找包含时间的div
            for div in all_divs[:50]:  # 先看前50个
                text = div.get_text(strip=True)
                if re.search(r'\d{1,2}:\d{2}', text) and len(text) < 100:
                    print(f"  可能的消息: {text[:80]}...")
        
        return messages
        
    except ImportError:
        print("❌ 需要BeautifulSoup库，使用简单文本提取")
        
        # 简单文本提取
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取日期和消息的简单方法
        import re
        
        # 查找日期模式
        date_pattern = r'(\d{4}-\d{2}-\d{2})'
        dates = re.findall(date_pattern, content)
        
        print(f"📅 找到 {len(set(dates))} 个不同日期")
        if dates:
            print(f"  最早日期: {min(dates)}")
            print(f"  最晚日期: {max(dates)}")
        
        return []

if __name__ == "__main__":
    file_path = r'C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb'
    
    # 检查文件格式
    file_type = check_file_format(file_path)
    
    if file_type == 'html':
        messages = extract_html_content(file_path)
        print(f"\n✅ HTML文件检查完成")
    else:
        print(f"\n📋 文件类型: {file_type}")