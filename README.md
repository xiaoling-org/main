# 全球机会监控系统 (Global Opportunity Monitor)

## 项目概述

这是一个为陈先生开发的全球机会监控系统原型，旨在监控三大方向的机会：
1. 创新技术监控（GitHub/Hacker News）
2. 消费趋势监控（TikTok/电商平台）
3. 香港本地机会监控（本地论坛）

## 系统架构

### 核心模块
- **数据采集模块**：支持三大方向的数据采集
- **AI分析引擎**：文本分析、情感分析、机会识别
- **评分系统**：机会评分和优先级排序
- **Web界面**：数据可视化展示
- **数据库系统**：数据存储和管理

### 技术栈
- **后端**: Python + FastAPI
- **前端**: HTML/CSS/JavaScript + Chart.js
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **AI分析**: Transformers库 + 预训练模型
- **数据采集**: Requests + BeautifulSoup + API客户端

## 快速开始

### 1. 环境设置
```bash
# 克隆项目
git clone <repository-url>

# 进入项目目录
cd GlobalOpportunityMonitor

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置系统
```bash
# 复制配置文件模板
cp config/config.example.yaml config/config.yaml

# 编辑配置文件
# 添加API密钥和其他配置
```

### 3. 运行系统
```bash
# 启动数据采集
python scripts/run_collector.py

# 启动AI分析
python scripts/run_analyzer.py

# 启动Web界面
python scripts/run_web.py
```

## 项目结构

```
GlobalOpportunityMonitor/
├── src/                    # 源代码
│   ├── collectors/         # 数据采集模块
│   ├── analyzers/         # AI分析模块
│   ├── scoring/           # 评分系统
│   ├── database/          # 数据库操作
│   └── web/               # Web后端
├── web_interface/         # 前端界面
├── config/               # 配置文件
├── data/                 # 数据存储
├── logs/                 # 日志文件
├── tests/                # 测试代码
├── deployment/           # 部署配置
├── scripts/              # 运行脚本
└── docs/                 # 文档
```

## 功能特性

### 第一阶段功能 (1-2周)
- [x] 项目基础结构搭建
- [x] 核心数据采集模块
- [x] 基础AI分析引擎
- [x] 机会评分系统原型
- [x] 简单Web界面展示
- [x] 数据库和存储系统
- [x] 部署和运行脚本
- [x] 技术文档和使用指南

### 数据源支持
1. **创新技术**:
   - GitHub Trending Repositories
   - Hacker News Top Stories
   - TechCrunch最新文章

2. **消费趋势**:
   - TikTok热门话题
   - 电商平台热销商品
   - 社交媒体趋势

3. **香港本地机会**:
   - 本地论坛热门讨论
   - 香港新闻媒体
   - 本地商业机会

## 配置说明

### 必需配置
1. **API密钥**:
   - GitHub API Token (可选)
   - 新闻API密钥
   - 社交媒体API密钥

2. **数据库配置**:
   - SQLite (默认，无需配置)
   - PostgreSQL (生产环境)

3. **分析模型**:
   - 预训练情感分析模型
   - 文本分类模型
   - 关键词提取模型

## 使用指南

### 数据采集
系统支持定时采集和手动触发两种模式：
```bash
# 定时采集 (每6小时)
python src/collectors/scheduler.py

# 手动采集特定数据源
python src/collectors/github_collector.py
python src/collectors/hackernews_collector.py
```

### 数据分析
AI分析引擎自动处理采集的数据：
- 文本情感分析
- 机会关键词提取
- 趋势识别
- 相关性评分

### 结果查看
通过Web界面查看分析结果：
- 机会仪表板
- 趋势图表
- 详细报告
- 导出功能

## 开发计划

### 第一阶段 (已完成)
- 基础架构搭建
- 核心功能实现
- 原型系统部署

### 第二阶段 (规划中)
- 高级AI分析功能
- 实时数据流处理
- 移动端应用
- 多语言支持

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题或建议，请联系项目维护者。