import re

# 读取文件
with open(r'C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb', 'r', encoding='utf-8') as f:
    content = f.read()

print("搜索关键信息...")

# 搜索各种关键词
keywords = ['彩灵', '小灵同学', 'GitHub', 'github', 'Mac mini', 'mac mini', '陈志标', 'czp']

for keyword in keywords:
    count = len(re.findall(keyword, content, re.IGNORECASE))
    if count > 0:
        print(f"'{keyword}': {count} 次")
        
        # 显示一些上下文
        matches = re.finditer(keyword, content, re.IGNORECASE)
        for i, match in enumerate(matches):
            if i >= 2:  # 只显示前2个
                break
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end]
            # 清理HTML标签
            context = re.sub(r'<[^>]+>', ' ', context)
            context = re.sub(r'\s+', ' ', context)
            print(f"  上下文: ...{context.strip()}...")

print("\n提取日期信息...")
# 提取所有日期
dates = re.findall(r'title="(\d{2}\.\d{2}\.\d{4})', content)
if dates:
    print(f"最早日期: {min(dates)}")
    print(f"最晚日期: {max(dates)}")
    print(f"总消息数: {len(dates)}")