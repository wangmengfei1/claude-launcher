import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


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
            # 使用 PowerShell 启动 - 使用不同的方式
            # 方法1: 直接使用 start 命令通过 cmd
            try:
                # 方式1: 使用 start 命令通过 cmd
                cmd_command = f'start powershell.exe -NoExit -Command "{ps_command}"'
                subprocess.Popen(cmd_command, shell=True, cwd=folder)
                return True
            except Exception as e1:
                print(f"方式1失败: {e1}")
                try:
                    # 方式2: 直接调用 powershell
                    subprocess.Popen([
                        "powershell.exe",
                        "-NoExit",
                        "-Command",
                        ps_command
                    ], cwd=folder, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    return True
                except Exception as e2:
                    print(f"方式2失败: {e2}")
                    # 方式3: 使用 os.startfile (Windows only)
                    if sys.platform == 'win32':
                        # 创建一个临时批处理文件
                        batch_path = os.path.join(folder, "launch_claude.bat")
                        with open(batch_path, "w", encoding="gbk") as f:
                            f.write(f"@echo off\ncd /d \"{folder}\"\npowershell.exe -NoExit -Command \"{ps_command}\"\ndel \"%~f0\"\n")
                        os.startfile(batch_path)
                        return True
                    return False

        except Exception as e:
            print(f"启动失败: {e}")
            import traceback
            traceback.print_exc()
            return False


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
        # 主容器
        main_frame = ttk.Frame(self.root, padding="30 20 30 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题区域
        self._create_header(main_frame)

        # 文件夹路径区域
        self._create_folder_section(main_frame)

        # 对话模式区域
        self._create_mode_section(main_frame)

        # 命令预览区域
        self._create_command_preview(main_frame)

        # 底部按钮区域
        self._create_footer(main_frame)

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
            messagebox.showwarning("提示", "请先选择文件夹！")
            return

        # 保存配置
        self.config.last_folder = folder
        self.config.last_mode = mode

        # 启动
        success = ClaudeLauncher.launch(folder, mode)
        if not success:
            messagebox.showerror("错误", "启动失败，请检查文件夹路径是否有效！")

    def run(self):
        """运行主循环"""
        self.root.mainloop()


def main():
    """主程序入口"""
    # 处理打包后的路径问题
    if getattr(sys, 'frozen', False):
        # 打包后的 EXE 运行
        app_path = os.path.dirname(sys.executable)
    else:
        # 开发环境运行
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 切换工作目录
    os.chdir(app_path)

    try:
        # 初始化配置和 UI
        config = Config()
        app = LauncherUI(config)
        app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")


if __name__ == "__main__":
    main()
