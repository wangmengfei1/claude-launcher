import os
import sys

# 处理打包后的路径问题
if getattr(sys, 'frozen', False):
    # 打包后的 EXE 运行
    app_path = os.path.dirname(sys.executable)
    # 确保能找到其他模块
    bundle_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else app_path
    sys.path.insert(0, bundle_dir)
    sys.path.insert(0, app_path)
else:
    # 开发环境运行
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, src_dir)

# 切换工作目录
os.chdir(app_path)

# 导入模块（延迟导入，确保路径设置好了）
try:
    from config import Config
    from ui import LauncherUI
except Exception as e:
    print(f"导入模块失败: {e}")
    import traceback
    traceback.print_exc()
    input("\n按回车键退出...")
    sys.exit(1)


def main():
    """主程序入口"""
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
