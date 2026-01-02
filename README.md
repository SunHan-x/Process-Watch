# Process-Watch

Linux 进程监控工具，任务结束后通过 Bark 推送通知到 iOS 设备。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
chmod +x pwatch
```

### 2. 配置 Bark Key
将```.env.example```更名为```.env```，并配置
```env
BARK_KEY=你的BarkKey
```

### 3. 设置别名
将 `pwatch` 设为全局命令：
```bash
echo 'alias pwatch="'$PWD'/pwatch"' >> ~/.bashrc
source ~/.bashrc
```

## 📖 使用方法

### 监控已有进程 (后台模式)
监控指定 PID，脚本在后台运行，不占用终端。
```bash
pwatch your_pid
```

### 运行命令并通知 (Wrapper 模式)
执行命令，结束后发送包含耗时和状态的通知。
```bash
pwatch your_command
```