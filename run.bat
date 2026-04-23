@echo off
echo ================================
echo 虚拟币犯罪调查工具集
echo ================================
echo.

REM Check if Flask is installed
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    echo.
)

echo 正在启动Flask服务器...
echo 服务器地址: http://127.0.0.1:5000
echo 按 Ctrl+C 可停止服务器
echo.

REM Change to script directory
cd /d "%~dp0"

REM Start browser after 2 seconds (background)
start "" cmd /c "timeout /t 2 >nul && start http://127.0.0.1:5000"

REM Start Flask server
python app.py

pause