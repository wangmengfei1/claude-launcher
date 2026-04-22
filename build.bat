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
