#!/usr/bin/env python3
"""
Gmail邮箱连接测试脚本
用于测试IMAP/SMTP连接是否正常
"""

import imaplib
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

def test_imap_connection(email, password):
    """测试IMAP连接"""
    print(f"测试IMAP连接: {email}")
    
    try:
        # Gmail IMAP服务器
        imap_server = "imap.gmail.com"
        imap_port = 993
        
        # 建立SSL连接
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=context)
        
        # 登录
        mail.login(email, password)
        print("✅ IMAP登录成功")
        
        # 列出邮箱文件夹
        status, folders = mail.list()
        if status == "OK":
            print("✅ 邮箱文件夹列表:")
            for folder in folders[:5]:  # 只显示前5个
                print(f"  - {folder.decode()}")
        
        # 选择收件箱
        mail.select("INBOX")
        
        # 搜索邮件
        status, messages = mail.search(None, 'ALL')
        if status == "OK":
            message_ids = messages[0].split()
            print(f"✅ 收件箱中有 {len(message_ids)} 封邮件")
        
        # 退出
        mail.logout()
        print("✅ IMAP连接测试完成")
        return True
        
    except Exception as e:
        print(f"❌ IMAP连接失败: {e}")
        return False

def test_smtp_connection(email, password):
    """测试SMTP连接"""
    print(f"\n测试SMTP连接: {email}")
    
    try:
        # Gmail SMTP服务器
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # 建立连接
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS
        
        # 登录
        server.login(email, password)
        print("✅ SMTP登录成功")
        
        # 创建测试邮件
        test_email = email  # 发送给自己
        
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = test_email
        msg['Subject'] = "小灵同学助理 - 邮箱连接测试"
        
        body = """
        这是一封测试邮件，用于验证邮箱连接是否正常。
        
        发送时间: 测试时间
        发件人: 小灵同学助理
        收件人: 你自己
        
        如果收到此邮件，说明邮箱配置正确。
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # 发送邮件（注释掉实际发送，只测试连接）
        # server.send_message(msg)
        print("✅ SMTP发送测试通过（未实际发送）")
        
        # 退出
        server.quit()
        print("✅ SMTP连接测试完成")
        return True
        
    except Exception as e:
        print(f"❌ SMTP连接失败: {e}")
        
        # 提供常见错误解决方案
        if "Application-specific password required" in str(e):
            print("\n⚠️  需要应用专用密码")
            print("请前往: https://myaccount.google.com/apppasswords")
            print("1. 生成应用专用密码")
            print("2. 使用生成的密码而不是常规密码")
        elif "Please log in via your web browser" in str(e):
            print("\n⚠️  需要通过网页浏览器登录")
            print("1. 前往 https://myaccount.google.com/lesssecureapps")
            print("2. 启用'不够安全的应用'访问权限")
            print("3. 或使用应用专用密码")
        
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("小灵同学助理 - 邮箱连接测试")
    print("=" * 50)
    
    # 邮箱信息
    email = "xiaoling.assistant@gmail.com"
    
    # 注意：出于安全考虑，这里不直接使用密码
    # 实际测试时需要用户输入密码
    print(f"\n邮箱地址: {email}")
    print("⚠️  出于安全考虑，此脚本不直接使用存储的密码")
    print("如需测试，请手动运行此脚本并输入密码")
    
    print("\n测试步骤:")
    print("1. 手动登录网页版Gmail确认邮箱可用")
    print("2. 检查是否启用了IMAP访问")
    print("3. 检查是否启用了'不够安全的应用'访问")
    print("4. 或设置应用专用密码")
    
    print("\nGmail设置检查:")
    print("1. IMAP设置: https://mail.google.com/mail/u/0/#settings/fwdandpop")
    print("2. 安全性设置: https://myaccount.google.com/security")
    print("3. 应用专用密码: https://myaccount.google.com/apppasswords")
    
    print("\n建议的测试方法:")
    print("1. 手动登录 https://gmail.com")
    print("2. 发送测试邮件到备用邮箱")
    print("3. 检查是否能正常收发邮件")
    
    return True

if __name__ == "__main__":
    main()