# 虚拟币犯罪调查工具集 - Phase 1 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建Flask应用核心框架，包含基础模板、侧边栏导航、共享模块，以及第一个完整工具（TRON可疑特征分析），实现一键启动和Web界面操作。

**Architecture:** Flask单应用结构，modules目录按功能分组（tron/eth/btc等），templates使用Jinja2继承base.html，API路由统一在/api/v1/下，前端用原生HTML+Tailwind无需构建。

**Tech Stack:** Flask 2.3.0, Python 3.8+, requests, Tailwind CSS (CDN)

---

## File Structure for Phase 1

```
虚拟币犯罪调查工具集/
├── app.py                      # Flask主入口
├── config.py                   # 配置（样本数据）
├── requirements.txt            # 依赖列表
├── run.bat                     # Windows启动脚本
├── run.sh                      # Linux启动脚本
├── static/
│   ├── css/custom.css          # 自定义样式
│   └── js/main.js              # 前端交互
├── templates/
│   ├── base.html               # 基础模板（侧边栏）
│   ├── index.html              # 首页
│   └── tools/tron-suspicious.html
├── modules/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── api_client.py       # API调用基类
│   │   ├── formatter.py        # 输出格式化
│   │   └── exporter.py         # 导出功能
│   └── tron/
│   │   ├── __init__.py
│   │   └── suspicious_analyzer.py
└── tests/
    ├── test_app.py
    └── test_tron_analyzer.py
```

---

## Task 1: 项目基础文件

**Files:**
- Create: `requirements.txt`
- Create: `run.bat`
- Create: `run.sh`
- Create: `config.py`

- [ ] **Step 1: 创建requirements.txt**

```txt
flask==2.3.0
requests==2.31.0
werkzeug==2.3.0
```

- [ ] **Step 2: 创建run.bat（Windows启动脚本）**

```batch
@echo off
echo ========================================
echo 虚拟币犯罪调查工具集
echo ========================================
echo.

REM 检查Python
python --version 2>NUL
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖...
pip show flask 2>NUL >NUL
if errorlevel 1 (
    echo 安装依赖...
    pip install -r requirements.txt
)

REM 启动Flask
echo.
echo 启动服务...
echo 请在浏览器打开: http://localhost:5000
echo.
python app.py
pause
```

- [ ] **Step 3: 创建run.sh（Linux/Mac启动脚本）**

```bash
#!/bin/bash
echo "========================================"
echo "虚拟币犯罪调查工具集"
echo "========================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python"
    exit 1
fi

# 安装依赖
pip3 install -r requirements.txt 2>/dev/null

# 启动
echo "启动服务: http://localhost:5000"
python3 app.py
```

- [ ] **Step 4: 创建config.py（样本数据配置）**

```python
"""配置文件 - 存储样本数据和工具信息"""

# 样本地址数据（帮助初学者理解输入格式）
SAMPLE_DATA = {
    "tron": {
        "address": "TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw",
        "hint": "TRON地址示例（以T开头，34位）"
    },
    "eth": {
        "address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
        "api_key_hint": "从 etherscan.io/apis 免费获取",
        "hint": "ETH地址示例（以0x开头，42位）"
    },
    "btc": {
        "address": "bc1qar0srrr7xfkvy5l643lydnw9re59gtfar9ru49",
        "api_key_hint": "从 blockchain.com/api 免费获取",
        "hint": "BTC地址示例（bc1开头）"
    }
}

# 工具分组信息
TOOL_GROUPS = [
    {
        "name": "地址分析",
        "icon": "🔍",
        "tools": [
            {"id": "tron-suspicious", "name": "TRON地址可疑分析", "desc": "检测可疑特征、评分"},
            {"id": "tron-behavior", "name": "TRON地址行为分析", "desc": "行为模式、资金流向"},
            {"id": "eth-transactions", "name": "ETH交易查询", "desc": "全部交易+跨链桥识别"}
        ]
    },
    {
        "name": "交易追踪",
        "icon": "💸",
        "tools": [
            {"id": "uniswap-trace", "name": "Uniswap追踪", "desc": "DEX交易路径"},
            {"id": "mixer-trace", "name": "混币器追踪", "desc": "洗钱路径还原"},
            {"id": "btc-tx", "name": "BTC交易分析", "desc": "比特币流向"}
        ]
    },
    {
        "name": "跨链分析",
        "icon": "🔗",
        "tools": [
            {"id": "btc-clustering", "name": "地址聚类", "desc": "多地址关联分析"},
            {"id": "cross-border", "name": "跨境协查", "desc": "国际协作模板"}
        ]
    },
    {
        "name": "案件处理",
        "icon": "🛡️",
        "tools": [
            {"id": "multi-chain", "name": "多链监控", "desc": "实时地址监控"},
            {"id": "obfuscation", "name": "混淆攻击对抗", "desc": "对抗手法识别"},
            {"id": "recovery", "name": "资产追回冻结", "desc": "冻结流程建议"}
        ]
    }
]

# Flask配置
FLASK_CONFIG = {
    "SECRET_KEY": "dev-key-change-in-production",
    "DEBUG": True,
    "HOST": "localhost",
    "PORT": 5000
}
```

- [ ] **Step 5: 提交基础文件**

```bash
git add requirements.txt run.bat run.sh config.py
git commit -m "chore: add project base files and config"
```

---

## Task 2: Flask主应用结构

**Files:**
- Create: `app.py`
- Create: `modules/__init__.py`
- Create: `modules/core/__init__.py`

- [ ] **Step 1: 创建app.py（Flask主入口）**

```python
"""Flask主应用入口"""
from flask import Flask, render_template, jsonify, request
from config import FLASK_CONFIG, TOOL_GROUPS

app = Flask(__name__)
app.secret_key = FLASK_CONFIG["SECRET_KEY"]

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """首页 - 工具概览"""
    return render_template('index.html', tool_groups=TOOL_GROUPS)

@app.route('/tools/<tool_id>')
def tool_page(tool_id):
    """工具页面"""
    # 查找工具信息
    for group in TOOL_GROUPS:
        for tool in group["tools"]:
            if tool["id"] == tool_id:
                return render_template(f'tools/{tool_id}.html', 
                    tool=tool, group=group, tool_groups=TOOL_GROUPS)
    return "工具不存在", 404

# ==================== API路由 ====================

@app.route('/api/v1/tron/address', methods=['POST'])
def api_tron_address():
    """TRON地址可疑特征分析API"""
    from modules.tron.suspicious_analyzer import analyze_address
    
    data = request.get_json()
    address = data.get('address')
    
    if not address:
        return jsonify({"status": "error", "message": "缺少address参数"}), 400
    
    result = analyze_address(address)
    return jsonify(result)

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html', tool_groups=TOOL_GROUPS), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "服务器错误"}), 500

# ==================== 启动 ====================

if __name__ == '__main__':
    print("========================================")
    print("虚拟币犯罪调查工具集已启动")
    print("请在浏览器打开: http://localhost:5000")
    print("========================================")
    app.run(
        host=FLASK_CONFIG["HOST"],
        port=FLASK_CONFIG["PORT"],
        debug=FLASK_CONFIG["DEBUG"]
    )
```

- [ ] **Step 2: 创建modules/__init__.py**

```python
"""分析模块"""
```

- [ ] **Step 3: 创建modules/core/__init__.py**

```python
"""核心共享模块"""
from .api_client import BaseAPIClient
from .formatter import OutputFormatter
```

- [ ] **Step 4: 创建tests目录**

```bash
mkdir -p tests
```

- [ ] **Step 5: 创建tests/test_app.py**

```python
"""Flask应用测试"""
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """首页可访问"""
    response = client.get('/')
    assert response.status_code == 200
    assert '虚拟币犯罪调查工具集' in response.data.decode('utf-8')

def test_api_tron_address_missing_param(client):
    """API缺少参数时返回错误"""
    response = client.post('/api/v1/tron/address', 
        json={},
        content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
```

- [ ] **Step 6: 运行测试验证Flask结构**

```bash
cd "J:\虚拟币犯罪调查工具集"
pip install pytest
pytest tests/test_app.py::test_index_page -v
pytest tests/test_app.py::test_api_tron_address_missing_param -v
```

Expected: 首页测试PASS（需模板），API测试PASS

- [ ] **Step 7: 提交Flask主应用**

```bash
git add app.py modules/__init__.py modules/core/__init__.py tests/
git commit -m "feat: add Flask app structure with routes"
```

---

## Task 3: 基础模板（base.html）

**Files:**
- Create: `templates/base.html`
- Create: `templates/index.html`

- [ ] **Step 1: 创建templates目录**

```bash
mkdir -p templates/tools
```

- [ ] **Step 2: 创建templates/base.html（侧边栏布局）**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}虚拟币犯罪调查工具集{% endblock %}</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 自定义样式 */
        .sidebar-item:hover { background-color: #f3f4f6; }
        .sidebar-item.active { background-color: #e5e7eb; border-left: 3px solid #3b82f6; }
        .result-card { transition: all 0.3s ease; }
        .alert-red { background-color: #fee2e2; border-color: #ef4444; }
        .alert-yellow { background-color: #fef3c7; border-color: #f59e0b; }
        .alert-green { background-color: #d1fae5; border-color: #10b981; }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="flex h-screen">
        <!-- 侧边栏 -->
        <aside class="w-64 bg-white shadow-lg flex-shrink-0">
            <div class="p-4 border-b">
                <h1 class="text-lg font-bold text-gray-800">📊 虚拟币犯罪调查工具集</h1>
                <p class="text-sm text-gray-500">链上分析辅助工具</p>
            </div>
            <nav class="p-2 overflow-y-auto h-full">
                {% for group in tool_groups %}
                <div class="mb-4">
                    <div class="px-3 py-2 text-sm font-semibold text-gray-600">
                        {{ group.icon }} {{ group.name }}
                    </div>
                    {% for tool in group.tools %}
                    <a href="/tools/{{ tool.id }}" 
                       class="sidebar-item block px-3 py-2 text-sm text-gray-700 rounded {% if tool.id == tool_id %}active{% endif %}">
                        {{ tool.name }}
                    </a>
                    {% endfor %}
                </div>
                {% endfor %}
            </nav>
            <!-- 底部链接 -->
            <div class="p-4 border-t">
                <a href="/" class="text-sm text-blue-600 hover:underline">首页</a>
            </div>
        </aside>
        
        <!-- 主内容区 -->
        <main class="flex-1 overflow-y-auto">
            <div class="p-6">
                {% block content %}{% endblock %}
            </div>
        </main>
    </div>
    
    <!-- 底部声明 -->
    <footer class="fixed bottom-0 right-0 left-64 bg-gray-200 p-2 text-center text-xs text-gray-600">
        ⚠️ 本工具仅供合法调查使用，请遵守相关法律法规
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 3: 创建templates/index.html（首页）**

```html
{% extends "base.html" %}

{% block title %}虚拟币犯罪调查工具集 - 首页{% endblock %}

{% block content %}
<div class="max-w-4xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">欢迎使用调查工具集</h2>
    <p class="text-gray-600 mb-6">本工具集为链上调查初学者提供便捷的分析功能，无需编写代码即可完成地址分析、交易追踪等工作。</p>
    
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <h3 class="font-semibold text-blue-800 mb-2">快速开始</h3>
        <ol class="text-sm text-blue-700 list-decimal list-inside space-y-1">
            <li>点击左侧工具名称进入工具页面</li>
            <li>输入地址或点击"样本填充"查看示例</li>
            <li>点击"开始分析"获取结果</li>
            <li>导出结果为JSON/CSV/PDF格式</li>
        </ol>
    </div>
    
    <h3 class="text-lg font-semibold text-gray-800 mb-3">工具概览</h3>
    <div class="grid grid-cols-2 gap-4">
        {% for group in tool_groups %}
        <div class="bg-white rounded-lg shadow p-4">
            <h4 class="font-semibold text-gray-800 mb-2">{{ group.icon }} {{ group.name }}</h4>
            <ul class="text-sm text-gray-600 space-y-1">
                {% for tool in group.tools %}
                <li>
                    <a href="/tools/{{ tool.id }}" class="text-blue-600 hover:underline">
                        {{ tool.name }}
                    </a>
                    <span class="text-gray-400">- {{ tool.desc }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: 运行测试验证模板**

```bash
cd "J:\虚拟币犯罪调查工具集"
pytest tests/test_app.py::test_index_page -v
```

Expected: PASS

- [ ] **Step 5: 启动Flask验证首页显示**

```bash
python app.py
# 浏览器打开 http://localhost:5000
# 检查侧边栏显示4个分组、首页显示工具概览
```

Expected: 页面正常显示侧边栏和工具卡片

- [ ] **Step 6: 提交模板文件**

```bash
git add templates/
git commit -m "feat: add base template with sidebar navigation"
```

---

## Task 4: 核心共享模块

**Files:**
- Create: `modules/core/api_client.py`
- Create: `modules/core/formatter.py`
- Create: `modules/core/exporter.py`

- [ ] **Step 1: 创建modules/core/api_client.py**

```python
"""API调用基类 - 统一HTTP请求处理"""
import requests
import time

class BaseAPIClient:
    """API调用基类"""
    
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def get(self, endpoint: str, params: dict = None) -> dict:
        """
        发送GET请求
        
        Args:
            endpoint: API端点路径
            params: 查询参数
            
        Returns:
            dict: API返回数据，失败返回None
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(
                    url, 
                    params=params, 
                    headers=self.HEADERS,
                    timeout=self.DEFAULT_TIMEOUT
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit
                    time.sleep(self.RETRY_DELAY * 2)
                    continue
                else:
                    return None
                    
            except requests.Timeout:
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                    continue
                return None
            except requests.RequestException:
                return None
        
        return None
    
    def validate_address(self, address: str, prefix: str) -> bool:
        """验证地址格式"""
        if not address:
            return False
        return address.startswith(prefix) and len(address) > 20
```

- [ ] **Step 2: 创建modules/core/formatter.py**

```python
"""输出格式化 - 统一结果展示格式"""
from datetime import datetime

class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def format_timestamp(ts: int) -> str:
        """
        时间戳转可读格式
        
        Args:
            ts: 毫秒时间戳
            
        Returns:
            str: YYYY-MM-DD HH:MM:SS 格式
        """
        if not ts:
            return "未知"
        try:
            dt = datetime.fromtimestamp(ts / 1000)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "无效时间"
    
    @staticmethod
    def format_balance(value: float, unit: str = "") -> str:
        """格式化余额显示"""
        if value == 0:
            return f"0 {unit}"
        return f"{value:.6f} {unit}".rstrip('0').rstrip('.')
    
    @staticmethod
    def format_alerts(alerts: dict) -> list:
        """
        格式化警报列表
        
        Args:
            alerts: {red: [], yellow: [], green: []}
            
        Returns:
            list: 格式化的警报列表
        """
        result = []
        
        for alert in alerts.get('red', []):
            result.append({
                "level": "red",
                "icon": "⚠️",
                "feature": alert.get('feature', ''),
                "detail": alert.get('detail', ''),
                "meaning": alert.get('meaning', '')
            })
        
        for alert in alerts.get('yellow', []):
            result.append({
                "level": "yellow",
                "icon": "⚡",
                "feature": alert.get('feature', ''),
                "detail": alert.get('detail', ''),
                "meaning": alert.get('meaning', '')
            })
        
        for alert in alerts.get('green', []):
            result.append({
                "level": "green",
                "icon": "✅",
                "feature": alert.get('feature', ''),
                "detail": alert.get('detail', ''),
                "meaning": alert.get('meaning', '')
            })
        
        return result
    
    @staticmethod
    def format_score(score: int) -> dict:
        """格式化风险评分"""
        if score >= 70:
            return {"level": "high", "color": "red", "text": "高风险"}
        elif score >= 40:
            return {"level": "medium", "color": "yellow", "text": "中等风险"}
        else:
            return {"level": "low", "color": "green", "text": "低风险"}
```

- [ ] **Step 3: 创建modules/core/exporter.py**

```python
"""导出功能 - JSON/CSV/PDF导出"""
import json
import csv
import io
from datetime import datetime

class Exporter:
    """导出器"""
    
    @staticmethod
    def to_json(data: dict) -> str:
        """导出为JSON字符串"""
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def to_csv(data: dict, filename: str = "export") -> str:
        """
        导出为CSV格式
        
        Args:
            data: 分析结果数据
            
        Returns:
            str: CSV内容
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 基本信息
        writer.writerow(["=== 基本信息 ==="])
        writer.writerow(["地址", data.get("address", "")])
        writer.writerow(["分析时间", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # 余额信息
        if "balance" in data:
            writer.writerow(["=== 余额信息 ==="])
            writer.writerow(["TRX余额", data.get("balance", 0)])
            writer.writerow(["USDT余额", data.get("usdt_balance", 0)])
            writer.writerow([])
        
        # 警报信息
        if "alerts" in data:
            writer.writerow(["=== 可疑特征 ==="])
            writer.writerow(["级别", "特征", "详情", "意义"])
            for alert in data.get("alerts", {}).get("red", []):
                writer.writerow(["红色警报", alert.get("feature"), alert.get("detail"), alert.get("meaning")])
            for alert in data.get("alerts", {}).get("yellow", []):
                writer.writerow(["黄色预警", alert.get("feature"), alert.get("detail"), alert.get("meaning")])
            for alert in data.get("alerts", {}).get("green", []):
                writer.writerow(["正常范围", alert.get("feature"), alert.get("detail"), alert.get("meaning")])
            writer.writerow([])
        
        # 评分
        if "score" in data:
            writer.writerow(["=== 风险评分 ==="])
            writer.writerow(["评分", data.get("score", 0)])
        
        return output.getvalue()
    
    @staticmethod
    def get_filename(tool_id: str, address: str, ext: str) -> str:
        """生成导出文件名"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        short_addr = address[:8] if len(address) > 8 else address
        return f"{tool_id}_{short_addr}_{timestamp}.{ext}"
```

- [ ] **Step 4: 提交核心模块**

```bash
git add modules/core/
git commit -m "feat: add core shared modules (api_client, formatter, exporter)"
```

---

## Task 5: TRON可疑特征分析模块

**Files:**
- Create: `modules/tron/__init__.py`
- Create: `modules/tron/suspicious_analyzer.py`
- Create: `templates/tools/tron-suspicious.html`
- Create: `tests/test_tron_analyzer.py`

- [ ] **Step 1: 创建modules/tron/__init__.py**

```python
"""TRON链分析模块"""
from .suspicious_analyzer import analyze_address, get_tron_address_info
```

- [ ] **Step 2: 创建modules/tron/suspicious_analyzer.py**

```python
"""TRON地址可疑特征分析模块"""
from modules.core.api_client import BaseAPIClient
from modules.core.formatter import OutputFormatter

TRONSCAN_API = "https://apilist.tronscan.org"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

def get_tron_address_info(address: str) -> dict:
    """
    获取TRON地址基本信息
    
    Args:
        address: TRON钱包地址（T开头，34位）
        
    Returns:
        dict: 地址信息或None
    """
    client = BaseAPIClient(TRONSCAN_API)
    data = client.get("/api/account", {"address": address})
    
    if not data:
        return None
    
    # 计算USDT余额
    usdt_balance = 0
    for token in data.get('trc20token_balances', []):
        if token.get('tokenId') == USDT_CONTRACT:
            usdt_balance = int(token.get('balance', 0)) / 1e6
            break
    
    return {
        'address': address,
        'balance': data.get('balance', 0) / 1e6,
        'usdt_balance': usdt_balance,
        'total_transaction_count': data.get('total_transaction_count', 0),
        'create_time': data.get('create_time', 0)
    }

def get_trc20_transfers(address: str, limit: int = 50) -> list:
    """获取TRC20代币转账记录"""
    client = BaseAPIClient(TRONSCAN_API)
    data = client.get("/api/token_trc20/transfers", {
        "relatedAddress": address,
        "limit": limit,
        "sort": "-timestamp"
    })
    return data.get('token_transfers', []) if data else []

def detect_suspicious_features(address_info: dict, transfers: list) -> dict:
    """
    识别可疑特征
    
    Returns:
        dict: {red: [], yellow: [], green: [], score: int}
    """
    alerts = {'red': [], 'yellow': [], 'green': [], 'score': 0}
    
    if not address_info:
        alerts['red'].append({
            'feature': '无法获取地址信息',
            'detail': 'API请求失败或地址无效',
            'meaning': '请检查地址格式'
        })
        return alerts
    
    usdt_balance = address_info.get('usdt_balance', 0)
    trx_balance = address_info.get('balance', 0)
    total_tx = address_info.get('total_transaction_count', 0)
    
    # 红色警报：余额清空
    if usdt_balance == 0 and total_tx > 0:
        alerts['red'].append({
            'feature': '余额清空',
            'detail': f'USDT已全部转出，当前余额: {usdt_balance:.2f} USDT',
            'meaning': '资金已被转移，需追踪流向'
        })
        alerts['score'] += 30
    
    # 红色警报：快进快出（简化检测）
    if transfers and len(transfers) >= 2:
        # 检查是否有大额转入后快速转出
        for i, tx in enumerate(transfers[:10]):
            amount = float(tx.get('quant', 0)) / 1e6
            if amount >= 1000 and tx.get('to_address') == address_info['address']:
                # 检查后续是否有转出
                for j in range(i):
                    prev_tx = transfers[j]
                    if prev_tx.get('from_address') == address_info['address']:
                        prev_amount = float(prev_tx.get('quant', 0)) / 1e6
                        if prev_amount > 0:
                            alerts['red'].append({
                                'feature': '大额转入+快速转出',
                                'detail': f'转入 {amount:.2f} USDT，有转出记录',
                                'meaning': '典型洗钱模式（快进快出）'
                            })
                            alerts['score'] += 35
                            break
    
    # 黄色预警：分散转出
    out_addresses = set()
    for tx in transfers:
        if tx.get('from_address') == address_info['address']:
            out_addresses.add(tx.get('to_address', ''))
    
    if len(out_addresses) >= 3:
        alerts['yellow'].append({
            'feature': '分散转出',
            'detail': f'资金被转出到 {len(out_addresses)} 个不同地址',
            'meaning': '洗钱操作，资金已分散'
        })
        alerts['score'] += 20
    
    # 绿色正常：余额稳定
    if usdt_balance > 0:
        alerts['green'].append({
            'feature': '余额稳定',
            'detail': f'USDT余额: {usdt_balance:.2f} USDT',
            'meaning': '资金仍在地址中'
        })
    
    if trx_balance > 10:
        alerts['green'].append({
            'feature': '有TRX余额',
            'detail': f'TRX余额: {trx_balance:.6f} TRX',
            'meaning': '地址仍在使用'
        })
    
    alerts['score'] = min(alerts['score'], 100)
    return alerts

def analyze_address(address: str) -> dict:
    """
    综合分析TRON地址
    
    Args:
        address: TRON钱包地址
        
    Returns:
        dict: 完整分析结果
    """
    # 获取基本信息
    address_info = get_tron_address_info(address)
    
    # 获取转账记录
    transfers = get_trc20_transfers(address) if address_info else []
    
    # 识别可疑特征
    alerts = detect_suspicious_features(address_info, transfers)
    
    # 构建结果
    result = {
        "status": "success",
        "data": {
            "address": address,
            "balance": address_info.get('balance', 0) if address_info else 0,
            "usdt_balance": address_info.get('usdt_balance', 0) if address_info else 0,
            "total_transactions": address_info.get('total_transaction_count', 0) if address_info else 0,
            "alerts": alerts,
            "score": alerts['score']
        },
        "metadata": {
            "query_time": OutputFormatter.format_timestamp(
                address_info.get('create_time', 0) if address_info else 0
            ),
            "source": "Tronscan API"
        }
    }
    
    return result
```

- [ ] **Step 3: 创建tests/test_tron_analyzer.py**

```python
"""TRON分析模块测试"""
import pytest
from modules.tron.suspicious_analyzer import analyze_address, get_tron_address_info

def test_analyze_address_returns_structure():
    """分析返回正确结构"""
    result = analyze_address("TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw")
    
    assert result["status"] in ["success", "error"]
    assert "data" in result
    assert "address" in result["data"]
    assert "alerts" in result["data"]
    assert "score" in result["data"]

def test_analyze_address_invalid():
    """无效地址返回错误信息"""
    result = analyze_address("invalid_address")
    # 可能返回success但data为空，或返回error
    # 这里只检查返回结构正确
    assert "status" in result
    assert "data" in result
```

- [ ] **Step 4: 运行测试验证模块**

```bash
cd "J:\虚拟币犯罪调查工具集"
pytest tests/test_tron_analyzer.py -v
```

Expected: PASS（需要网络连接访问Tronscan API）

- [ ] **Step 5: 提交TRON分析模块**

```bash
git add modules/tron/ tests/test_tron_analyzer.py
git commit -m "feat: add TRON suspicious address analyzer module"
```

---

## Task 6: TRON可疑分析前端页面

**Files:**
- Create: `templates/tools/tron-suspicious.html`
- Create: `static/js/main.js`

- [ ] **Step 1: 创建static目录**

```bash
mkdir -p static/css static/js
```

- [ ] **Step 2: 创建templates/tools/tron-suspicious.html**

```html
{% extends "base.html" %}

{% block title %}TRON地址可疑分析 - 虚拟币犯罪调查工具集{% endblock %}

{% block content %}
<div class="max-w-3xl">
    <!-- 工具标题 -->
    <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-800">🔍 TRON地址可疑特征分析</h2>
        <p class="text-gray-600 mt-1">查询TRON链上地址信息，检测可疑行为特征并给出风险评分</p>
    </div>
    
    <!-- 输入区域 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
                TRON地址
            </label>
            <div class="flex gap-2">
                <input type="text" id="address" 
                       class="flex-1 border rounded-lg px-4 py-2 text-sm"
                       placeholder="输入TRON地址（以T开头，34位）">
                <button onclick="fillSample()" 
                        class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm">
                    样本填充
                </button>
            </div>
            <p class="text-xs text-gray-500 mt-1" id="sampleHint">
                样本地址: TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw
            </p>
        </div>
        
        <button onclick="startAnalysis()" 
                class="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium">
            开始分析
        </button>
    </div>
    
    <!-- 加载状态 -->
    <div id="loading" class="hidden text-center py-4">
        <div class="animate-spin inline-block w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full"></div>
        <p class="text-gray-600 mt-2">正在查询链上数据...</p>
    </div>
    
    <!-- 结果区域 -->
    <div id="result" class="hidden">
        <!-- 基本信息 -->
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <h3 class="font-semibold text-gray-800 mb-3">📊 基本信息</h3>
            <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span class="text-gray-500">地址:</span>
                    <span id="resultAddress" class="ml-2 font-mono"></span>
                </div>
                <div>
                    <span class="text-gray-500">TRX余额:</span>
                    <span id="resultTrxBalance" class="ml-2"></span>
                </div>
                <div>
                    <span class="text-gray-500">USDT余额:</span>
                    <span id="resultUsdtBalance" class="ml-2"></span>
                </div>
                <div>
                    <span class="text-gray-500">交易数:</span>
                    <span id="resultTxCount" class="ml-2"></span>
                </div>
            </div>
        </div>
        
        <!-- 警报列表 -->
        <div id="alertsContainer" class="space-y-3 mb-4"></div>
        
        <!-- 风险评分 -->
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <h3 class="font-semibold text-gray-800 mb-3">📈 风险评分</h3>
            <div class="flex items-center gap-4">
                <div id="scoreBar" class="flex-1 h-4 bg-gray-200 rounded-full overflow-hidden">
                    <div id="scoreFill" class="h-full bg-blue-600 transition-all"></div>
                </div>
                <span id="scoreValue" class="font-bold text-xl"></span>
                <span id="scoreLevel" class="text-sm px-2 py-1 rounded"></span>
            </div>
        </div>
        
        <!-- 导出按钮 -->
        <div class="flex gap-3">
            <button onclick="exportResult('json')" 
                    class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm">
                导出 JSON
            </button>
            <button onclick="exportResult('csv')" 
                    class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm">
                导出 CSV
            </button>
        </div>
    </div>
    
    <!-- 错误提示 -->
    <div id="error" class="hidden bg-red-50 border border-red-200 rounded-lg p-4">
        <p class="text-red-700" id="errorMsg"></p>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script src="/static/js/main.js"></script>
<script>
// 样本数据
const SAMPLE_ADDRESS = "TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw";
let analysisResult = null;

function fillSample() {
    document.getElementById('address').value = SAMPLE_ADDRESS;
}

async function startAnalysis() {
    const address = document.getElementById('address').value.trim();
    
    if (!address) {
        showError('请输入TRON地址');
        return;
    }
    
    if (!address.startsWith('T') || address.length !== 34) {
        showError('地址格式不正确，TRON地址应以T开头，长度34位');
        return;
    }
    
    // 显示加载状态
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    try {
        const response = await fetch('/api/v1/tron/address', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({address: address})
        });
        
        const data = await response.json();
        analysisResult = data;
        
        if (data.status === 'success') {
            displayResult(data);
        } else {
            showError(data.message || '分析失败');
        }
    } catch (err) {
        showError('网络请求失败: ' + err.message);
    }
    
    document.getElementById('loading').classList.add('hidden');
}

function displayResult(data) {
    const d = data.data;
    
    // 基本信息
    document.getElementById('resultAddress').textContent = d.address;
    document.getElementById('resultTrxBalance').textContent = d.balance.toFixed(6) + ' TRX';
    document.getElementById('resultUsdtBalance').textContent = d.usdt_balance.toFixed(2) + ' USDT';
    document.getElementById('resultTxCount').textContent = d.total_transactions;
    
    // 警报列表
    const alertsContainer = document.getElementById('alertsContainer');
    alertsContainer.innerHTML = '';
    
    // 红色警报
    for (const alert of d.alerts.red || []) {
        alertsContainer.innerHTML += `
            <div class="alert-red border rounded-lg p-4">
                <div class="font-semibold text-red-800">⚠️ 红色警报: ${alert.feature}</div>
                <div class="text-sm text-red-700 mt-1">${alert.detail}</div>
                <div class="text-xs text-red-600 mt-1">${alert.meaning}</div>
            </div>`;
    }
    
    // 黄色预警
    for (const alert of d.alerts.yellow || []) {
        alertsContainer.innerHTML += `
            <div class="alert-yellow border rounded-lg p-4">
                <div class="font-semibold text-yellow-800">⚡ 黄色预警: ${alert.feature}</div>
                <div class="text-sm text-yellow-700 mt-1">${alert.detail}</div>
                <div class="text-xs text-yellow-600 mt-1">${alert.meaning}</div>
            </div>`;
    }
    
    // 绿色正常
    for (const alert of d.alerts.green || []) {
        alertsContainer.innerHTML += `
            <div class="alert-green border rounded-lg p-4">
                <div class="font-semibold text-green-800">✅ 正常: ${alert.feature}</div>
                <div class="text-sm text-green-700 mt-1">${alert.detail}</div>
                <div class="text-xs text-green-600 mt-1">${alert.meaning}</div>
            </div>`;
    }
    
    // 风险评分
    const score = d.score;
    document.getElementById('scoreFill').style.width = score + '%';
    document.getElementById('scoreValue').textContent = score + '/100';
    
    const scoreLevel = document.getElementById('scoreLevel');
    if (score >= 70) {
        scoreLevel.textContent = '高风险';
        scoreLevel.className = 'text-sm px-2 py-1 rounded bg-red-100 text-red-700';
        document.getElementById('scoreFill').className = 'h-full bg-red-600 transition-all';
    } else if (score >= 40) {
        scoreLevel.textContent = '中等风险';
        scoreLevel.className = 'text-sm px-2 py-1 rounded bg-yellow-100 text-yellow-700';
        document.getElementById('scoreFill').className = 'h-full bg-yellow-500 transition-all';
    } else {
        scoreLevel.textContent = '低风险';
        scoreLevel.className = 'text-sm px-2 py-1 rounded bg-green-100 text-green-700';
        document.getElementById('scoreFill').className = 'h-full bg-green-500 transition-all';
    }
    
    document.getElementById('result').classList.remove('hidden');
}

function showError(msg) {
    document.getElementById('errorMsg').textContent = msg;
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
}

function exportResult(format) {
    if (!analysisResult) return;
    
    const address = analysisResult.data.address;
    const timestamp = new Date().toISOString().slice(0,19).replace(/[:-]/g,'');
    const filename = `tron_${address.slice(0,8)}_${timestamp}.${format}`;
    
    if (format === 'json') {
        const content = JSON.stringify(analysisResult, null, 2);
        downloadFile(content, filename, 'application/json');
    } else if (format === 'csv') {
        // 简化CSV导出
        let csv = '地址,TRX余额,USDT余额,交易数,风险评分\n';
        csv += `${analysisResult.data.address},${analysisResult.data.balance},${analysisResult.data.usdt_balance},${analysisResult.data.total_transactions},${analysisResult.data.score}`;
        downloadFile(csv, filename, 'text/csv');
    }
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], {type: mimeType});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}
</script>
{% endblock %}
```

- [ ] **Step 3: 创建static/js/main.js（通用工具函数）**

```javascript
/** 
 * 通用前端工具函数
 */

// 显示提示消息
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg text-white z-50 ${
        type === 'error' ? 'bg-red-500' : 
        type === 'success' ? 'bg-green-500' : 'bg-blue-500'
    }`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('已复制到剪贴板', 'success');
    }).catch(() => {
        showToast('复制失败', 'error');
    });
}

// 格式化时间戳
function formatTimestamp(ts) {
    if (!ts) return '未知';
    const date = new Date(ts);
    return date.toLocaleString('zh-CN');
}

// 格式化金额
function formatAmount(amount, decimals = 6) {
    if (amount === 0) return '0';
    return parseFloat(amount).toFixed(decimals);
}
```

- [ ] **Step 4: 启动Flask验证完整功能**

```bash
python app.py
# 浏览器打开 http://localhost:5000
# 点击侧边栏 "TRON地址可疑分析"
# 点击 "样本填充" 验证地址填充
# 点击 "开始分析" 验证API调用和结果展示
# 点击 "导出 JSON" 验证导出功能
```

Expected: 完整工作流程正常

- [ ] **Step 5: 提交前端页面**

```bash
git add templates/tools/tron-suspicious.html static/
git commit -m "feat: add TRON suspicious analyzer frontend page with export"
```

---

## Task 7: 完善和验收

**Files:**
- Modify: `app.py` (添加导出API路由)
- Create: `static/css/custom.css`

- [ ] **Step 1: 在app.py添加导出API**

在 `app.py` 的API路由部分添加：

```python
# ==================== 导出API ====================

@app.route('/api/v1/export/<format>', methods=['POST'])
def api_export(format):
    """导出结果"""
    from modules.core.exporter import Exporter
    
    data = request.get_json()
    
    if format == 'json':
        content = Exporter.to_json(data)
        return jsonify({"content": content, "filename": "export.json"})
    elif format == 'csv':
        content = Exporter.to_csv(data)
        return jsonify({"content": content, "filename": "export.csv"})
    else:
        return jsonify({"status": "error", "message": "不支持该格式"}), 400
```

- [ ] **Step 2: 创建static/css/custom.css**

```css
/* 自定义样式补充 */

/* 动画效果 */
.animate-spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* 结果卡片样式 */
.result-card {
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* 警报颜色 */
.alert-red { background-color: #fee2e2; border-left: 4px solid #ef4444; }
.alert-yellow { background-color: #fef3c7; border-left: 4px solid #f59e0b; }
.alert-green { background-color: #d1fae5; border-left: 4px solid #10b981; }

/* 评分进度条 */
.score-bar {
    height: 8px;
    background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ef4444 100%);
    border-radius: 4px;
}

/* 地址显示 */
.address-display {
    font-family: monospace;
    font-size: 0.875rem;
    word-break: break-all;
}
```

- [ ] **Step 3: 运行所有测试**

```bash
cd "J:\虚拟币犯罪调查工具集"
pytest tests/ -v
```

Expected: 所有测试PASS

- [ ] **Step 4: 最终启动验证**

```bash
python app.py
# 完整验证:
# 1. 首页显示4个分组
# 2. 侧边栏导航正常
# 3. TRON分析工具完整工作
# 4. 样本填充功能
# 5. API调用和结果展示
# 6. 导出功能
# 7. 底部法律声明显示
```

Expected: 全部功能正常

- [ ] **Step 5: 提交最终版本**

```bash
git add -A
git commit -m "feat: complete Phase 1 - core framework with TRON analyzer"
```

---

## Phase 1 完成标准

- [ ] `run.bat` 双击可启动
- [ ] 首页显示工具概览和4个分组
- [ ] 侧边栏导航正常切换
- [ ] TRON可疑分析工具完整可用：
    - 样本填充按钮正常
    - API调用成功返回数据
    - 结果正确显示（红/黄/绿警报）
    - 风险评分正确计算
    - 导出JSON/CSV功能正常
- [ ] 底部法律声明显示

---

## 后续Phase计划概述

**Phase 2: 地址分析工具（3个）**
- TRON地址行为分析（复用001-day2脚本）
- ETH交易查询（复用002-day1脚本）

**Phase 3: 交易追踪工具（3个）**
- Uniswap追踪（复用002-day3脚本）
- 混币器追踪（复用002-day2脚本）
- BTC交易分析（复用004-day1脚本）

**Phase 4: 跨链分析工具（2个）**
- 地址聚类（复用004-day2脚本）
- 跨境协查（复用004-day3脚本）

**Phase 5: 案件处理工具（3个）**
- 多链监控（复用005-day1脚本）
- 混淆攻击对抗（复用005-day2脚本）
- 资产追回冻结（复用005-day3脚本）

**Phase 6: 文档完善**
- 用户手册（11个工具说明书）
- API获取指南（Tronscan/Etherscan/Blockchain）

---

*计划创建日期: 2026-04-23*