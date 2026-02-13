print("测试Python运行...")
print("当前目录:", __file__)

# 尝试读取文件
import os
filepath = r'C:\Users\czp\.openclaw\media\inbound\c4439bcc-0a0a-4b88-82c4-951afe98e1fb'

if os.path.exists(filepath):
    print("✅ 文件存在")
    size = os.path.getsize(filepath)
    print(f"文件大小: {size} 字节")
else:
    print("❌ 文件不存在")