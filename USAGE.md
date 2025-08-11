# 使用说明

## 获取登录凭据

为了使用此工具，您需要获取 Bilibili 的登录凭据。以下是获取方法：

### 方法一：浏览器开发者工具（推荐使用）

1. 使用浏览器登录 [Bilibili](https://www.bilibili.com)
2. 按 F12 打开开发者工具
3. 点击 "Network" (网络) 标签
4. 刷新页面或随便点击一个链接
5. 在请求列表中找到任意一个对 bilibili.com 的请求
6. 查看请求头中的 Cookie 信息，找到以下值：
   - `SESSDATA`: 会话数据
   - `bili_jct`: CSRF令牌  
   - `DedeUserID`: 用户ID
7. 或者点击 "Application" 标签，从Cookie一栏获得上述值

### 方法二：浏览器控制台（测试中发现部分凭据无法获得）

1. 登录 Bilibili 后，按 F12 打开开发者工具
2. 点击 "Console" (控制台) 标签
3. 输入以下代码并回车：

```javascript
// 获取所有需要的 Cookie 值
console.log('SESSDATA:', document.cookie.match(/SESSDATA=([^;]+)/)?.[1] || '未找到');
console.log('bili_jct:', document.cookie.match(/bili_jct=([^;]+)/)?.[1] || '未找到');  
console.log('DedeUserID:', document.cookie.match(/DedeUserID=([^;]+)/)?.[1] || '未找到');
```

4. 复制输出的值到配置文件中

## 配置文件设置

1. 复制 `config.example.json` 为 `config.json`
2. 将获取的值填入配置文件：

```json
{
    "cookies": {
        "SESSDATA": "你的SESSDATA值",
        "bili_jct": "你的bili_jct值", 
        "DedeUserID": "你的DedeUserID值"
    },
    ...
}
```

## 安全提醒

⚠️ **重要提醒**：
- 这些登录凭据相当于您的账号密码，请妥善保管
- 不要将包含真实凭据的 `config.json` 文件上传到公共代码库
- 建议定期更换密码以保证账号安全
- 此工具仅供个人学习使用，请遵守 Bilibili 使用条款

## 功能说明

### 批量取消关注
- 支持一键取消所有关注
- 提供二次确认，避免误操作
- 支持进度显示和错误处理
- 自动添加请求延迟，避免触发反爬机制

### 关注统计
- 查看总关注数
- 显示最近关注的用户列表
- 提供用户基本信息

## 故障排除

### 常见问题

1. **"登录验证失败"**
   - 检查配置文件中的凭据是否正确
   - 确认账号没有在其他地方退出登录
   - 尝试重新获取登录凭据

2. **"请求被限制"**
   - 适当增加配置文件中的 `delay_between_requests` 值
   - 减少 `batch_size` 值
   - 等待一段时间后重试

3. **"取消关注失败"**
   - 可能是网络问题，稍后重试
   - 可能是该用户已经不在关注列表中
   - 可能触发了 Bilibili 的安全机制

### 日志查看

程序运行时会输出详细的日志信息，如果遇到问题，请查看日志中的错误信息。
