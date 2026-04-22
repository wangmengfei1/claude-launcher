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
            # 使用 PowerShell 启动 - 使用不同的方式
            # 方法1: 直接使用 start 命令
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # 尝试多种启动方式
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
