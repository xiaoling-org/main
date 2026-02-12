#!/usr/bin/env python3
"""
项目分析脚本
用于分析LotteryAnalysisTool和OmniMarket-Financial-Monitor项目
"""

import os
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys

class ProjectAnalyzer:
    def __init__(self):
        self.base_dir = Path("C:/Users/czp/openclaw/projects/github")
        self.results = {}
        
    def analyze_project(self, project_name):
        """分析单个项目"""
        print(f"\n🔍 开始分析项目: {project_name}")
        print("=" * 60)
        
        project_path = self.base_dir / project_name
        if not project_path.exists():
            print(f"❌ 项目目录不存在: {project_path}")
            return None
        
        result = {
            "project_name": project_name,
            "analysis_time": datetime.now().isoformat(),
            "project_path": str(project_path),
            "file_stats": {},
            "structure": {},
            "tech_stack": {},
            "issues": [],
            "recommendations": []
        }
        
        # 1. 基本文件统计
        result["file_stats"] = self.analyze_file_stats(project_path)
        
        # 2. 项目结构分析
        result["structure"] = self.analyze_structure(project_path)
        
        # 3. 技术栈分析
        result["tech_stack"] = self.analyze_tech_stack(project_path)
        
        # 4. 问题识别
        result["issues"] = self.identify_issues(project_path, result)
        
        # 5. 改进建议
        result["recommendations"] = self.generate_recommendations(result)
        
        self.results[project_name] = result
        return result
    
    def analyze_file_stats(self, project_path):
        """分析文件统计"""
        stats = {
            "total_files": 0,
            "total_size_mb": 0,
            "file_types": {},
            "largest_files": []
        }
        
        try:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = Path(root) / file
                    stats["total_files"] += 1
                    
                    # 文件大小
                    try:
                        file_size = file_path.stat().st_size
                        stats["total_size_mb"] += file_size / (1024 * 1024)
                    except:
                        pass
                    
                    # 文件类型统计
                    ext = file_path.suffix.lower()
                    if ext:
                        stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                    else:
                        stats["file_types"]["no_extension"] = stats["file_types"].get("no_extension", 0) + 1
                    
                    # 记录大文件
                    if file_size > 1024 * 1024:  # 大于1MB
                        stats["largest_files"].append({
                            "path": str(file_path.relative_to(project_path)),
                            "size_mb": round(file_size / (1024 * 1024), 2)
                        })
            
            stats["total_size_mb"] = round(stats["total_size_mb"], 2)
            # 只保留前10个大文件
            stats["largest_files"] = sorted(stats["largest_files"], key=lambda x: x["size_mb"], reverse=True)[:10]
            
        except Exception as e:
            print(f"文件统计错误: {e}")
        
        return stats
    
    def analyze_structure(self, project_path):
        """分析项目结构"""
        structure = {
            "directories": [],
            "key_files": [],
            "readme_exists": False,
            "gitignore_exists": False,
            "requirements_exists": False
        }
        
        try:
            # 检查关键文件
            key_files = ["README.md", "README.txt", "README", "readme.md"]
            req_files = ["requirements.txt", "Pipfile", "pyproject.toml", "package.json"]
            
            for item in project_path.iterdir():
                if item.is_dir():
                    structure["directories"].append(item.name)
                else:
                    structure["key_files"].append(item.name)
                    
                    # 检查README
                    if item.name.lower() in [f.lower() for f in key_files]:
                        structure["readme_exists"] = True
                    
                    # 检查.gitignore
                    if item.name == ".gitignore":
                        structure["gitignore_exists"] = True
                    
                    # 检查依赖文件
                    if item.name.lower() in [f.lower() for f in req_files]:
                        structure["requirements_exists"] = True
            
            # 只显示前10个目录和文件
            structure["directories"] = structure["directories"][:10]
            structure["key_files"] = structure["key_files"][:15]
            
        except Exception as e:
            print(f"结构分析错误: {e}")
        
        return structure
    
    def analyze_tech_stack(self, project_path):
        """分析技术栈"""
        tech_stack = {
            "languages": {},
            "frameworks": [],
            "databases": [],
            "tools": []
        }
        
        try:
            # 通过文件扩展名识别语言
            ext_to_lang = {
                ".py": "Python",
                ".js": "JavaScript",
                ".ts": "TypeScript",
                ".java": "Java",
                ".cpp": "C++",
                ".c": "C",
                ".cs": "C#",
                ".go": "Go",
                ".rs": "Rust",
                ".php": "PHP",
                ".html": "HTML",
                ".css": "CSS",
                ".sql": "SQL",
                ".json": "JSON",
                ".yml": "YAML",
                ".yaml": "YAML",
                ".toml": "TOML",
                ".md": "Markdown",
                ".txt": "Text"
            }
            
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext in ext_to_lang:
                        lang = ext_to_lang[ext]
                        tech_stack["languages"][lang] = tech_stack["languages"].get(lang, 0) + 1
            
            # 检查框架和工具
            framework_indicators = {
                "django": ["settings.py", "urls.py", "wsgi.py"],
                "flask": ["app.py", "flask_app.py"],
                "react": ["package.json", "node_modules"],
                "vue": ["vue.config.js"],
                "angular": ["angular.json"],
                "spring": ["pom.xml", "build.gradle"],
                "express": ["package.json"],
                "fastapi": ["main.py"]
            }
            
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_lower = file.lower()
                    
                    # 检查数据库
                    if "sqlite" in file_lower:
                        tech_stack["databases"].append("SQLite")
                    elif "postgres" in file_lower:
                        tech_stack["databases"].append("PostgreSQL")
                    elif "mysql" in file_lower:
                        tech_stack["databases"].append("MySQL")
                    elif "mongodb" in file_lower:
                        tech_stack["databases"].append("MongoDB")
                    
                    # 检查工具
                    if "docker" in file_lower:
                        tech_stack["tools"].append("Docker")
                    elif "dockerfile" in file_lower:
                        tech_stack["tools"].append("Docker")
                    elif "docker-compose" in file_lower:
                        tech_stack["tools"].append("Docker Compose")
            
            # 去重
            tech_stack["databases"] = list(set(tech_stack["databases"]))
            tech_stack["tools"] = list(set(tech_stack["tools"]))
            
        except Exception as e:
            print(f"技术栈分析错误: {e}")
        
        return tech_stack
    
    def identify_issues(self, project_path, analysis_result):
        """识别问题"""
        issues = []
        
        try:
            # 检查README
            if not analysis_result["structure"]["readme_exists"]:
                issues.append({
                    "type": "documentation",
                    "severity": "medium",
                    "description": "缺少README文档",
                    "suggestion": "创建README.md文件，描述项目用途、安装和使用方法"
                })
            
            # 检查.gitignore
            if not analysis_result["structure"]["gitignore_exists"]:
                issues.append({
                    "type": "best_practice",
                    "severity": "low",
                    "description": "缺少.gitignore文件",
                    "suggestion": "创建.gitignore文件，排除不必要的文件"
                })
            
            # 检查依赖管理
            if not analysis_result["structure"]["requirements_exists"]:
                issues.append({
                    "type": "dependency",
                    "severity": "medium",
                    "description": "缺少依赖管理文件",
                    "suggestion": "添加requirements.txt或类似文件管理依赖"
                })
            
            # 检查大文件
            large_files = analysis_result["file_stats"]["largest_files"]
            if large_files:
                for file_info in large_files[:3]:  # 只显示前3个大文件
                    issues.append({
                        "type": "performance",
                        "severity": "low",
                        "description": f"发现大文件: {file_info['path']} ({file_info['size_mb']}MB)",
                        "suggestion": "考虑是否可以将大文件分割或压缩"
                    })
            
            # 检查代码文件比例
            total_files = analysis_result["file_stats"]["total_files"]
            code_files = sum(count for ext, count in analysis_result["file_stats"]["file_types"].items() 
                           if ext in [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".php"])
            
            if total_files > 0:
                code_ratio = code_files / total_files
                if code_ratio < 0.1:  # 代码文件比例低于10%
                    issues.append({
                        "type": "structure",
                        "severity": "low",
                        "description": f"代码文件比例较低 ({code_ratio:.1%})",
                        "suggestion": "检查项目结构，确保代码文件组织合理"
                    })
            
        except Exception as e:
            print(f"问题识别错误: {e}")
        
        return issues
    
    def generate_recommendations(self, analysis_result):
        """生成改进建议"""
        recommendations = []
        
        try:
            project_name = analysis_result["project_name"]
            
            # 基础建议
            recommendations.append({
                "priority": "high",
                "category": "documentation",
                "description": "完善项目文档",
                "action": "创建完整的README.md，包括项目介绍、安装步骤、使用示例"
            })
            
            # 根据项目类型给出建议
            if "彩票" in project_name.lower() or "lottery" in project_name.lower():
                recommendations.append({
                    "priority": "medium",
                    "category": "feature",
                    "description": "增强数据分析功能",
                    "action": "添加更多数据分析算法和可视化图表"
                })
            
            if "金融" in project_name.lower() or "financial" in project_name.lower() or "market" in project_name.lower():
                recommendations.append({
                    "priority": "high",
                    "category": "security",
                    "description": "加强数据安全",
                    "action": "添加数据加密和访问控制机制"
                })
            
            # 技术栈建议
            languages = list(analysis_result["tech_stack"]["languages"].keys())
            if "Python" in languages:
                recommendations.append({
                    "priority": "medium",
                    "category": "development",
                    "description": "添加测试框架",
                    "action": "配置pytest或unittest，添加单元测试"
                })
            
            if "JavaScript" in languages or "TypeScript" in languages:
                recommendations.append({
                    "priority": "medium",
                    "category": "development",
                    "description": "添加代码检查",
                    "action": "配置ESLint或Prettier，统一代码风格"
                })
            
            # 部署建议
            recommendations.append({
                "priority": "low",
                "category": "deployment",
                "description": "简化部署流程",
                "action": "创建部署脚本或Docker配置"
            })
            
        except Exception as e:
            print(f"建议生成错误: {e}")
        
        return recommendations
    
    def print_summary(self, result):
        """打印分析摘要"""
        print(f"\n📊 项目: {result['project_name']}")
        print(f"📅 分析时间: {result['analysis_time']}")
        print(f"📁 项目路径: {result['project_path']}")
        
        # 文件统计
        stats = result['file_stats']
        print(f"\n📈 文件统计:")
        print(f"   总文件数: {stats['total_files']}")
        print(f"   总大小: {stats['total_size_mb']} MB")
        
        if stats['file_types']:
            print(f"   文件类型分布:")
            for ext, count in sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"     {ext}: {count} 个")
        
        # 技术栈
        tech = result['tech_stack']
        if tech['languages']:
            print(f"\n💻 技术栈:")
            print(f"   编程语言: {', '.join(tech['languages'].keys())}")
        
        if tech['databases']:
            print(f"   数据库: {', '.join(tech['databases'])}")
        
        if tech['tools']:
            print(f"   工具: {', '.join(tech['tools'])}")
        
        # 问题
        if result['issues']:
            print(f"\n⚠️  发现的问题 ({len(result['issues'])}个):")
            for i, issue in enumerate(result['issues'][:3], 1):  # 只显示前3个
                print(f"   {i}. [{issue['severity'].upper()}] {issue['description']}")
        
        # 建议
        if result['recommendations']:
            print(f"\n💡 改进建议 ({len(result['recommendations'])}个):")
            for i, rec in enumerate(result['recommendations'][:3], 1):  # 只显示前3个
                print(f"   {i}. [{rec['priority'].upper()}] {rec['description']}")
        
        print("\n" + "=" * 60)
    
    def save_results(self):
        """保存分析结果"""
        output_dir = Path("C:/Users/czp/openclaw/projects/analysis")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON格式的详细结果
        json_path = output_dir / f"project_analysis_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # 保存文本格式的摘要
        txt_path = output_dir / f"project_summary_{timestamp}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"项目分析报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for project_name, result in self.results.items():
                f.write(f"项目: {project_name}\n")
                f.write(f"分析时间: {result['analysis_time']}\n")
                f.write(f"文件数: {result['file_stats']['total_files']}\n")
                f.write(f"大小: {result['file_stats']['total_size_mb']} MB\n")
                
                if result['issues']:
                    f.write(f"发现问题: {len(result['issues'])}个\n")
                
                if result['recommendations']:
                    f.write(f"改进建议: {len(result['recommendations'])}个\n")
                
                f.write("\n" + "-" * 40 + "\n\n")
        
        print(f"\n💾 分析结果已保存:")
        print(f"   详细结果: {json_path}")
        print(f"   摘要报告: {txt_path}")
        
        return str(json_path), str(txt_path)
    
    def run_analysis(self):
        """运行完整分析"""
        print("🚀 开始项目分析")
        print("=" * 60)
        
        projects = ["LotteryAnalysisTool", "OmniMarket-Financial-Monitor"]
        
        for project in projects:
            result = self.analyze_project(project)
            if result:
                self.print_summary(result)
        
        # 保存结果
        json_path, txt_path = self.save_results()
        
        print("\n🎉 项目分析完成!")
        print("=" * 60)
        
        return self.results

def main():
    """主函数"""
    try:
        analyzer = ProjectAnalyzer()
        results = analyzer.run_analysis()
        
        print("\n📋 下一步建议:")
        print("1. 查看详细分析报告了解具体问题")
        print("2. 根据优先级实施改进建议")
        print("3. 定期进行代码审查和优化")
        print("4. 考虑添加自动化测试和部署")
        
        return 0
        
    except Exception as e:
        print(f"分析出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())