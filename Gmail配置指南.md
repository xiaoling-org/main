# Gmail邮箱配置指南

## 📧 邮箱信息
- **主邮箱**: xiaoling.assistant@gmail.com
- **备用邮箱1**: xiao.ling.tongxue@gmail.com
- **备用邮箱2**: clawdbot.xiaoling@gmail.com

## 🔐 安全注意事项
**重要**: 密码 `czp94568` 已从对话记录中移除，避免泄露。

## ⚙️ Gmail设置步骤

### 1. 启用IMAP访问
1. 登录 https://gmail.com
2. 点击右上角设置图标 ⚙️
3. 选择"查看所有设置"
4. 转到"转发和POP/IMAP"标签页
5. 在"IMAP访问"部分选择"启用IMAP"
6. 点击"保存更改"

### 2. 允许不够安全的应用访问
**方法A（简单但安全性较低）**:
1. 访问 https://myaccount.google.com/lesssecureapps
2. 启用"允许不够安全的应用"选项

**方法B（推荐，更安全）**:
1. 访问 https://myaccount.google.com/apppasswords
2. 可能需要先启用两步验证
3. 生成应用专用密码
4. 使用生成的16位密码代替常规密码

### 3. 检查两步验证
1. 访问 https://myaccount.google.com/security
2. 检查是否启用了两步验证
3. 如果已启用，必须使用应用专用密码

## 🧪 手动测试步骤

### 测试1: 网页登录测试
1. 访问 https://gmail.com
2. 使用 `xiaoling.assistant@gmail.com` 和密码登录
3. 确认可以正常访问收件箱

### 测试2: 发送测试邮件
1. 登录主邮箱
2. 点击"撰写"
3. 发送邮件到备用邮箱
4. 登录备用邮箱确认收到

### 测试3: 接收测试邮件
1. 从备用邮箱发送邮件到主邮箱
2. 在主邮箱中确认收到

## 🔧 技术配置（供开发使用）

### IMAP设置
```
服务器: imap.gmail.com
端口: 993
加密: SSL/TLS
用户名: xiaoling.assistant@gmail.com
密码: [应用专用密码]
```

### SMTP设置
```
服务器: smtp.gmail.com
端口: 587
加密: STARTTLS
用户名: xiaoling.assistant@gmail.com
密码: [应用专用密码]
```

## 📋 检查清单

### ✅ 已完成
- [x] 邮箱地址确认
- [x] 密码提供
- [x] 安全存储密码信息

### 🔄 待测试
- [ ] 网页登录测试
- [ ] IMAP访问启用
- [ ] 应用访问权限设置
- [ ] 发送/接收测试

## 🚨 故障排除

### 常见问题1: 登录被拒绝
**症状**: "用户名或密码不正确" 或 "需要应用专用密码"
**解决**:
1. 确认密码正确
2. 启用"不够安全的应用"访问
3. 或生成应用专用密码

### 常见问题2: IMAP连接失败
**症状**: "无法连接到服务器"
**解决**:
1. 确认已启用IMAP
2. 检查防火墙设置
3. 确认使用正确端口(993)

### 常见问题3: 发送邮件失败
**症状**: "SMTP认证失败"
**解决**:
1. 确认SMTP设置正确
2. 使用应用专用密码
3. 检查是否启用了两步验证

## 📞 支持资源
- Gmail帮助中心: https://support.google.com/mail
- 应用专用密码指南: https://support.google.com/accounts/answer/185833
- IMAP设置指南: https://support.google.com/mail/answer/7126229

## 📝 最后更新
- **配置时间**: 2026-02-09 10:12
- **配置人**: 陈先生
- **测试状态**: 待测试
- **安全状态**: 密码已安全处理