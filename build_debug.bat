@echo off
echo ========================================
echo   Claude Launcher 调试版打包脚本
echo ========================================
echo.
echo   注意：此版本会显示控制台窗口，
echo   方便查看错误信息！
echo.
echo ========================================

REM 清理旧的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM 安装依赖
echo.
echo [1/3] 安装依赖...
pip install -r requirements.txt

REM 使用 PyInstaller 打包（带控制台窗口，方便调试）
echo.
echo [2/3] 正在打包（调试版，带控制台）...
pyinstaller --onefile --name "ClaudeLauncher_Debug" --distpath build src/main.py

echo.
echo [3/3] 清理临时文件...
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo.
echo ========================================
echo   打包完成！
echo   可执行文件位于: build\ClaudeLauncher_Debug.exe
echo.
echo   注意：这是调试版，运行时会显示控制台窗口，
echo   可以查看任何错误信息。
echo ========================================
pause
