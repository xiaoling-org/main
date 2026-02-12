# React Native 开发环境安装指南

## 📋 安装前准备
1. **管理员权限**：需要以管理员身份运行安装程序
2. **网络连接**：需要下载约 5GB 的文件
3. **磁盘空间**：需要至少 10GB 可用空间

## 🚀 安装步骤

### 步骤1：安装 Java JDK 17
1. 下载 Amazon Corretto 17：
   - 地址：https://corretto.aws/downloads/latest/amazon-corretto-17-x64-windows-jdk.msi
2. 运行安装程序
3. 默认设置，一路下一步

### 步骤2：安装 Android Studio
1. 下载 Android Studio：
   - 地址：https://redirector.gvt1.com/edgedl/android/studio/install/2023.3.1.19/android-studio-2023.3.1.19-windows.exe
2. 运行安装程序
3. 选择"Standard"安装
4. 安装完成后，启动 Android Studio
5. 完成初始设置，安装 Android SDK

### 步骤3：设置环境变量
1. 打开"系统属性" → "高级" → "环境变量"
2. **新建系统变量**：
   - 变量名：`JAVA_HOME`
   - 变量值：`C:\Program Files\Amazon Corretto\jdk17.0.0_35`
3. **新建系统变量**：
   - 变量名：`ANDROID_HOME`
   - 变量值：`C:\Users\%USERNAME%\AppData\Local\Android\Sdk`
4. **编辑 Path 变量**，添加：
   - `%JAVA_HOME%\bin`
   - `%ANDROID_HOME%\platform-tools`
   - `%ANDROID_HOME%\tools`
   - `%ANDROID_HOME%\tools\bin`

### 步骤4：安装 React Native CLI
1. 以管理员身份打开命令提示符
2. 运行：
   ```cmd
   npm install -g react-native-cli
   ```

### 步骤5：验证安装
打开新的命令提示符，运行：
```cmd
java -version
adb --version
react-native --version
```

## ⚡ 快速安装脚本
如果你信任自动化脚本，可以运行：
1. 以管理员身份打开 PowerShell
2. 运行：
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/react-native-community/rn-diff-purge/master/scripts/install.ps1'))
   ```

## 🔧 故障排除

### 常见问题1：Java未识别
- 检查 JAVA_HOME 环境变量
- 重启命令提示符

### 常见问题2：adb未找到
- 检查 ANDROID_HOME 环境变量
- 确保 Android SDK Platform-Tools 已安装

### 常见问题3：React Native命令失败
- 确保 Node.js 版本 >= 18
- 尝试：`npm cache clean --force`

## 📱 创建第一个React Native项目
安装完成后，运行：
```cmd
npx react-native init KanbanMobileApp
cd KanbanMobileApp
npx react-native run-android
```

## 📞 需要帮助？
联系小灵同学助理！ 🎯