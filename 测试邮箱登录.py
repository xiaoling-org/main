#!/usr/bin/env python3
"""
安全邮箱登录测试脚本
用于验证 xiaoling.assistant@gmail.com 邮箱可用性
"""

import imaplib
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import sys

def print_header():
    """打印标题"""
    print("=" * 60)
    print("小灵同学助理 - 邮箱登录测试")
    print("=" * 60)
    print()

def test_imap_login(email, password):
    """测试IMAP登录"""
    print(f"🔍 测试IMAP登录: {email}")
    
    try:
        # Gmail IMAP设置
        imap_server = "imap.gmail.com"
        imap_port = 993
        
        print(f"  连接服务器: {imap_server}:{imap_port}")
        
        # 建立SSL连接
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=context)
        
        print("  尝试登录...")
        mail.login(email, password)
        print("  ✅ IMAP登录成功!")
        
        # 获取邮箱信息
        status, messages = mail.select("INBOX")
        if status == "OK":
            typ, data = mail.search(None, 'ALL')
            if data[0]:
                msg_count = len(data[0].split())
                print(f"  📧 收件箱中有 {msg_count} 封邮件")
        
        # 列出文件夹（前3个）
        print("  📁 邮箱文件夹:")
        status, folders = mail.list()
        if status == "OK":
            for i, folder in enumerate(folders[:3]):
                print(f"    {i+1}. {folder.decode()}")
            if len(folders) > 3:
                print(f"    ... 还有 {len(folders)-3} 个文件夹")
        
        mail.logout()
        print("  ✅ IMAP测试完成")
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"  ❌ IMAP登录失败: {e}")
        
        # 提供错误解决方案
        error_msg = str(e)
        if "Invalid credentials" in error_msg:
            print("\n  💡 解决方案:")
            print("    1. 确认密码正确")
            print("    2. 前往 https://myaccount.google.com/apppasswords")
            print("    3. 生成应用专用密码")
            print("    4. 使用生成的16位密码")
        elif "Please log in via your web browser" in error_msg:
            print("\n  💡 解决方案:")
            print("    1. 前往 https://myaccount.google.com/lesssecureapps")
            print("    2. 启用'不够安全的应用'访问权限")
            print("    3. 或使用应用专用密码")
        
        return False
    except Exception as e:
        print(f"  ❌ 连接错误: {e}")
        return False

def test_smtp_login(email, password):
    """测试SMTP登录"""
    print(f"\n🔍 测试SMTP登录: {email}")
    
    try:
        # Gmail SMTP设置
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        print(f"  连接服务器: {smtp_server}:{smtp_port}")
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS
        
        print("  尝试登录...")
        server.login(email, password)
        print("  ✅ SMTP登录成功!")
        
        # 测试发送能力（不实际发送）
        print("  📤 发送功能测试...")
        
        # 创建测试邮件
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email  # 发送给自己
        msg['Subject'] = "邮箱连接测试 - 小灵同学助理"
        
        body = """这是一封测试邮件，用于验证邮箱连接是否正常。
        
        如果收到此邮件，说明邮箱配置正确。
        
        发送时间: 测试时间
        发件人: 小灵同学助理
        
        注意：这封邮件仅用于测试，不会实际发送。
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # 验证邮件格式（不实际发送）
        test_message = msg.as_string()
        print(f"  ✅ 邮件格式正确 ({len(test_message)} 字节)")
        
        server.quit()
        print("  ✅ SMTP测试完成")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"  ❌ SMTP认证失败: {e}")
        
        # 提供错误解决方案
        error_code = e.smtp_code
        error_msg = e.smtp_error.decode()
        
        print(f"\n  💡 错误代码: {error_code}")
        print(f"  💡 错误信息: {error_msg}")
        
        if "Application-specific password required" in error_msg:
            print("\n  💡 解决方案:")
            print("    1. 前往 https://myaccount.google.com/apppasswords")
            print("    2. 生成应用专用密码")
            print("    3. 使用生成的16位密码")
        
        return False
    except Exception as e:
        print(f"  ❌ 连接错误: {e}")
        return False

def manual_test_instructions():
    """提供手动测试指导"""
    print("\n" + "=" * 60)
    print("手动测试指导")
    print("=" * 60)
    
    print("\n如果自动测试失败，请按以下步骤手动测试:")
    
    print("\n1. 🌐 网页登录测试")
    print("   访问: https://gmail.com")
    print("   用户名: xiaoling.assistant@gmail.com")
    print("   密码: czp94568")
    print("   确认可以正常登录")
    
    print("\n2. ⚙️ Gmail设置检查")
    print("   a. 启用IMAP:")
    print("      访问: https://mail.google.com/mail/u/0/#settings/fwdandpop")
    print("      启用'IMAP访问'")
    
    print("   b. 应用访问权限:")
    print("      选项A（简单）:")
    print("        访问: https://myaccount.google.com/lesssecureapps")
    print("        启用'不够安全的应用'")
    
    print("      选项B（推荐）:")
    print("        访问: https://myaccount.google.com/apppasswords")
    print("        生成应用专用密码")
    print("        使用16位密码代替常规密码")
    
    print("\n3. 📧 发送测试邮件")
    print("   a. 登录主邮箱")
    print("   b. 发送邮件到备用邮箱: xiao.ling.tongxue@gmail.com")
    print("   c. 登录备用邮箱确认收到")

def main():
    """主函数"""
    print_header()
    
    # 邮箱信息
    email = "xiaoling.assistant@gmail.com"
    
    print(f"📧 测试邮箱: {email}")
    print(f"🔐 密码: {'*' * 8} (已隐藏)")
    print()
    
    # 获取密码
    print("请输入邮箱密码进行测试:")
    password = getpass.getpass("密码: ")
    
    print("\n" + "-" * 60)
    
    # 执行测试
    imap_success = test_imap_login(email, password)
    smtp_success = test_smtp_login(email, password)
    
    print("\n" + "-" * 60)
    print("测试结果汇总:")
    print(f"  IMAP登录: {'✅ 成功' if imap_success else '❌ 失败'}")
    print(f"  SMTP登录: {'✅ 成功' if smtp_success else '❌ 失败'}")
    
    if imap_success and smtp_success:
        print("\n🎉 邮箱测试完全成功！")
        print("小灵同学助理可以正常使用这个邮箱。")
    else:
        print("\n⚠️  邮箱测试部分失败")
        manual_test_instructions()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n测试出错: {e}")
        sys.exit(1)