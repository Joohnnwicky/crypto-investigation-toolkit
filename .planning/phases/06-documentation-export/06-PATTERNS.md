# Phase 6: Documentation & Export - Pattern Map

**Mapped:** 2026-04-24
**Files analyzed:** 24 (12 new + 12 modified)
**Analogs found:** 22 / 24

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `modules/docs/routes.py` | controller | request-response | `modules/tron/routes.py` | exact |
| `modules/docs/__init__.py` | config | request-response | `modules/tron/__init__.py` | exact |
| `modules/docs/pdf_exporter.py` | service | file-I/O | `modules/core/exporter.py` | exact |
| `modules/core/exporter.py` (extend) | service | file-I/O | `modules/core/exporter.py` | same file |
| `templates/docs/manuals.html` | component | request-response | `templates/index.html` | exact |
| `templates/docs/manual_tron_suspicious.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_tron_behavior.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_eth_query.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_uniswap.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_mixer.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_btc.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_cluster.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_cross_border.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_monitor.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_obfuscation.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/manual_asset_freeze.html` | component | request-response | `templates/tron/suspicious_analyzer.html` | role-match |
| `templates/docs/api_guide.html` | component | request-response | `templates/index.html` | role-match |
| `templates/base.html` (extend) | component | request-response | `templates/base.html` | same file |
| `templates/tron/suspicious_analyzer.html` (extend) | component | request-response | `templates/tron/suspicious_analyzer.html` | same file |
| `templates/tron/behavior_analyzer.html` (extend) | component | request-response | `templates/tron/suspicious_analyzer.html` | exact |
| `templates/eth/transaction_query.html` (extend) | component | request-response | `templates/tron/suspicious_analyzer.html` | exact |
| `templates/trace/uniswap.html` (extend) | component | request-response | `templates/trace/btc.html` | exact |
| `templates/trace/mixer.html` (extend) | component | request-response | `templates/trace/btc.html` | exact |
| `templates/trace/btc.html` (extend) | component | request-response | `templates/trace/btc.html` | same file |
| `templates/cross/cluster.html` (extend) | component | request-response | `templates/tron/suspicious_analyzer.html` | exact |
| `templates/cross/cross_border.html` (extend) | component | request-response | `templates/tron/suspicious_analyzer.html` | exact |
| `templates/case/monitor.html` (extend) | component | request-response | `templates/case/monitor.html` | same file |
| `templates/case/obfuscation.html` (extend) | component | request-response | `templates/case/monitor.html` | exact |
| `templates/case/asset_freeze.html` (extend) | component | request-response | `templates/case/monitor.html` | exact |
| `app.py` (extend) | config | request-response | `app.py` | same file |

## Pattern Assignments

### `modules/docs/routes.py` (controller, request-response)

**Analog:** `modules/tron/routes.py`

**Imports pattern** (lines 1-8):
```python
from flask import Blueprint, jsonify, request, Response, render_template
from .suspicious_analyzer import analyze_address_web, is_valid_tron_address
from .behavior_analyzer import analyze_behavior_web
from modules.core.exporter import export_json, export_csv, get_export_filename

tron_bp = Blueprint('tron', __name__, url_prefix='/tron')
```

**Route handler pattern** (lines 48-72):
```python
@tron_bp.route('/api/export/json', methods=['POST'])
def export_json_endpoint():
    """Export analysis result as JSON file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: JSON file download with Content-Disposition header
    """
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    json_content = export_json(result)

    from modules.core.exporter import get_export_filename
    filename = get_export_filename(address, 'json')

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response
```

**Page route pattern** (lines 99-108):
```python
@tron_bp.route('/behavior-analyzer')
def behavior_analyzer_page():
    """Render TRON address behavior analysis tool page.

    Returns:
        HTML template for behavior analyzer with 4 Summary Cards
    """
    return render_template('tron/behavior_analyzer.html')
```

---

### `modules/docs/__init__.py` (config, request-response)

**Analog:** `modules/tron/__init__.py`

**Pattern** (line 1):
```python
"""TRON blockchain analysis modules"""
```

**Adapted for docs:**
```python
"""Documentation and PDF export modules"""
```

---

### `modules/docs/pdf_exporter.py` (service, file-I/O)

**Analog:** `modules/core/exporter.py`

**Imports pattern** (lines 1-6):
```python
"""Export utilities for analysis results - JSON and CSV formats"""

import json
import csv
from io import StringIO
from typing import Dict, Any
```

**Export function pattern** (lines 8-17):
```python
def export_json(data: Dict[str, Any]) -> str:
    """Convert analysis result to JSON string for download.

    Args:
        data: Analysis result dict (basic_info, alerts, etc.)

    Returns:
        JSON string with Chinese characters preserved (ensure_ascii=False)
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
```

**Filename pattern** (lines 79-93):
```python
def get_export_filename(address: str, format_type: str, analysis_type: str = 'analysis') -> str:
    """Generate filename for export download.

    Args:
        address: TRON address being analyzed
        format_type: "json" or "csv"
        analysis_type: Type of analysis ("analysis", "behavior", etc.)

    Returns:
        Filename like "tron_behavior_TUtP...NNw_20240115.json"
    """
    from datetime import datetime
    date_str = datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    return f"tron_{analysis_type}_{addr_short}_{date_str}.{format_type}"
```

---

### `modules/core/exporter.py` (extend - service, file-I/O)

**Existing file to extend. Add PDF export function after line 93.**

**New function to add (pattern from existing export_json):**
```python
def export_pdf(data: Dict[str, Any], tool_type: str) -> bytes:
    """Convert analysis result to PDF bytes using WeasyPrint.

    Args:
        data: Analysis result dict
        tool_type: Tool identifier for template selection

    Returns:
        PDF bytes for download
    """
    from weasyprint import HTML
    from flask import render_template_string
    
    html_template = get_pdf_template(tool_type)
    html_content = render_template_string(html_template, result=data)
    pdf = HTML(string=html_content).write_pdf()
    return pdf

def get_pdf_filename(address: str, tool_type: str) -> str:
    """Generate PDF filename following existing pattern."""
    from datetime import datetime
    date_str = datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    return f"{tool_type}_{addr_short}_{date_str}.pdf"
```

---

### `templates/docs/manuals.html` (component, request-response)

**Analog:** `templates/index.html`

**Template extends pattern** (lines 1-2):
```html
{% extends "base.html" %}
{% block title %}虚拟币犯罪调查工具集{% endblock %}
```

**Card grid pattern** (lines 14-35):
```html
<!-- Tool categories -->
<div class="space-y-6">
    <!-- Category 1: Address Analysis -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="bg-blue-500 text-white px-3 py-1 rounded mr-3">地址分析</span>
            区块链地址行为特征分析
        </h2>
        <div class="grid grid-cols-3 gap-4">
            <a href="/tron/suspicious-analyzer" class="block p-4 bg-gray-50 rounded hover:bg-gray-100 transition border border-gray-200">
                <h3 class="font-bold text-gray-700">TRON可疑分析</h3>
                <p class="text-sm text-gray-500 mt-1">识别诈骗/洗钱可疑特征</p>
            </a>
            <a href="/tron/behavior-analyzer" class="block p-4 bg-gray-50 rounded hover:bg-gray-100 transition border border-gray-200">
                <h3 class="font-bold text-gray-700">TRON行为分析</h3>
                <p class="text-sm text-gray-500 mt-1">分析地址交易行为模式</p>
            </a>
            <a href="/eth/transaction-query" class="block p-4 bg-gray-50 rounded hover:bg-gray-100 transition border border-gray-200">
                <h3 class="font-bold text-gray-700">ETH交易查询</h3>
                <p class="text-sm text-gray-500 mt-1">查询以太坊交易记录</p>
            </a>
        </div>
    </div>
</div>
```

**Documentation link pattern** (lines 100-105):
```html
<!-- Documentation link -->
<div class="mt-8 bg-gray-100 rounded-lg p-6 text-center">
    <a href="/docs/manuals" class="text-blue-600 hover:text-blue-800 font-bold">
        查看使用手册与API获取指南
    </a>
</div>
```

---

### `templates/docs/manual_*.html` (component, request-response)

**Analog:** `templates/tron/suspicious_analyzer.html`

**Template structure pattern** (lines 1-10):
```html
{% extends "base.html" %}
{% block title %}TRON可疑特征分析{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <!-- Tool header -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">TRON地址可疑特征分析</h1>
        <p class="text-gray-600">识别诈骗/洗钱等可疑行为特征，生成风险评分报告</p>
    </div>
```

**Content section pattern** (lines 51-54):
```html
<!-- Basic info -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-bold text-gray-700 mb-4">基本信息</h2>
    <div id="basic-info" class="grid grid-cols-2 gap-4"></div>
</div>
```

**Adapted for manual pages (4-section structure):**
```html
{% extends "base.html" %}
{% block title %}TRON可疑分析 - 使用手册{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">TRON地址可疑特征分析</h1>
        <p class="text-gray-600">操作步骤、结果解释、API说明与案例演示</p>
    </div>

    <!-- Section 1: 操作步骤 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-lg font-bold text-gray-700 mb-4">操作步骤</h2>
        <ol class="list-decimal list-inside space-y-2">
            <li>输入TRON钱包地址（34位，以T开头）</li>
            <li>点击"加载样本"按钮查看示例地址格式</li>
            <li>点击"开始分析"按钮</li>
            <li>等待API返回数据，查看分析结果</li>
        </ol>
    </div>

    <!-- Section 2: 结果解释 -->
    <!-- Section 3: API密钥说明 -->
    <!-- Section 4: 案例演示 -->
</div>
{% endblock %}
```

---

### `templates/docs/api_guide.html` (component, request-response)

**Analog:** `templates/index.html` (static page layout)

**Layout pattern** (lines 5-11):
```html
<div class="max-w-4xl mx-auto">
    <!-- Hero section -->
    <div class="bg-gradient-to-r from-gray-800 to-gray-900 rounded-lg p-8 mb-8 text-white">
        <h1 class="text-3xl font-bold mb-4">虚拟币犯罪调查工具集</h1>
        <p class="text-gray-300 mb-2">为虚拟货币犯罪调查初学者构建的本地运行Web工具集</p>
        <p class="text-gray-400 text-sm">一键本地启动，零配置使用。配合说明书理解结果含义。</p>
    </div>
```

**Section card pattern** (lines 16-20):
```html
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
        <span class="bg-blue-500 text-white px-3 py-1 rounded mr-3">地址分析</span>
        区块链地址行为特征分析
    </h2>
```

---

### `templates/base.html` (extend - component, request-response)

**Existing file to extend. Add API guide link after line 54.**

**Sidebar navigation pattern** (lines 31-55):
```html
{% block sidebar %}
<aside class="w-64 bg-gray-900 text-white fixed h-full">
    <!-- Application title/logo -->
    <h1 class="text-xl font-bold p-4 border-b border-gray-700">虚拟币犯罪调查工具集</h1>
    <!-- Navigation menu with active state highlighting via Jinja2 request.path -->
    <nav class="p-4 space-y-2">
        <a href="/" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/' %} bg-gray-700{% endif %}">首页</a>
        <!-- TRON blockchain analysis tools -->
        <a href="/tron/suspicious-analyzer" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/tron/suspicious-analyzer' %} bg-gray-700{% endif %}">TRON可疑分析</a>
        <!-- ... more nav links ... -->
        <!-- Documentation -->
        <a href="/docs/manuals" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/manuals' %} bg-gray-700{% endif %}">使用手册</a>
    </nav>
</aside>
{% endblock %}
```

**Add after line 54:**
```html
<a href="/docs/api-guide" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/api-guide' %} bg-gray-700{% endif %}">API获取指南</a>
```

---

### `templates/tron/suspicious_analyzer.html` (extend - add PDF button)

**Existing file to extend. Add PDF button at lines 83-96.**

**Export button pattern** (lines 83-96):
```html
<!-- Export buttons -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-bold text-gray-700 mb-4">导出结果</h2>
    <div class="flex space-x-4">
        <button onclick="exportJSON()"
                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
            导出JSON
        </button>
        <button onclick="exportCSV()"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
            导出CSV
        </button>
    </div>
</div>
```

**Add PDF button (purple color for differentiation):**
```html
<button onclick="exportPDF()"
        class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">
    导出PDF
</button>
```

**Export JavaScript pattern** (lines 226-254):
```javascript
function exportJSON() {
    if (!analysisResult) {
        alert('请先进行地址分析');
        return;
    }

    fetch('/tron/api/export/json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ result: analysisResult })
    })
    .then(response => {
        const filename = response.headers.get('Content-Disposition').split('filename=')[1].replace(/"/g, '');
        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        alert('导出失败: ' + error.message);
    });
}
```

**Add PDF export function:**
```javascript
function exportPDF() {
    if (!analysisResult) {
        alert('请先进行地址分析');
        return;
    }

    fetch('/docs/api/export/pdf', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            result: analysisResult,
            tool_type: 'tron_suspicious'
        })
    })
    .then(response => {
        const filename = response.headers.get('Content-Disposition')
            .split('filename=')[1].replace(/"/g, '');
        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => alert('PDF导出失败: ' + error.message));
}
```

---

### `templates/tron/behavior_analyzer.html` (extend - add PDF button)

**Analog:** `templates/tron/suspicious_analyzer.html` (same export button pattern at lines 110-123)

**Export button pattern** (lines 110-123):
```html
<!-- Export buttons -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-bold text-gray-700 mb-4">导出结果</h2>
    <div class="flex space-x-4">
        <button onclick="exportJSON()"
                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
            导出JSON
        </button>
        <button onclick="exportCSV()"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
            导出CSV
        </button>
    </div>
</div>
```

---

### `templates/trace/btc.html` (extend - add PDF button)

**Analog:** `templates/tron/suspicious_analyzer.html` (same export button pattern at lines 77-89)

**Export button pattern** (lines 77-89):
```html
<!-- Export -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-bold text-gray-700 mb-4">导出结果</h2>
    <div class="flex space-x-4">
        <button onclick="exportJSON()"
                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
            导出JSON
        </button>
        <button onclick="exportCSV()"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
            导出CSV
        </button>
    </div>
</div>
```

---

### `templates/case/monitor.html` (extend - add PDF button)

**Analog:** `templates/tron/suspicious_analyzer.html` (same export button pattern at lines 164-174)

**Export button pattern** (lines 164-174):
```html
// Export buttons
html += '<div class="bg-white rounded-lg shadow p-6 mb-6">';
html += '<h2 class="text-lg font-semibold text-gray-800 mb-4">导出结果</h2>';
html += '<div class="flex flex-wrap gap-3">';
html += `<button onclick="exportJSON()" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">导出JSON</button>`;
html += `<button onclick="exportCSV()" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">导出CSV</button>`;
```

---

### `app.py` (extend - config, request-response)

**Existing file to extend. Add docs blueprint registration after line 17.**

**Blueprint registration pattern** (lines 10-17):
```python
from flask import Flask, render_template
from modules.tron.routes import tron_bp
from modules.eth.routes import eth_bp
from modules.trace.routes import trace_bp
from modules.cross.routes import cross_bp
from modules.case.routes import case_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(tron_bp)
app.register_blueprint(eth_bp)
app.register_blueprint(trace_bp)
app.register_blueprint(cross_bp)
app.register_blueprint(case_bp)
```

**Add docs blueprint:**
```python
from modules.docs.routes import docs_bp
# ...
app.register_blueprint(docs_bp)
```

---

## Shared Patterns

### Flask Blueprint Structure

**Source:** `modules/tron/routes.py`
**Apply to:** `modules/docs/routes.py`

```python
from flask import Blueprint, jsonify, request, Response, render_template

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')
```

### Export Response Pattern

**Source:** `modules/tron/routes.py` lines 67-72
**Apply to:** PDF export endpoint in `modules/docs/routes.py`

```python
response = Response(
    content_bytes,
    mimetype='application/pdf',
    headers={'Content-Disposition': f'attachment; filename="{filename}"'}
)
return response
```

### Export Button Trio Pattern

**Source:** `templates/tron/suspicious_analyzer.html` lines 83-96
**Apply to:** All 11 tool templates

```html
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-bold text-gray-700 mb-4">导出结果</h2>
    <div class="flex space-x-4">
        <button onclick="exportJSON()" class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">导出JSON</button>
        <button onclick="exportCSV()" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">导出CSV</button>
        <!-- ADD: PDF button -->
        <button onclick="exportPDF()" class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">导出PDF</button>
    </div>
</div>
```

### Sidebar Navigation Link Pattern

**Source:** `templates/base.html` line 54
**Apply to:** Add API guide link after manuals link

```html
<a href="/docs/manuals" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/manuals' %} bg-gray-700{% endif %}">使用手册</a>
<a href="/docs/api-guide" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/api-guide' %} bg-gray-700{% endif %}">API获取指南</a>
```

### Card Grid Layout Pattern

**Source:** `templates/index.html` lines 21-34
**Apply to:** `templates/docs/manuals.html`

```html
<div class="grid grid-cols-3 gap-4">
    <a href="/docs/manual/tron-suspicious" class="block p-4 bg-gray-50 rounded hover:bg-gray-100 transition border border-gray-200">
        <h3 class="font-bold text-gray-700">TRON可疑分析</h3>
        <p class="text-sm text-gray-500 mt-1">说明书与操作指南</p>
    </a>
</div>
```

### Filename Generation Pattern

**Source:** `modules/core/exporter.py` lines 79-93
**Apply to:** PDF filename in `modules/docs/pdf_exporter.py`

```python
from datetime import datetime
date_str = datetime.now().strftime('%Y%m%d')
addr_short = address[:8] + address[-4:] if len(address) > 12 else address
return f"{tool_type}_{addr_short}_{date_str}.pdf"
```

---

## No Analog Found

All files have analogs found. No files require patterns from RESEARCH.md only.

---

## Metadata

**Analog search scope:**
- `modules/` directory (routes.py, exporter.py, __init__.py patterns)
- `templates/` directory (base.html, index.html, tool templates)
- `app.py` (blueprint registration)

**Files scanned:** 15 files
**Pattern extraction date:** 2026-04-24

**Key pattern sources:**
- `modules/tron/routes.py` - Blueprint structure, export endpoints
- `modules/core/exporter.py` - Export functions, filename generation
- `templates/base.html` - Sidebar navigation
- `templates/index.html` - Card grid layout
- `templates/tron/suspicious_analyzer.html` - Export button trio, page structure
- `templates/trace/btc.html` - Alternative export button pattern
- `templates/case/monitor.html` - Dynamically generated export buttons