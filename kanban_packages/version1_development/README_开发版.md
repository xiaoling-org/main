# 小灵同学看板系统 - 完整开发版

## 系统概述
这是一个功能完整的看板系统，包含：
1. **后端服务器**：基于Flask的看板系统，支持WebSocket实时通信
2. **移动端应用**：React Native开发的Android/iOS应用
3. **实时协作**：多用户同时编辑，实时同步更新
4. **标签分类**：智能标签系统，支持自定义标签
5. **搜索过滤**：强大的搜索和过滤功能

## 系统要求
- Python 3.8+
- Node.js 18+
- Android Studio（用于移动端开发）
- 网络环境：局域网访问

## 安装指南

### 1. 后端服务器安装
```bash
# 进入后端目录
cd kanban_packages/version1_development

# 安装Python依赖
pip install -r requirements.txt

# 启动服务器
python kanban_enhanced.py
```

### 2. 移动端开发环境配置
```bash
# 进入移动端目录
cd KanbanMobileApp

# 安装Node.js依赖
npm install

# 配置Android开发环境
# 1. 安装Android Studio
# 2. 配置ANDROID_HOME环境变量
# 3. 安装Android SDK

# 启动开发服务器
npm start

# 在Android模拟器或真机上运行
npm run android
```

## 配置文件

### 服务器配置
- **默认端口**：5000
- **访问地址**：
  - 电脑：http://localhost:5000
  - 手机：http://[电脑IP地址]:5000

### 移动端配置
- **服务器地址**：在`src/services/websocket.js`中配置
- **适配小米15Pro**：已优化屏幕适配和触摸响应

## 功能特性

### 后端功能
✅ 实时任务管理（增删改查）
✅ WebSocket实时通信
✅ 多用户协作
✅ 标签分类系统
✅ 搜索过滤功能
✅ 数据导入导出（JSON/CSV）
✅ 活动日志记录
✅ 用户认证系统

### 移动端功能
✅ 响应式设计，适配各种屏幕
✅ 实时任务同步
✅ 拖拽排序
✅ 离线缓存
✅ 通知提醒
✅ 深色/浅色主题

## 开发指南

### 后端开发
- 主要文件：`kanban_enhanced.py`
- API文档：访问 http://localhost:5000/api/status 查看系统状态
- 数据结构：JSON格式存储在`kanban_data.json`

### 移动端开发
- 技术栈：React Native + TypeScript
- 状态管理：Redux + Zustand
- 网络通信：Axios + Socket.io
- UI框架：React Native Paper

## 小米15Pro优化
1. **屏幕适配**：针对小米15Pro的屏幕尺寸优化
2. **触摸响应**：优化手势识别和拖拽体验
3. **性能优化**：减少内存占用，提升响应速度
4. **网络优化**：优化局域网连接稳定性

## 部署指南

### 生产环境部署
```bash
# 使用Gunicorn部署（Linux）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 kanban_enhanced:app

# 使用Nginx反向代理
# 配置Nginx转发到localhost:5000
```

### 移动端打包
```bash
# Android APK打包
cd KanbanMobileApp/android
./gradlew assembleRelease

# iOS打包
cd KanbanMobileApp/ios
xcodebuild -workspace KanbanMobileApp.xcworkspace -scheme KanbanMobileApp -configuration Release
```

## 故障排除

### 常见问题
1. **服务器无法启动**：检查端口5000是否被占用
2. **手机无法访问**：确保电脑和手机在同一局域网
3. **移动端连接失败**：检查服务器IP地址配置
4. **依赖安装失败**：使用国内镜像源

### 调试工具
- 后端日志：查看控制台输出
- 移动端调试：使用React Native Debugger
- 网络调试：使用Charles或Fiddler

## 更新日志
- v3.0 (2026-02-10)：增强版发布，新增标签分类、搜索过滤、实时评论功能
- v2.0 (2026-02-09)：基础版发布，支持任务管理和移动端访问
- v1.0 (2026-02-08)：初始版本

## 技术支持
如有问题，请联系：
- 开发者：小灵同学助理
- 邮箱：assistant@xiaoling.com
- 更新时间：2026年2月13日