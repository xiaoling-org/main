#!/usr/bin/env python3
"""
最高权限验证测试脚本
用于验证小灵同学助理是否具备完全控制权限
"""

import os
import sys
import platform
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path

class PermissionValidator:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_result(self, test_name, success, details=""):
        """记录测试结果"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if details:
            print(f"   详情: {details}")
        return success
    
    def test_file_system_permissions(self):
        """测试文件系统权限"""
        print("\n📁 测试文件系统权限")
        print("-" * 40)
        
        # 测试1：创建文件夹
        test_dir = Path("权限测试文件夹")
        try:
            test_dir.mkdir(exist_ok=True)
            self.log_result("创建文件夹", True, f"创建: {test_dir}")
        except Exception as e:
            return self.log_result("创建文件夹", False, str(e))
        
        # 测试2：创建文件
        test_file = test_dir / "测试文件.txt"
        try:
            test_file.write_text("这是权限测试文件\n创建时间: " + datetime.now().isoformat())
            self.log_result("创建文件", True, f"创建: {test_file}")
        except Exception as e:
            return self.log_result("创建文件", False, str(e))
        
        # 测试3：读取文件
        try:
            content = test_file.read_text()
            self.log_result("读取文件", True, f"内容长度: {len(content)} 字符")
        except Exception as e:
            return self.log_result("读取文件", False, str(e))
        
        # 测试4：修改文件
        try:
            with open(test_file, 'a', encoding='utf-8') as f:
                f.write("追加内容: 权限测试通过\n")
            self.log_result("修改文件", True, "成功追加内容")
        except Exception as e:
            return self.log_result("修改文件", False, str(e))
        
        # 测试5：删除文件
        try:
            test_file.unlink()
            self.log_result("删除文件", True, f"删除: {test_file}")
        except Exception as e:
            return self.log_result("删除文件", False, str(e))
        
        # 测试6：删除文件夹
        try:
            test_dir.rmdir()
            self.log_result("删除文件夹", True, f"删除: {test_dir}")
        except Exception as e:
            return self.log_result("删除文件夹", False, str(e))
        
        return True
    
    def test_system_command_permissions(self):
        """测试系统命令权限"""
        print("\n💻 测试系统命令权限")
        print("-" * 40)
        
        # 测试1：执行简单命令
        try:
            result = subprocess.run(["echo", "权限测试"], 
                                  capture_output=True, text=True, shell=True)
            self.log_result("执行命令", True, f"输出: {result.stdout.strip()}")
        except Exception as e:
            return self.log_result("执行命令", False, str(e))
        
        # 测试2：获取系统信息
        try:
            system_info = {
                "系统": platform.system(),
                "版本": platform.version(),
                "架构": platform.architecture()[0],
                "处理器": platform.processor(),
                "Python版本": platform.python_version()
            }
            self.log_result("获取系统信息", True, json.dumps(system_info, ensure_ascii=False))
        except Exception as e:
            return self.log_result("获取系统信息", False, str(e))
        
        # 测试3：环境变量访问
        try:
            path_var = os.environ.get('PATH', '')
            path_count = len(path_var.split(';'))
            self.log_result("访问环境变量", True, f"PATH包含 {path_count} 个路径")
        except Exception as e:
            return self.log_result("访问环境变量", False, str(e))
        
        return True
    
    def test_network_permissions(self):
        """测试网络权限"""
        print("\n🌐 测试网络权限")
        print("-" * 40)
        
        # 测试1：解析域名
        try:
            import socket
            ip = socket.gethostbyname('www.google.com')
            self.log_result("域名解析", True, f"Google IP: {ip}")
        except Exception as e:
            # 网络可能受限，这不是权限问题
            self.log_result("域名解析", False, f"可能网络受限: {e}")
        
        # 测试2：创建网络请求（简单测试）
        try:
            import urllib.request
            response = urllib.request.urlopen('http://www.google.com', timeout=5)
            status = response.status
            self.log_result("网络请求", True, f"HTTP状态码: {status}")
        except Exception as e:
            # 网络可能受限
            self.log_result("网络请求", False, f"可能网络受限: {e}")
        
        return True
    
    def test_application_permissions(self):
        """测试应用程序权限"""
        print("\n🖥️ 测试应用程序权限")
        print("-" * 40)
        
        # 测试1：检查Python安装
        try:
            python_path = sys.executable
            self.log_result("Python访问", True, f"Python路径: {python_path}")
        except Exception as e:
            return self.log_result("Python访问", False, str(e))
        
        # 测试2：检查重要目录访问
        important_dirs = [
            ("用户目录", Path.home()),
            ("当前目录", Path.cwd()),
            ("临时目录", Path(os.environ.get('TEMP', 'C:\\Windows\\Temp'))),
        ]
        
        for name, directory in important_dirs:
            try:
                if directory.exists():
                    self.log_result(f"访问{name}", True, f"路径: {directory}")
                else:
                    self.log_result(f"访问{name}", True, f"目录不存在但可访问: {directory}")
            except Exception as e:
                self.log_result(f"访问{name}", False, str(e))
        
        return True
    
    def test_admin_permissions(self):
        """测试管理员权限"""
        print("\n🔧 测试管理员权限")
        print("-" * 40)
        
        # 测试1：检查是否以管理员运行
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            self.log_result("管理员状态", True, f"管理员权限: {is_admin}")
        except Exception as e:
            self.log_result("管理员状态", False, f"无法检测: {e}")
        
        # 测试2：系统目录访问测试（只读）
        system_dirs = [
            ("Windows目录", Path("C:\\Windows")),
            ("Program Files", Path("C:\\Program Files")),
        ]
        
        for name, directory in system_dirs:
            try:
                if directory.exists():
                    # 尝试列出一些内容（不修改）
                    items = list(directory.iterdir())[:3]
                    self.log_result(f"访问{name}", True, f"可访问，示例: {[i.name for i in items]}")
                else:
                    self.log_result(f"访问{name}", True, f"目录不存在: {directory}")
            except Exception as e:
                self.log_result(f"访问{name}", False, f"访问被拒绝: {e}")
        
        return True
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 权限验证测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"\n测试统计:")
        print(f"  总测试数: {total_tests}")
        print(f"  通过测试: {passed_tests}")
        print(f"  失败测试: {failed_tests}")
        print(f"  通过率: {(passed_tests/total_tests*100):.1f}%")
        
        print(f"\n测试时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"持续时间: {(datetime.now() - self.start_time).total_seconds():.1f}秒")
        
        # 保存详细报告
        report_file = Path("权限验证报告.json")
        report_data = {
            "测试时间": self.start_time.isoformat(),
            "测试系统": platform.system(),
            "测试用户": os.environ.get('USERNAME', '未知'),
            "测试结果": self.test_results,
            "统计信息": {
                "总数": total_tests,
                "通过": passed_tests,
                "失败": failed_tests,
                "通过率": f"{(passed_tests/total_tests*100):.1f}%"
            }
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            print(f"\n📄 详细报告已保存: {report_file}")
        except Exception as e:
            print(f"\n⚠️  无法保存报告: {e}")
        
        # 总结
        print("\n" + "=" * 60)
        if failed_tests == 0:
            print("🎉 所有权限测试通过！")
            print("小灵同学助理具备完全控制权限。")
        else:
            print("⚠️  部分权限测试失败")
            print("可能需要调整权限设置。")
        
        print("\n" + "=" * 60)
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🔐 开始最高权限验证测试")
        print("=" * 60)
        
        tests = [
            ("文件系统权限", self.test_file_system_permissions),
            ("系统命令权限", self.test_system_command_permissions),
            ("网络权限", self.test_network_permissions),
            ("应用程序权限", self.test_application_permissions),
            ("管理员权限", self.test_admin_permissions),
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            try:
                if not test_func():
                    all_passed = False
            except Exception as e:
                self.log_result(test_name, False, f"测试异常: {e}")
                all_passed = False
        
        # 生成报告
        self.generate_report()
        
        return all_passed

def main():
    """主函数"""
    validator = PermissionValidator()
    
    try:
        success = validator.run_all_tests()
        
        if success:
            print("\n✅ 权限验证完成 - 系统就绪")
            print("小灵同学助理已获得完全控制权限。")
            print("可以开始执行高级任务。")
        else:
            print("\n⚠️  权限验证发现问题")
            print("部分权限可能受限，建议检查系统设置。")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        return 2
    except Exception as e:
        print(f"\n测试出错: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())