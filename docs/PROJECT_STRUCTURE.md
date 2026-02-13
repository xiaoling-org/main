# 项目结构文档

## 目录结构说明

### 根目录
```
GlobalOpportunityMonitor/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── .env.example                 # 环境变量模板
├── .gitignore                   # Git忽略文件
├── pyproject.toml              # Python项目配置
└── setup.py                    # 安装脚本
```

### 源代码目录 (src/)
```
src/
├── __init__.py
├── main.py                     # 应用入口点
├── config.py                   # 配置管理
├── database/
│   ├── __init__.py
│   ├── models.py              # 数据模型定义
│   ├── crud.py                # 数据库操作
│   ├── session.py             # 数据库会话管理
│   └── migrations/            # 数据库迁移
├── collectors/                 # 数据采集模块
│   ├── __init__.py
│   ├── base_collector.py      # 采集器基类
│   ├── github_collector.py    # GitHub数据采集
│   ├── hackernews_collector.py # Hacker News采集
│   ├── news_collector.py      # 新闻采集
│   ├── social_collector.py    # 社交媒体采集
│   └── hongkong_collector.py  # 香港本地采集
├── analyzers/                  # AI分析模块
│   ├── __init__.py
│   ├── base_analyzer.py       # 分析器基类
│   ├── sentiment_analyzer.py  # 情感分析
│   ├── text_analyzer.py       # 文本分析
│   ├── keyword_extractor.py   # 关键词提取
│   └── opportunity_detector.py # 机会检测
├── scoring/                    # 评分系统
│   ├── __init__.py
│   ├── base_scorer.py         # 评分器基类
│   ├── relevance_scorer.py    # 相关性评分
│   ├── popularity_scorer.py   # 流行度评分
│   ├── timeliness_scorer.py   # 时效性评分
│   └── composite_scorer.py    # 综合评分
├── web/                        # Web后端
│   ├── __init__.py
│   ├── api.py                 # API路由
│   ├── schemas.py             # Pydantic模型
│   ├── dependencies.py        # 依赖注入
│   └── middleware.py          # 中间件
├── utils/                      # 工具函数
│   ├── __init__.py
│   ├── logger.py              # 日志配置
│   ├── helpers.py             # 辅助函数
│   ├── validators.py          # 数据验证
│   └── formatters.py          # 数据格式化
└── jobs/                       # 后台任务
    ├── __init__.py
    ├── scheduler.py           # 任务调度
    ├── collector_job.py       # 采集任务
    ├── analyzer_job.py        # 分析任务
    └── backup_job.py          # 备份任务
```

### 配置文件目录 (config/)
```
config/
├── config.example.yaml         # 配置文件模板
├── config.yaml                 # 实际配置文件 (不提交到Git)
├── logging.yaml               # 日志配置
└── models/                    # AI模型配置
    ├── sentiment.yaml
    ├── classification.yaml
    └── keywords.yaml
```

### 数据目录 (data/)
```
data/
├── raw/                       # 原始数据
│   ├── github/
│   ├── hackernews/
│   ├── news/
│   ├── social/
│   └── hongkong/
├── processed/                 # 处理后的数据
│   ├── analyzed/
│   └── scored/
├── models/                    # 本地AI模型
│   ├── sentiment/
│   ├── classification/
│   └── embeddings/
└── backups/                   # 数据备份
```

### Web界面目录 (web_interface/)
```
web_interface/
├── index.html                 # 主页面
├── styles.css                 # 样式表
├── app.js                     # 主应用逻辑
├── components/                # 组件
│   ├── header.js
│   ├── sidebar.js
│   ├── dashboard.js
│   ├── opportunities.js
│   └── charts.js
├── pages/                     # 页面
│   ├── dashboard.html
│   ├── opportunities.html
│   ├── trends.html
│   └── settings.html
└── assets/                    # 静态资源
    ├── images/
    ├── icons/
    └── fonts/
```

### 数据库目录 (database/)
```
database/
├── schema.sql                 # 数据库架构
├── seeds.sql                  # 初始数据
├── queries/                   # 常用查询
│   ├── opportunities.sql
│   ├── trends.sql
│   └── reports.sql
└── migrations/                # 迁移脚本
    ├── 001_initial.sql
    ├── 002_add_scoring.sql
    └── 003_add_categories.sql
```

### 部署目录 (deployment/)
```
deployment/
├── docker/
│   ├── Dockerfile            # Docker镜像配置
│   ├── docker-compose.yml    # 多容器配置
│   └── nginx/
│       ├── nginx.conf
│       └── ssl/
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── restore.sh
└── monitoring/
    ├── prometheus.yml
    ├── grafana/
    └── alerts.yml
```

### 脚本目录 (scripts/)
```
scripts/
├── setup.sh                   # 环境设置脚本
├── run_collector.py          # 运行数据采集
├── run_analyzer.py           # 运行AI分析
├── run_web.py                # 运行Web服务
├── run_all.py                # 运行所有服务
├── backup.py                 # 数据备份
├── restore.py                # 数据恢复
└── test_api.py               # API测试
```

### 测试目录 (tests/)
```
tests/
├── __init__.py
├── conftest.py               # 测试配置
├── test_collectors/          # 采集器测试
│   ├── test_github.py
│   ├── test_hackernews.py
│   └── test_base.py
├── test_analyzers/           # 分析器测试
│   ├── test_sentiment.py
│   ├── test_keywords.py
│   └── test_opportunity.py
├── test_scoring/             # 评分系统测试
│   ├── test_relevance.py
│   ├── test_popularity.py
│   └── test_composite.py
├── test_web/                 # Web测试
│   ├── test_api.py
│   └── test_schemas.py
├── test_database/            # 数据库测试
│   ├── test_models.py
│   └── test_crud.py
└── integration/              # 集成测试
    ├── test_workflow.py
    └── test_end_to_end.py
```

### 文档目录 (docs/)
```
docs/
├── PROJECT_STRUCTURE.md      # 项目结构文档
├── ARCHITECTURE.md           # 系统架构文档
├── API_DOCUMENTATION.md      # API文档
├── USER_GUIDE.md             # 用户指南
├── DEVELOPER_GUIDE.md        # 开发者指南
├── DEPLOYMENT_GUIDE.md       # 部署指南
├── DATA_SOURCES.md           # 数据源说明
├── AI_MODELS.md              # AI模型说明
└── TROUBLESHOOTING.md        # 故障排除
```

## 文件命名规范

### Python文件
- 使用小写字母和下划线：`module_name.py`
- 类名使用驼峰命名法：`ClassName`
- 函数名使用小写字母和下划线：`function_name`

### 配置文件
- 使用小写字母和连字符：`config-name.yaml`
- 环境变量使用大写字母和下划线：`ENV_VARIABLE_NAME`

### 数据库文件
- SQL文件使用小写字母和下划线：`table_name.sql`
- 迁移文件使用数字前缀：`001_initial.sql`

### 测试文件
- 测试文件以`test_`开头：`test_module.py`
- 测试类以`Test`开头：`TestClassName`
- 测试函数以`test_`开头：`test_function_name`

## 代码组织原则

### 模块化设计
- 每个模块有明确的单一职责
- 模块之间通过接口通信
- 避免循环依赖

### 配置管理
- 所有配置集中管理
- 支持环境特定的配置
- 敏感信息通过环境变量管理

### 错误处理
- 统一的错误处理机制
- 详细的错误日志
- 友好的用户错误信息

### 日志记录
- 结构化日志记录
- 不同级别的日志输出
- 日志轮转和归档

### 测试覆盖
- 单元测试覆盖核心逻辑
- 集成测试验证模块协作
- 端到端测试验证完整流程