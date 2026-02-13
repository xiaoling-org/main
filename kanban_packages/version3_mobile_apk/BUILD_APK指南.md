# Android APK 构建指南

## 环境要求

### 1. 开发环境
- Node.js 18+
- Java JDK 11+
- Android Studio
- Android SDK

### 2. 系统要求
- Windows 10/11, macOS, Linux
- 至少8GB RAM
- 20GB可用磁盘空间

## 安装步骤

### 步骤1：安装Node.js
1. 下载Node.js 18+：https://nodejs.org/
2. 安装时勾选"Add to PATH"
3. 验证安装：
   ```bash
   node --version
   npm --version
   ```

### 步骤2：安装Java JDK
1. 下载JDK 11+：https://adoptium.net/
2. 设置JAVA_HOME环境变量
3. 验证安装：
   ```bash
   java --version
   ```

### 步骤3：安装Android Studio
1. 下载Android Studio：https://developer.android.com/studio
2. 安装时选择"Standard"安装
3. 安装Android SDK和必要的组件

### 步骤4：配置环境变量
```bash
# Windows
set ANDROID_HOME=C:\Users\用户名\AppData\Local\Android\Sdk
set PATH=%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%PATH%

# macOS/Linux
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$PATH
```

## 构建APK

### 方法一：使用React Native CLI（推荐）

#### 1. 准备项目
```bash
# 进入移动端项目目录
cd KanbanMobileApp

# 安装依赖
npm install

# 安装Android依赖
cd android
./gradlew clean
```

#### 2. 生成签名密钥（首次构建）
```bash
# 生成密钥库
keytool -genkeypair -v -keystore kanban-release-key.keystore -alias kanban-key-alias -keyalg RSA -keysize 2048 -validity 10000

# 按照提示输入信息：
# 密钥库密码：设置密码
# 名字与姓氏：您的姓名
# 组织单位：您的组织
# 组织名称：您的公司
# 城市或区域：所在城市
# 州或省份：所在省份
# 国家代码：CN
```

#### 3. 配置gradle
在`android/app/build.gradle`中添加：
```gradle
android {
    signingConfigs {
        release {
            storeFile file('kanban-release-key.keystore')
            storePassword '您的密码'
            keyAlias 'kanban-key-alias'
            keyPassword '您的密码'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

#### 4. 构建APK
```bash
# 进入android目录
cd android

# 清理项目
./gradlew clean

# 构建Release APK
./gradlew assembleRelease

# 构建完成后，APK文件位于：
# android/app/build/outputs/apk/release/app-release.apk
```

### 方法二：使用Android Studio

#### 1. 导入项目
1. 打开Android Studio
2. 选择"Open an existing project"
3. 选择`KanbanMobileApp/android`目录
4. 等待Gradle同步完成

#### 2. 配置构建
1. 点击菜单 Build > Generate Signed Bundle / APK
2. 选择APK
3. 选择或创建密钥库
4. 配置签名信息

#### 3. 构建APK
1. 选择Build Variant为"release"
2. 点击Finish开始构建
3. 构建完成后，APK文件会显示在输出目录

## 小米15Pro优化配置

### 1. 屏幕适配
在`android/app/src/main/AndroidManifest.xml`中添加：
```xml
<supports-screens
    android:smallScreens="true"
    android:normalScreens="true"
    android:largeScreens="true"
    android:xlargeScreens="true"
    android:anyDensity="true" />

<uses-feature
    android:name="android.hardware.touchscreen"
    android:required="true" />
```

### 2. 权限配置
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

### 3. 性能优化
在`android/app/build.gradle`中：
```gradle
android {
    defaultConfig {
        // 启用多dex支持
        multiDexEnabled true
        
        // 目标SDK版本
        targetSdkVersion 33
        minSdkVersion 26
    }
    
    buildTypes {
        release {
            // 启用代码压缩
            minifyEnabled true
            shrinkResources true
            
            // 优化配置
            debuggable false
            jniDebuggable false
            renderscriptDebuggable false
        }
    }
}
```

## 测试APK

### 1. 安装测试
```bash
# 使用adb安装
adb install app-release.apk

# 卸载旧版本
adb uninstall com.kanbanmobileapp

# 重新安装
adb install -r app-release.apk
```

### 2. 功能测试
- 启动应用测试
- 网络连接测试
- 触摸操作测试
- 性能测试

### 3. 小米15Pro专项测试
- 屏幕适配测试
- 手势操作测试
- 电池消耗测试
- 内存使用测试

## 问题解决

### 常见构建错误

#### 错误1：Gradle同步失败
```bash
# 清理Gradle缓存
cd android
./gradlew cleanBuildCache

# 删除node_modules重新安装
cd ..
rm -rf node_modules
npm install
```

#### 错误2：签名问题
```bash
# 检查密钥库
keytool -list -v -keystore kanban-release-key.keystore

# 重新生成密钥
keytool -genkeypair -v -keystore kanban-release-key.keystore -alias kanban-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

#### 错误3：资源找不到
```bash
# 清理构建
cd android
./gradlew clean

# 重新构建
./gradlew assembleRelease
```

## 发布准备

### 1. APK优化
- 使用Android Studio的APK Analyzer分析
- 移除未使用的资源
- 压缩图片资源
- 启用R8代码优化

### 2. 版本管理
- 更新版本号和版本名称
- 更新应用图标和启动图
- 更新应用描述

### 3. 安全考虑
- 不要提交密钥库到版本控制
- 使用环境变量存储敏感信息
- 启用代码混淆

## 自动化构建脚本

### Windows批处理
```batch
@echo off
echo 开始构建APK...
cd /d %~dp0
cd KanbanMobileApp

echo 安装依赖...
call npm install

echo 构建APK...
cd android
call gradlew clean
call gradlew assembleRelease

echo APK构建完成！
pause
```

### Shell脚本
```bash
#!/bin/bash
echo "开始构建APK..."
cd KanbanMobileApp

echo "安装依赖..."
npm install

echo "构建APK..."
cd android
./gradlew clean
./gradlew assembleRelease

echo "APK构建完成！"
```

---
**提示**：构建过程中遇到问题，请参考React Native官方文档或联系技术支持。