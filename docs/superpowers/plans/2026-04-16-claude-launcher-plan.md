# Claude 启动器实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个 Python + Tkinter 的 Windows 桌面工具，用于简化 Claude Code 的启动流程，支持文件夹选择、对话模式切换，并记忆上次配置。

**Architecture:** 采用模块化设计，分为配置管理(config.py)、UI界面(ui.py)、命令启动器(launcher.py)三个核心模块，通过 main.py 整合启动。

**Tech Stack:** Python 3.x, Tkinter, PyInstaller

---

## 任务清单

### Task 1: 项目结构与依赖配置

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
pyinstaller>=6.0.0
```

- [ ] **Step 2: 创建 src 目录和空的 __init__.py**

```bash
mkdir -p src
echo "# Claude Launcher" > src/__init__.py
```

---

### Task 2: 配置管理模块 (config.py)

**Files:**
- Create: `src/config.py`

- [ ] **Step 1: 编写 Config 类**

```python
import json
import os


class Config:
    """配置管理类，负责保存和加载用户配置"""

    DEFAULT_CONFIG = {
        "last_folder": "",
        "last_mode": "-c"
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """从 JSON 文件加载配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        """保存配置到 JSON 文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    @property
    def last_folder(self):
        return self.config.get("last_folder", "")

    @last_folder.setter
    def last_folder(self, value):
        self.config["last_folder"] = value
        self.save()

    @property
    def last_mode(self):
        return self.config.get("last_mode", "-c")

    @last_mode.setter
    def last_mode(self, value):
        self.config["last_mode"] = value
        self.save()
```

---

### Task 3: 命令启动器模块 (launcher.py)

**Files:**
- Create: `src/launcher.py`

- [ ] **Step 1: 编写 ClaudeLauncher 类**

```python
import os
import subprocess
import sys


class ClaudeLauncher:
    """命令启动器，负责启动 PowerShell 并执行 Claude 命令"""

    @staticmethod
    def build_command(mode):
        """构建 Claude 命令字符串"""
        return f'claude {mode} --dangerously-skip-permissions'

    @staticmethod
    def launch(folder, mode):
        """
        启动 Claude Code

        Args:
            folder: 目标文件夹路径
            mode: 对话模式 (-c 或 -r)
        """
        if not folder or not os.path.isdir(folder):
            return False

        command = ClaudeLauncher.build_command(mode)

        # 构建 PowerShell 启动命令
        # 先切换目录，然后执行 claude
        ps_command = f'cd "{folder}"; {command}; pause'

        try:
            # 使用 PowerShell 启动
            subprocess.Popen([
                "powershell.exe",
                "-NoExit",
                "-Command",
                ps_command
            ], cwd=folder)
            return True
        except Exception as e:
            print(f"启动失败: {e}")
            return False
```

---

### Task 4: UI 界面模块 (ui.py) - 基础框架

**Files:**
- Create: `src/ui.py`

- [ ] **Step 1: 编写 LauncherUI 基础框架**

```python
import tkinter as tk
from tkinter import ttk, filedialog
from config import Config
from launcher import ClaudeLauncher


class LauncherUI:
    """Claude 启动器主界面"""

    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 450

    def __init__(self, config: Config):
        self.config = config
        self.root = tk.Tk()
        self.root.title("Claude 启动器")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # 变量
        self.folder_path = tk.StringVar(value=self.config.last_folder)
        self.mode_var = tk.StringVar(value=self.config.last_mode)

        self.setup_ui()

    def setup_ui(self):
        """构建界面"""
        pass

    def run(self):
        """运行主循环"""
        self.root.mainloop()
```

---

### Task 5: UI 界面模块 (ui.py) - 标题与路径输入区

**Files:**
- Modify: `src/ui.py`

- [ ] **Step 1: 更新 setup_ui()，添加标题和路径输入区**

```python
    def setup_ui(self):
        """构建界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="30 20 30 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题区域
        self._create_header(main_frame)

        # 文件夹路径区域
        self._create_folder_section(main_frame)

    def _create_header(self, parent):
        """创建标题区域"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(
            header_frame,
            text="🚀 Claude 启动器",
            font=("Microsoft YaHei", 18, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="快速启动 Claude Code 会话",
            font=("Microsoft YaHei", 10),
            foreground="#666666"
        )
        subtitle_label.pack(pady=(5, 0))

    def _create_folder_section(self, parent):
        """创建文件夹路径区域"""
        folder_frame = ttk.Frame(parent)
        folder_frame.pack(fill=tk.X, pady=(0, 15))

        # 标签
        label = ttk.Label(
            folder_frame,
            text="📁 文件夹路径",
            font=("Microsoft YaHei", 10, "bold")
        )
        label.pack(anchor=tk.W, pady=(0, 5))

        # 输入框和按钮容器
        input_frame = ttk.Frame(folder_frame)
        input_frame.pack(fill=tk.X)

        # 路径输入框
        entry = ttk.Entry(
            input_frame,
            textvariable=self.folder_path,
            font=("Microsoft YaHei", 10)
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 浏览按钮
        browse_btn = ttk.Button(
            input_frame,
            text="📂 选择",
            command=self.on_browse_click,
            width=10
        )
        browse_btn.pack(side=tk.LEFT, padx=(8, 0))

        # 记住提示
        if self.config.last_folder:
            hint = ttk.Label(
                folder_frame,
                text="✓ 已记住上次选择的文件夹",
                font=("Microsoft YaHei", 9),
                foreground="#28a745"
            )
            hint.pack(anchor=tk.W, pady=(5, 0))
```

---

### Task 6: UI 界面模块 (ui.py) - 对话模式与命令预览

**Files:**
- Modify: `src/ui.py`

- [ ] **Step 1: 添加 _create_mode_section() 和 _create_command_preview()**

在 `setup_ui()` 中添加：
```python
        # 对话模式区域
        self._create_mode_section(main_frame)

        # 命令预览区域
        self._create_command_preview(main_frame)
```

然后添加这两个方法：
```python
    def _create_mode_section(self, parent):
        """创建对话模式选择区域"""
        mode_frame = ttk.Frame(parent)
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        # 标签
        label = ttk.Label(
            mode_frame,
            text="💬 对话模式",
            font=("Microsoft YaHei", 10, "bold")
        )
        label.pack(anchor=tk.W, pady=(0, 5))

        # 单选按钮容器
        radio_frame = ttk.Frame(mode_frame)
        radio_frame.pack(fill=tk.X)

        # 当前对话
        rb_current = ttk.Radiobutton(
            radio_frame,
            text="当前对话 (-c)",
            variable=self.mode_var,
            value="-c",
            command=self.on_mode_change
        )
        rb_current.pack(side=tk.LEFT, padx=(0, 30))

        # 历史对话
        rb_history = ttk.Radiobutton(
            radio_frame,
            text="历史对话 (-r)",
            variable=self.mode_var,
            value="-r",
            command=self.on_mode_change
        )
        rb_history.pack(side=tk.LEFT)

    def _create_command_preview(self, parent):
        """创建命令预览区域"""
        preview_frame = ttk.Frame(parent)
        preview_frame.pack(fill=tk.X, pady=(0, 20))

        # 预览框
        self.command_preview = tk.Text(
            preview_frame,
            height=2,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            padx=10,
            pady=8,
            state=tk.DISABLED
        )
        self.command_preview.pack(fill=tk.X)

        self.update_command_preview()

    def on_mode_change(self):
        """模式切换回调"""
        self.config.last_mode = self.mode_var.get()
        self.update_command_preview()

    def update_command_preview(self):
        """更新命令预览"""
        mode = self.mode_var.get()
        command = f'claude {mode} --dangerously-skip-permissions'

        self.command_preview.config(state=tk.NORMAL)
        self.command_preview.delete(1.0, tk.END)
        self.command_preview.insert(1.0, command)
        self.command_preview.config(state=tk.DISABLED)
```

---

### Task 7: UI 界面模块 (ui.py) - 启动按钮与事件处理

**Files:**
- Modify: `src/ui.py`

- [ ] **Step 1: 添加 _create_footer() 和事件处理方法**

在 `setup_ui()` 中添加：
```python
        # 底部按钮区域
        self._create_footer(main_frame)
```

然后添加：
```python
    def _create_footer(self, parent):
        """创建底部按钮区域"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X)

        # 启动按钮
        style = ttk.Style()
        style.configure(
            "Launch.TButton",
            font=("Microsoft YaHei", 12, "bold"),
            padding=15
        )

        launch_btn = ttk.Button(
            footer_frame,
            text="🎯 启动 Claude",
            command=self.on_launch_click,
            style="Launch.TButton"
        )
        launch_btn.pack(fill=tk.X, pady=(0, 10))

        # 提示文字
        hint = ttk.Label(
            footer_frame,
            text="点击按钮将打开 PowerShell 并自动切换到目标文件夹",
            font=("Microsoft YaHei", 9),
            foreground="#999999"
        )
        hint.pack()

    def on_browse_click(self):
        """浏览按钮点击"""
        initial_dir = self.folder_path.get() or self.config.last_folder
        folder = filedialog.askdirectory(
            title="选择文件夹",
            initialdir=initial_dir if initial_dir else None
        )
        if folder:
            self.folder_path.set(folder)
            self.config.last_folder = folder

    def on_launch_click(self):
        """启动按钮点击"""
        folder = self.folder_path.get()
        mode = self.mode_var.get()

        if not folder:
            tk.messagebox.showwarning("提示", "请先选择文件夹！")
            return

        # 保存配置
        self.config.last_folder = folder
        self.config.last_mode = mode

        # 启动
        success = ClaudeLauncher.launch(folder, mode)
        if not success:
            tk.messagebox.showerror("错误", "启动失败，请检查文件夹路径是否有效！")
```

- [ ] **Step 2: 添加 messagebox 导入**

在文件顶部添加：
```python
from tkinter import messagebox
```

---

### Task 8: 主程序入口 (main.py)

**Files:**
- Create: `src/main.py`

- [ ] **Step 1: 编写主程序入口**

```python
import os
import sys

# 添加 src 目录到路径
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from config import Config
from ui import LauncherUI


def main():
    """主程序入口"""
    # 切换工作目录到程序所在目录（确保 config.json 保存在正确位置）
    if getattr(sys, 'frozen', False):
        # 打包后的 EXE 运行
        app_path = os.path.dirname(sys.executable)
    else:
        # 开发环境运行
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os.chdir(app_path)

    # 初始化配置和 UI
    config = Config()
    app = LauncherUI(config)
    app.run()


if __name__ == "__main__":
    main()
```

---

### Task 9: 打包脚本与测试

**Files:**
- Create: `build.bat`

- [ ] **Step 1: 创建打包脚本 build.bat**

```batch
@echo off
echo ========================================
echo   Claude Launcher 打包脚本
echo ========================================

REM 清理旧的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM 安装依赖
echo.
echo [1/3] 安装依赖...
pip install -r requirements.txt

REM 使用 PyInstaller 打包
echo.
echo [2/3] 正在打包...
pyinstaller --onefile --noconsole --name "ClaudeLauncher" --distpath build src/main.py

echo.
echo [3/3] 清理临时文件...
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo.
echo ========================================
echo   打包完成！
echo   可执行文件位于: build\ClaudeLauncher.exe
echo ========================================
pause
```

- [ ] **Step 2: 测试程序运行**

```bash
python src/main.py
```

预期结果：窗口正常显示，界面元素完整。

---

### Task 10: 最终验证与文档

**Files:**
- Create: `README.md` (可选)

- [ ] **Step 1: 完整功能测试**

手动测试以下功能：
- [ ] 启动程序，显示主界面
- [ ] 手动输入文件夹路径
- [ ] 点击"选择"按钮，弹出文件夹选择对话框
- [ ] 选择文件夹后，路径更新到输入框
- [ ] 在"当前对话"和"历史对话"之间切换，命令预览同步更新
- [ ] 点击"启动 Claude"，打开 PowerShell 并执行命令
- [ ] 关闭程序，重新打开，验证上次选择的文件夹被恢复
- [ ] 运行 build.bat 打包成 EXE
- [ ] 在另一台未安装 Python 的 Windows 机器上测试 EXE

- [ ] **Step 2: 创建简单的 README.md (可选)**

```markdown
# Claude 启动器

一个简化 Claude Code 启动流程的 Windows 桌面小工具。

## 功能特点

- 📁 图形化文件夹选择
- 💬 支持当前对话/历史对话模式切换
- 💾 自动记住上次配置
- 🚀 一键启动 Claude Code

## 使用方法

1. 运行 `ClaudeLauncher.exe`
2. 选择或输入目标文件夹路径
3. 选择对话模式
4. 点击"启动 Claude"

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python src/main.py

# 打包
build.bat
```
```

---

## 计划完成

**计划文件位置:** `docs/superpowers/plans/2026-04-16-claude-launcher-plan.md`

**执行选项:**

1. **Subagent-Driven (推荐)** - 为每个任务启动独立的子代理，任务间进行代码审查
2. **Inline Execution** - 在当前会话中批量执行，带有检查点

请选择执行方式！
