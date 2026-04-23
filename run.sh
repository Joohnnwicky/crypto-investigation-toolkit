#!/bin/bash

echo "================================"
echo "虚拟币犯罪调查工具集"
echo "================================"
echo ""

# Check if Flask is installed
if ! pip show Flask > /dev/null 2>&1; then
    echo "正在安装依赖..."
    pip install -r requirements.txt
    echo ""
fi

echo "正在启动Flask服务器..."
echo "服务器地址: http://127.0.0.1:5000"
echo "按 Ctrl+C 可停止服务器"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Start Flask server
python3 app.py