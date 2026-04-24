# Phase 5: Case Handling Tools - Pattern Map

**Mapped:** 2026-04-24
**Files analyzed:** 8 new files
**Analogs found:** 8 / 8

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `modules/case/__init__.py` | config | - | `modules/cross/__init__.py` | exact |
| `modules/case/routes.py` | route | request-response | `modules/cross/routes.py` | exact |
| `modules/case/monitor.py` | service | request-response, multi-address | `modules/cross/cluster_analyzer.py` | exact |
| `modules/case/obfuscation_detector.py` | service | request-response, confidence-scoring | `modules/trace/mixer_tracker.py` | exact |
| `modules/case/asset_freeze_generator.py` | service | request-response, template-gen | `modules/cross/cross_border_generator.py` | exact |
| `templates/case/monitor.html` | component | request-response, card-display | `templates/cross/cluster.html` | exact |
| `templates/case/obfuscation.html` | component | request-response, card-display | `templates/cross/cluster.html` | exact |
| `templates/case/asset_freeze.html` | component | request-response, step-by-step | `templates/cross/cross_border.html` | exact |

---

## Pattern Assignments

### `modules/case/__init__.py` (config)

**Analog:** `modules/cross/__init__.py`

**Module docstring pattern** (line 1):
```python
"""Cross-chain analysis module for multi-address association and international coordination"""
```

**Apply:** Create similar docstring for case handling module.

---

### `modules/case/routes.py` (route, request-response)

**Analog:** `modules/cross/routes.py`

**Imports pattern** (lines 1-7):
```python
"""Flask Blueprint routes for cross-chain analysis tools"""

from flask import Blueprint, jsonify, request, Response, render_template
from modules.core.exporter import export_json
import datetime
import csv
from io import StringIO
```

**Blueprint creation pattern** (lines 9-10):
```python
# Create Blueprint for cross-chain analysis tools
cross_bp = Blueprint('cross', __name__, url_prefix='/cross')
```

**Sample data constants pattern** (lines 12-15):
```python
# Sample data constants (per D-04)
SAMPLE_TRON_ADDRESS = "TUtPv8ZD7WKxMQFQ8RyD3m5yP9NhS3qLNNw"  # Sample TRON address
SAMPLE_ETH_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT contract
SAMPLE_BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Genesis block address
```

**API endpoint pattern** (lines 20-47):
```python
@cross_bp.route('/api/cluster/query', methods=['POST'])
def cluster_query():
    """API endpoint for address clustering.

    Request JSON body: {"addresses": ["..."], "eth_key": "..."}
    Response JSON: {"success": bool, "addresses": [...], "clusters": [...], "unassociated": [...]}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    addresses = data.get('addresses', [])
    eth_key = data.get('eth_key', '')

    # Clean addresses (strip whitespace, filter empty)
    addresses = [addr.strip() for addr in addresses if addr.strip()]

    if not addresses:
        return jsonify({'success': False, 'error': '请输入至少一个地址'}), 400

    # Import and call analyzer
    from .cluster_analyzer import cluster_addresses_web
    result = cluster_addresses_web(addresses, {'eth_key': eth_key})

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400
```

**Page route pattern** (lines 50-53):
```python
@cross_bp.route('/cluster')
def cluster_page():
    """Page route for address clustering tool."""
    return render_template('cross/cluster.html')
```

**Sample endpoint pattern** (lines 56-65):
```python
@cross_bp.route('/api/cluster/sample')
def cluster_sample():
    """Sample addresses for demo (per D-04)."""
    return jsonify({
        "sample_addresses": [
            SAMPLE_TRON_ADDRESS,
            SAMPLE_ETH_ADDRESS,
            SAMPLE_BTC_ADDRESS
        ]
    })
```

**JSON export route pattern** (lines 68-86):
```python
@cross_bp.route('/api/cluster/export/json', methods=['POST'])
def cluster_export_json():
    """Export cluster result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    json_content = export_json(result)

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"cluster_result_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response
```

**CSV export route pattern** (lines 89-130):
```python
@cross_bp.route('/api/cluster/export/csv', methods=['POST'])
def cluster_export_csv():
    """Export cluster result as CSV file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    clusters = result.get('clusters', [])
    unassociated = result.get('unassociated', [])

    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['聚类ID', '地址', '链类型', '关联原因'])

    # Write clusters
    for cluster in clusters:
        cluster_id = cluster.get('cluster_id', '')
        addresses = cluster.get('addresses', [])
        chain_types = cluster.get('chain_types', [])
        reasons = cluster.get('reasons', [])
        reasons_str = '; '.join(reasons) if reasons else ''

        for i, addr in enumerate(addresses):
            chain = chain_types[i] if i < len(chain_types) else 'unknown'
            writer.writerow([cluster_id, addr, chain, reasons_str])

    # Write unassociated addresses
    for addr in unassociated:
        writer.writerow(['无', addr, 'unknown', '无关联'])

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"cluster_result_{date_str}.csv"

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response
```

---

### `modules/case/monitor.py` (service, request-response, multi-address)

**Analog:** `modules/cross/cluster_analyzer.py`

**Imports pattern** (lines 1-16):
```python
"""Address clustering module for multi-address association analysis"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .chain_detector import detect_chain_type, get_chain_requirements
from modules.core.api_client import (
    get_account_info,
    get_trc20_transfers,
    get_eth_transactions,
    get_erc20_transfers
)
from modules.trace.btc_analyzer import fetch_transaction, identify_address_type

logger = logging.getLogger(__name__)
```

**Multi-address input validation pattern** (lines 229-237):
```python
# Validate address count (D-01)
if not addresses:
    return {'success': False, 'error': '请输入至少一个地址'}

if len(addresses) > 10:
    return {'success': False, 'error': '地址数量超过10个限制'}

# Clean addresses (strip whitespace)
addresses = [addr.strip() for addr in addresses if addr.strip()]
```

**Chain detection pattern** (lines 240-254):
```python
# Detect chain types and validate
address_chain_map = {}
needs_eth_key = False

for addr in addresses:
    chain = detect_chain_type(addr)
    if chain == 'unknown':
        return {'success': False, 'error': f'无法识别地址链类型: {addr}'}
    address_chain_map[addr] = chain
    if chain == 'eth':
        needs_eth_key = True

# Validate API keys (D-03)
eth_key = api_keys.get('eth_key', '').strip()
if needs_eth_key and not eth_key:
    return {'success': False, 'error': 'ETH地址需要Etherscan API密钥'}
```

**TRON API call pattern** (lines 264-269):
```python
if chain == 'tron':
    # TRON: Use Tronscan API (free, no key required)
    account_info = get_account_info(addr)
    trc20_transfers = get_trc20_transfers(addr, limit=50)
    tx_data['account_info'] = account_info
    tx_data['trc20_transfers'] = trc20_transfers
```

**ETH API call pattern** (lines 272-276):
```python
elif chain == 'eth':
    # ETH: Use Etherscan API (requires key)
    eth_txs = get_eth_transactions(addr, eth_key, limit=100)
    erc20_transfers = get_erc20_transfers(addr, eth_key, limit=100)
    tx_data['eth_transactions'] = eth_txs
    tx_data['erc20_transfers'] = erc20_transfers
```

**BTC limited data pattern** (lines 279-283):
```python
elif chain == 'btc':
    # BTC: Blockstream free API - limited address history
    # Note: Blockstream API requires tx_hash, not address lookup
    # For clustering, we'll mark BTC addresses as limited data
    tx_data['btc_transactions'] = []
    tx_data['limited_data'] = True
```

**Error handling pattern** (lines 285-289):
```python
except Exception as e:
    logger.warning(f"Failed to fetch data for {addr}: {e}")
    tx_data['error'] = str(e)

address_data[addr] = tx_data
```

**Return structured result pattern** (lines 392-396):
```python
return {
    'success': True,
    'addresses': addresses,
    'clusters': clusters,
    'unassociated': unassociated
}
```

---

### `modules/case/obfuscation_detector.py` (service, request-response, confidence-scoring)

**Analog:** `modules/trace/mixer_tracker.py`

**Imports pattern** (lines 1-19):
```python
"""Tornado Cash mixer tracing module with time window analysis"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    Web3 = None

from modules.core.eth_rpc_client import EthRpcClient
from .tornado_pools import TORNADO_POOLS, WITHDRAWAL_EVENT_ABI, EXCHANGE_PREFIXES

# Configure logging
logger = logging.getLogger(__name__)
```

**Confidence scoring pattern** (lines 128-152):
```python
def calculate_confidence(self, withdrawal: Dict, deposit_ts: float) -> tuple:
    """Calculate confidence level for withdrawal.

    Args:
        withdrawal: Withdrawal event dict
        deposit_ts: Deposit timestamp

    Returns:
        (confidence, reason) tuple
    """
    # Check if withdrawal goes to exchange
    exchange = self.identify_exchange(withdrawal['recipient'])
    if exchange:
        return "HIGH", f"立即转入{exchange}交易所，高度可疑"

    # Check withdrawal timing
    withdraw_ts = withdrawal['timestamp']
    hours_diff = (withdraw_ts - deposit_ts) / 3600

    if hours_diff < 6:
        return "MEDIUM", f"存款后 {hours_diff:.1f} 小时即提款，较可疑"
    elif hours_diff < 24:
        return "LOW", f"存款后 {hours_diff:.1f} 小时提款"

    return "LOW", "时间窗口边缘提款"
```

**Sorting by confidence pattern** (lines 254-258):
```python
# Sort by confidence (HIGH first)
suspicious_withdrawals.sort(key=lambda x: (
    0 if x['confidence'] == 'HIGH' else
    1 if x['confidence'] == 'MEDIUM' else 2
))
```

**Web interface function pattern** (lines 233-274):
```python
def time_window_analysis_web(deposit_time: str) -> Dict[str, Any]:
    """Web interface for mixer tracing.

    Args:
        deposit_time: Deposit time string "YYYY-MM-DD HH:MM:SS"

    Returns:
        Dict with success, deposit_time, suspicious_withdrawals, flow_diagram
    """
    # Validate deposit time format
    if not validate_deposit_time(deposit_time):
        return {
            "success": False,
            "error": "无效的存款时间格式，请使用 YYYY-MM-DD HH:MM:SS 格式",
            "deposit_time": deposit_time
        }

    try:
        tracker = TornadoCashTracker()
        suspicious_withdrawals = tracker.search_all_pools(deposit_time)

        # Sort by confidence (HIGH first)
        suspicious_withdrawals.sort(key=lambda x: (
            0 if x['confidence'] == 'HIGH' else
            1 if x['confidence'] == 'MEDIUM' else 2
        ))

        return {
            "success": True,
            "deposit_time": deposit_time,
            "window_hours": DEFAULT_WINDOW_HOURS,
            "suspicious_withdrawals": suspicious_withdrawals,
            "flow_diagram": tracker.generate_flow_diagram(deposit_time, suspicious_withdrawals)
        }

    except Exception as e:
        logger.error(f"Mixer trace error: {e}")
        return {
            "success": False,
            "error": str(e),
            "deposit_time": deposit_time
        }
```

---

### `modules/case/asset_freeze_generator.py` (service, request-response, template-gen)

**Analog:** `modules/cross/cross_border_generator.py`

**Imports pattern** (lines 1-8):
```python
"""Cross-border investigation coordination template generator module"""

import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
```

**Required fields pattern** (lines 9-18):
```python
# Required fields per D-15 to D-18
REQUIRED_FIELDS = [
    'case_number',     # 案件编号 (D-15)
    'agency',          # 调查机构 (D-15)
    'contact_person',  # 联系人 (D-15)
    'contact_method',  # 联系方式 (D-15)
    'suspicious_behavior',  # 可疑行为描述 (D-17)
    'request_type',    # 请求类型 (D-18)
    'expected_response'  # 期望回复时间 (D-18)
]
```

**Field validation pattern** (lines 21-39):
```python
def validate_template_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Validate template input fields.

    Args:
        fields: Dict with template field values

    Returns:
        Dict with valid: bool, missing: list of missing required fields
    """
    missing = []
    for field in REQUIRED_FIELDS:
        value = fields.get(field, '')
        if not value or (isinstance(value, str) and not value.strip()):
            missing.append(field)

    return {
        'valid': len(missing) == 0,
        'missing': missing
    }
```

**Plain text template generation pattern** (lines 42-91):
```python
def generate_plain_text(fields: Dict[str, Any]) -> str:
    """Generate plain text version for clipboard copy (per D-13).

    Args:
        fields: Dict with all template fields

    Returns:
        Plain text template string
    """
    # Format address list
    addresses = fields.get('addresses', [])
    chain_types = fields.get('chain_types', [])
    address_list_formatted = ""
    for i, addr in enumerate(addresses):
        chain = chain_types[i] if i < len(chain_types) else 'unknown'
        address_list_formatted += f"  {addr} ({chain})\n"

    # Format tx hashes
    tx_hashes = fields.get('tx_hashes', [])
    tx_list_formatted = ""
    for tx in tx_hashes:
        tx_list_formatted += f"  {tx}\n"

    template = f"""
跨境虚拟货币调查协查请求

案件编号: {fields.get('case_number', '')}
调查机构: {fields.get('agency', '')}
联系人: {fields.get('contact_person', '')}
联系方式: {fields.get('contact_method', '')}

涉案地址:
{address_list_formatted if addresses else '  无'}

金额汇总: {fields.get('total_amount', '未知')}
交易哈希:
{tx_list_formatted if tx_hashes else '  无'}

可疑行为描述: {fields.get('suspicious_behavior', '')}
资金流向简述: {fields.get('fund_flow', '')}
调查背景: {fields.get('investigation_context', '')}

请求类型: {fields.get('request_type', '')}
期望回复时间: {fields.get('expected_response', '')}

---
本协查请求由虚拟币犯罪调查工具集生成，仅供合规调查使用。
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template.strip()
```

**Template generation web function pattern** (lines 94-145):
```python
def generate_template_web(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Generate cross-border coordination template (per D-14 to D-18).

    Args:
        fields: Dict with case_info, address_info, background, request

    Returns:
        Dict with success, template_data, plain_text
    """
    # Validate required fields
    validation = validate_template_fields(fields)
    if not validation['valid']:
        missing_str = ', '.join(validation['missing'])
        return {
            'success': False,
            'error': f'缺少必填字段: {missing_str}'
        }

    # Build structured template data for frontend rendering
    template_data = {
        'case_info': {
            'case_number': fields.get('case_number', ''),
            'agency': fields.get('agency', ''),
            'contact_person': fields.get('contact_person', ''),
            'contact_method': fields.get('contact_method', '')
        },
        'address_info': {
            'addresses': fields.get('addresses', []),
            'chain_types': fields.get('chain_types', []),
            'total_amount': fields.get('total_amount', '未知'),
            'tx_hashes': fields.get('tx_hashes', [])
        },
        'background': {
            'suspicious_behavior': fields.get('suspicious_behavior', ''),
            'fund_flow': fields.get('fund_flow', ''),
            'investigation_context': fields.get('investigation_context', '')
        },
        'request': {
            'request_type': fields.get('request_type', ''),
            'expected_response': fields.get('expected_response', '')
        },
        'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Generate plain text version for copy
    plain_text = generate_plain_text(fields)

    return {
        'success': True,
        'template_data': template_data,
        'plain_text': plain_text
    }
```

---

### `templates/case/monitor.html` (component, request-response, card-display)

**Analog:** `templates/cross/cluster.html`

**Template extends pattern** (line 1):
```html
{% extends "base.html" %}
{% block title %}地址聚类分析 - CIT{% endblock %}
```

**Input section pattern** (lines 12-44):
```html
<!-- Input section -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-semibold text-gray-800 mb-4">输入地址</h2>

    <!-- Address textarea (per D-01) -->
    <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">钱包地址（每行一个，最多10个）</label>
        <textarea id="addresses-input"
                  class="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  rows="5"
                  placeholder="每行一个地址，最多10个地址（支持TRON/ETH/BTC）"></textarea>
    </div>

    <!-- ETH API key input (per D-03) -->
    <div id="eth-key-section" class="mb-4 hidden">
        <label class="block text-sm font-medium text-gray-700 mb-1">Etherscan API密钥</label>
        <input type="text" id="eth-key-input"
               class="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
               placeholder="从 etherscan.io 获取免费API密钥">
        <p class="text-sm text-gray-500 mt-1">ETH地址分析需要API密钥</p>
    </div>

    <!-- Buttons -->
    <div class="flex gap-3">
        <button onclick="fillSample()"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition">
            样本填充
        </button>
        <button onclick="analyzeCluster()"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            开始分析
        </button>
    </div>
</div>
```

**Loading indicator pattern** (lines 47-50):
```html
<!-- Loading indicator -->
<div id="loading" class="hidden bg-white rounded-lg shadow p-6 mb-6 text-center">
    <div class="animate-spin inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full"></div>
    <p class="text-gray-600 mt-2">正在分析地址关联...</p>
</div>
```

**Error display pattern** (lines 53-55):
```html
<!-- Error display -->
<div id="error-display" class="hidden bg-red-100 border border-red-400 rounded-lg p-4 mb-6">
    <p id="error-message" class="text-red-700"></p>
</div>
```

**Card display pattern** (lines 186-218):
```javascript
// Display single cluster card
function displayClusterCard(cluster) {
    let html = `<div class="border rounded-lg p-4 mb-4">`;
    html += `<div class="flex justify-between items-center mb-2">`;
    html += `<span class="font-semibold text-blue-600">聚类 ${cluster.cluster_id}</span>`;
    html += `<span class="text-gray-500">${cluster.addresses.length} 个地址</span>`;
    html += `</div>`;

    // Addresses list
    html += `<div class="mb-2"><span class="text-sm text-gray-600">地址列表:</span>`;
    for (let i = 0; i < cluster.addresses.length; i++) {
        const addr = cluster.addresses[i];
        const chain = cluster.chain_types[i] || 'unknown';
        html += `<p class="text-sm ml-2">${addr} (${chain})</p>`;
    }
    html += `</div>`;

    // Reasons (per D-10)
    html += `<div class="mb-2"><span class="text-sm text-gray-600">关联原因:</span>`;
    for (const reason of cluster.reasons) {
        html += `<p class="text-sm text-green-600 ml-2">✓ ${reason}</p>`;
    }
    html += `</div>`;

    // Stats
    if (cluster.stats) {
        html += `<div class="text-sm text-gray-500">`;
        html += `交易总数: ${cluster.stats.total_transactions || '未知'}`;
        html += `</div>`;
    }

    html += `</div>`;
    return html;
}
```

**Export buttons pattern** (lines 173-179):
```javascript
// Export buttons (per D-12, D-20)
html += '<div class="bg-white rounded-lg shadow p-6 mb-6">';
html += '<h2 class="text-lg font-semibold text-gray-800 mb-4">导出结果</h2>';
html += '<div class="flex gap-3">';
html += `<button onclick="exportJSON()" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">导出JSON</button>`;
html += `<button onclick="exportCSV()" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">导出CSV</button>`;
html += `<button onclick="exportToCrossBorder()" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition">导出到跨境协查</button>`;
html += '</div></div>';
```

**sessionStorage cache pattern** (lines 64-65, 133-134, 301-307):
```javascript
// Session cache key
const CACHE_KEY = 'cit_cluster_result';

// Cache result
sessionStorage.setItem(CACHE_KEY, JSON.stringify(data));

// Restore from cache on page load
window.onload = function() {
    const cached = sessionStorage.getItem(CACHE_KEY);
    if (cached) {
        const data = JSON.parse(cached);
        displayResults(data);
    }
};
```

---

### `templates/case/obfuscation.html` (component, request-response, card-display)

**Analog:** `templates/cross/cluster.html` (same patterns as monitor.html)

Use the same patterns from `templates/cross/cluster.html` as documented above for monitor.html.

**Additional confidence color coding:** Apply confidence-based styling (HIGH=red, MEDIUM=yellow, LOW=blue) to attack cards, based on the mixer_tracker.py confidence pattern.

---

### `templates/case/asset_freeze.html` (component, request-response, step-by-step)

**Analog:** `templates/cross/cross_border.html`

**Step indicators pattern** (lines 11-27):
```html
<!-- Step indicators (per D-19) -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <div class="flex justify-between items-center">
        <div id="step1-indicator" class="flex-1 text-center">
            <div class="w-8 h-8 mx-auto rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">1</div>
            <p class="text-sm mt-2 text-blue-600 font-medium">案件基本信息</p>
        </div>
        <div class="flex-1 text-center border-l">
            <div id="step2-indicator" class="w-8 h-8 mx-auto rounded-full bg-gray-300 text-gray-600 flex items-center justify-center font-bold">2</div>
            <p class="text-sm mt-2 text-gray-500">涉案地址选择</p>
        </div>
        <div class="flex-1 text-center border-l">
            <div id="step3-indicator" class="w-8 h-8 mx-auto rounded-full bg-gray-300 text-gray-600 flex items-center justify-center font-bold">3</div>
            <p class="text-sm mt-2 text-gray-500">调查背景与请求</p>
        </div>
    </div>
</div>
```

**Step section pattern** (lines 29-65):
```html
<!-- Step 1: Case Info (per D-15) -->
<div id="step1-section" class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-semibold text-gray-800 mb-4">案件基本信息</h2>

    <div class="grid grid-cols-2 gap-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">案件编号 *</label>
            <input type="text" id="case-number"
                   class="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                   placeholder="例如: 案件编号-2024-001">
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">调查机构 *</label>
            <input type="text" id="agency"
                   class="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                   placeholder="例如: XX市公安局">
        </div>
        <!-- ... more fields -->
    </div>

    <div class="flex justify-end mt-4">
        <button onclick="navigateToStep(2)" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            下一步 →
        </button>
    </div>
</div>
```

**Navigation function pattern** (lines 209-232):
```javascript
// Navigate between steps (per D-19)
function navigateToStep(step) {
    currentStep = step;

    // Hide all sections
    document.getElementById('step1-section').classList.add('hidden');
    document.getElementById('step2-section').classList.add('hidden');
    document.getElementById('step3-section').classList.add('hidden');

    // Show current step
    document.getElementById(`step${step}-section`).classList.remove('hidden');

    // Update indicators
    for (let i = 1; i <= 3; i++) {
        const indicator = document.getElementById(`step${i}-indicator`);
        if (i <= step) {
            indicator.classList.remove('bg-gray-300', 'text-gray-600');
            indicator.classList.add('bg-blue-600', 'text-white');
        } else {
            indicator.classList.remove('bg-blue-600', 'text-white');
            indicator.classList.add('bg-gray-300', 'text-gray-600');
        }
    }
}
```

**Import from other tool pattern** (lines 234-270):
```javascript
// Import from cluster (per D-20)
function importFromCluster() {
    const cached = sessionStorage.getItem('cit_cluster_export');
    if (!cached) {
        showError('未找到聚类结果，请先在地址聚类工具进行分析并点击"导出到跨境协查"');
        return;
    }

    try {
        const clusterResult = JSON.parse(cached);

        // Extract addresses from clusters
        addresses = [];
        chainTypes = [];

        if (clusterResult.clusters) {
            for (const cluster of clusterResult.clusters) {
                addresses.push(...cluster.addresses);
                chainTypes.push(...cluster.chain_types);
            }
        }

        // Add unassociated addresses
        if (clusterResult.unassociated) {
            for (const addr of clusterResult.unassociated) {
                addresses.push(addr);
                chainTypes.push('unknown');
            }
        }

        // Display address list
        updateAddressListDisplay();

    } catch (error) {
        showError('解析聚类结果失败: ' + error.message);
    }
}
```

**Template display pattern** (lines 187-199):
```html
<!-- Template display (per D-13) -->
<div id="template-display" class="hidden bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-semibold text-gray-800 mb-4">协查模板</h2>
    <div id="template-content" class="bg-gray-50 rounded p-6 whitespace-pre-wrap font-mono text-sm"></div>

    <!-- Copy button (per D-13) -->
    <div class="mt-4">
        <button onclick="copyTemplate()" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition">
            复制到剪贴板
        </button>
        <span id="copy-success" class="hidden text-green-600 ml-2">已复制!</span>
    </div>
</div>
```

**Copy to clipboard pattern** (lines 342-358):
```javascript
// Copy to clipboard (per D-13)
async function copyTemplate() {
    if (!templatePlainText) {
        showError('请先生成模板');
        return;
    }

    try {
        await navigator.clipboard.writeText(templatePlainText);
        document.getElementById('copy-success').classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('copy-success').classList.add('hidden');
        }, 2000);
    } catch (error) {
        showError('复制失败: ' + error.message);
    }
}
```

---

## Shared Patterns

### Flask Blueprint Registration
**Source:** `modules/cross/routes.py` lines 9-10
**Apply to:** All new modules must register Blueprint in `app.py`
```python
# Create Blueprint for case handling tools
case_bp = Blueprint('case', __name__, url_prefix='/case')

# In app.py, register:
from modules.case.routes import case_bp
app.register_blueprint(case_bp)
```

### JSON/CSV Export
**Source:** `modules/core/exporter.py`
**Apply to:** Monitor and Obfuscation export routes
```python
from modules.core.exporter import export_json

json_content = export_json(result)
response = Response(
    json_content,
    mimetype='application/json',
    headers={'Content-Disposition': f'attachment; filename="{filename}"'}
)
return response
```

### sessionStorage Tool Interconnection
**Source:** `templates/cross/cluster.html` lines 266-276
**Apply to:** All tool export/import buttons
```javascript
// Export button stores result in sessionStorage
sessionStorage.setItem('cit_monitor_export', cached);
window.location.href = '/case/asset-freeze';

// Target page imports on load
window.onload = function() {
    const cached = sessionStorage.getItem('cit_monitor_export');
    if (cached) {
        importFromMonitor();
    }
};
```

### Confidence Scoring
**Source:** `modules/trace/mixer_tracker.py` lines 128-152
**Apply to:** `modules/case/obfuscation_detector.py` attack detection results
```python
# Use HIGH/MEDIUM/LOW confidence levels
# Sort by confidence (HIGH first)
results.sort(key=lambda x: (
    0 if x['confidence'] == 'HIGH' else
    1 if x['confidence'] == 'MEDIUM' else 2
))
```

---

## No Analog Found

None - All files have exact or role-match analogs in the codebase.

---

## Metadata

**Analog search scope:** `modules/cross/`, `modules/trace/`, `modules/core/`, `templates/cross/`
**Files scanned:** 6 analog files
**Pattern extraction date:** 2026-04-24

---

## PATTERN MAPPING COMPLETE

**Phase:** 05 - Case Handling Tools
**Files classified:** 8
**Analogs found:** 8 / 8

### Coverage
- Files with exact analog: 8
- Files with role-match analog: 0
- Files with no analog: 0

### Key Patterns Identified
- Flask Blueprint modular architecture - each tool module registers its own Blueprint
- Multi-address input validation - max 10 addresses, chain detection, ETH key requirement
- Card-based result display - each result rendered as styled card with key stats
- Confidence scoring (HIGH/MEDIUM/LOW) - attack detection uses mixer_tracker confidence pattern
- Step-by-step form navigation - 3-step form with indicator updates
- sessionStorage tool interconnection - export/import between tools via sessionStorage
- JSON/CSV export via POST - cached result sent to export endpoint for file download
- Plain text template generation - formatted text for clipboard copy

### File Created
`J:\虚拟币犯罪调查工具集\docs\superpowers\.planning\phases\05-case-handling\05-PATTERNS.md`

### Ready for Planning
Pattern mapping complete. Planner can now reference analog patterns in PLAN.md files.