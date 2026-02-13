#!/usr/bin/env python3
"""
直接从HTML文件中提取关键信息
"""

import re

# 读取文件
with open(r'C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb', 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 搜索关键信息...")

# 1. 搜索"彩灵"
print("\n1. 搜索'彩灵':")
cailing_matches = re.findall(r'彩灵', content)
print(f"   找到 {len(cailing_matches)} 次")

# 查找包含"彩灵"的上下文
cailing_context = re.findall(r'.{0,50}彩灵.{0,50}', content)
for ctx in cailing_context[:5]:
    print(f"   ...{ctx}...")

# 2. 搜索"小灵同学"
print("\n2. 搜索'小灵同学':")
xiaoling_matches = re.findall(r'小灵同学', content)
print(f"   找到 {len(xiaoling_matches)} 次")

# 3. 搜索"GitHub"
print("\n3. 搜索'GitHub':")
github_matches = re.findall(r'[Gg]it[Hh]ub', content)
print(f"   找到 {len(github_matches)} 次")

# 查找GitHub用户名
github_context = re.findall(r'github\.com/[^\s<]+', content, re.IGNORECASE)
for ctx in github_context[:5]:
    print(f"   {ctx}")

# 4. 搜索"Mac mini"
print("\n4. 搜索'Mac mini':")
macmini_matches = re.findall(r'[Mm]ac\s*[Mm]ini', content)
print(f"   找到 {len(macmini_matches)} 次")

# 查找Mac mini讨论的日期
macmini_dates = []
for match in re.finditer(r'<div class="pull_date">([^<]+)</div>.*?[Mm]ac\s*[Mm]ini', content, re.DOTALL):
    date = match.group(1)
    macmini_dates.append(date)
    print(f"   在 {date} 讨论了Mac mini")

# 5. 搜索用户信息
print("\n5. 搜索用户信息:")
# 查找用户姓名
user_name_matches = re.findall(r'<div class="from_name">([^<]+)</div>', content)
unique_users = set(user_name_matches)
print(f"   找到 {len(unique_users)} 个不同用户:")
for user in unique_users:
    print(f"   • {user}")

# 6. 提取所有日期
print("\n6. 提取所有日期:")
all_dates = re.findall(r'<div class="pull_date">([^<]+)</div>', content)
unique_dates = set(all_dates)
print(f"   找到 {len(unique_dates)} 个不同日期")
print(f"   最早日期: {min(unique_dates) if unique_dates else '无'}")
print(f"   最晚日期: {max(unique_dates) if unique_dates else '无'}")

# 7. 搜索重要对话
print("\n7. 重要对话片段:")

# 查找包含关键字的对话
keywords = ['名字', '称呼', 'GitHub', 'mac', 'mini', '配置', '第一次', '开始']
for keyword in keywords:
    pattern = rf'.{{0,100}}{keyword}.{{0,100}}'
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f"\n  包含'{keyword}'的对话:")
        for match in matches[:3]:
            # 清理HTML标签
            clean = re.sub(r'<[^>]+>', '', match)
            print(f"   • {clean[:80]}...")

print("\n✅ 关键信息提取完成")