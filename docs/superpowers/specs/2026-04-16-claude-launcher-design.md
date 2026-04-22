# Claude 启动器设计文档

**日期**: 2026-04-16  
**作者**: Claude Code  
**状态**: 待审核

---

## 1. 概述

### 1.1 项目目标
创建一个 Windows 桌面小工具，用于简化 Claude Code 的启动流程，提供图形化界面选择文件夹和对话模式。

### 1.2 问题背景
用户当前需要手动打开 PowerShell，切换到目标文件夹，然后输入 `claude --dangerously-skip-permissions` 命令，流程繁琐。

---

## 2. 技术方案

### 2.1 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 编程语言 | Python 3.x | 跨平台，Windows 支持良好，生态丰富 |
| GUI 框架 | Tkinter + ttk | Python 内置，无需额外依赖，轻量 |
| 打包工具 | PyInstaller | 支持单文件打包，成熟稳定 |
| 配置存储 | JSON 文件 | 简单易读，无需数据库 |

### 2.2 依赖列表
```
pyinstaller>=6.0.0
```

---

## 3. 功能需求

### 3.1 核心功能

| ID | 功能 | 描述 | 优先级 |
|----|------|------|--------|
| F001 | 文件夹路径输入 | 支持手动粘贴文件夹绝对路径 | P0 |
| F002 | 文件夹选择按钮 | 点击弹出 Windows 原生文件夹选择对话框 | P0 |
| F003 | 对话模式选择 | 单选按钮：当前对话(-c) / 历史对话(-r) | P0 |
| F004 | 命令预览 | 实时显示将要执行的完整命令 | P1 |
| F005 | 启动 Claude | 点击按钮打开 PowerShell 并执行命令 | P0 |
| F006 | 记忆文件夹 | 自动保存上次选择的文件夹，下次启动自动恢复 | P1 |

### 3.2 启动命令格式
```powershell
claude <mode> --dangerously-skip-permissions
```
其中 `<mode>` 为 `-c` 或 `-r`。

---

## 4. UI 设计

### 4.1 窗口规格
- **宽度**: 500px
- **高度**: 450px
- **可调整大小**: 否
- **窗口标题**: "Claude 启动器"

### 4.2 界面布局
```
┌─────────────────────────────────────┐
│     🚀 Claude 启动器                │
│   快速启动 Claude Code 会话          │
│                                     │
│  📁 文件夹路径                       │
│  ┌─────────────────────────────┐   │
│  │ D:\project\my-app    [📂]  │   │
│  └─────────────────────────────┘   │
│  ✓ 已记住上次选择的文件夹           │
│                                     │
│  💬 对话模式                        │
│  ┌─────────────────────────────┐   │
│  │ ◉ 当前对话 (-c)   ○ 历史    │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ claude -c --dangerously...  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │      🎯 启动 Claude         │   │
│  └─────────────────────────────┘   │
│                                     │
│  点击按钮将打开 PowerShell...       │
└─────────────────────────────────────┘
```

### 4.3 配色方案
- 主色调: 紫色渐变 (#667eea → #764ba2)
- 背景: 白色
- 文字: 深灰色 (#333)
- 边框: 浅灰色 (#e0e0e0)

---

## 5. 架构设计

### 5.1 文件结构
```
test_claude_snap/
├── src/
│   ├── main.py          # 主程序入口
│   ├── ui.py            # UI 界面类
│   ├── config.py        # 配置管理类
│   └── launcher.py      # 命令启动器
├── build/               # 打包输出目录
├── config.json          # 运行时生成的配置文件
├── requirements.txt     # 依赖列表
└── build.bat            # 打包脚本
```

### 5.2 模块职责

#### config.py - 配置管理
```python
class Config:
    - __init__()                # 初始化，加载配置
    - load()                    # 从 config.json 加载
    - save()                    # 保存到 config.json
    - last_folder: str          # 上次选择的文件夹路径
```

#### ui.py - 用户界面
```python
class LauncherUI:
    - __init__(config)          # 初始化 UI
    - setup_ui()                # 构建界面
    - on_browse_click()         # 浏览按钮点击
    - on_mode_change()          # 模式切换
    - on_launch_click()         # 启动按钮点击
    - update_command_preview()  # 更新命令预览
```

#### launcher.py - 命令启动器
```python
class ClaudeLauncher:
    - launch(folder, mode)      # 启动 Claude
    - build_command(mode)       # 构建命令字符串
```

#### main.py - 主入口
```python
if __name__ == "__main__":
    config = Config()
    app = LauncherUI(config)
    app.run()
```

---

## 6. 配置文件格式

### config.json
```json
{
  "last_folder": "D:\\学习\\workplace\\idea-space\\test_claude_snap",
  "last_mode": "-c"
}
```

---

## 7. 打包方案

### 7.1 PyInstaller 配置
- 单文件打包: `--onefile`
- 无控制台窗口: `--noconsole`
- 图标: 可选，使用默认 Python 图标
- 输出目录: `build/`

### 7.2 打包命令
```bash
pyinstaller --onefile --noconsole --name "ClaudeLauncher" --distpath build src/main.py
```

---

## 8. 验收标准

- [ ] 可以正常启动，显示主界面
- [ ] 可以手动输入文件夹路径
- [ ] 点击"选择"按钮可以弹出文件夹选择对话框
- [ ] 可以在"当前对话"和"历史对话"之间切换
- [ ] 命令预览区域实时更新
- [ ] 点击"启动 Claude"可以打开 PowerShell 并执行正确命令
- [ ] 关闭程序后重新打开，自动恢复上次选择的文件夹
- [ ] 可以打包为单个 EXE 文件
- [ ] EXE 文件可以在未安装 Python 的 Windows 机器上运行

---

## 9. 非功能性需求

| 需求 | 目标 |
|------|------|
| 启动时间 | < 2 秒 |
| EXE 体积 | < 20MB |
| 兼容性 | Windows 10/11 |
| 内存占用 | < 50MB |
