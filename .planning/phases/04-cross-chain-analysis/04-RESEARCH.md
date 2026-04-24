# Phase 4: Cross-Chain Analysis Tools - Research

**Researched:** 2026-04-24
**Domain:** Cryptocurrency address clustering and cross-border investigation coordination
**Confidence:** HIGH (established patterns from existing codebase, standard forensics techniques)

## Summary

Phase 4 implements two tools for advanced cryptocurrency investigation: address clustering (multi-address association analysis) and cross-border coordination (international cooperation template generation). Both tools integrate TRON, ETH, and BTC blockchain data through existing API clients, following established Flask Blueprint patterns from previous phases.

**Primary recommendation:** Build cluster_analyzer.py and cross_border_generator.py modules using existing api_client.py, eth_rpc_client.py, and btc_analyzer.py patterns. Template generation uses Jinja2 with pre-defined field structure. Results integrate via "export to cross-border" button.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 输入方式为文本域（多行输入框），每行一个地址，最多10个地址
- **D-02:** 支持TRON + ETH + BTC三链地址聚类
- **D-03:** ETH/BTC分析需要用户输入API密钥（每次查询输入，不存储）
- **D-04:** 提供样本填充按钮，帮助初学者理解输入格式
- **D-05:** 聚类依据1：首次资金来源相同（追踪所有地址的首次入账来源）
- **D-06:** 聚类依据2：频繁互转账（检查地址之间的直接转账频率）
- **D-07:** 聚类依据3：时间窗口关联（分析地址活动时间重叠度）
- **D-08:** 聚类依据4：共享存款地址（识别是否使用相同的存款地址）
- **D-09:** 结果采用分组卡片（Cluster Cards）形式，每组显示地址列表和关联原因
- **D-10:** 每个聚类显示：关联类型和原因、交易统计、时间窗口信息、共享地址信息
- **D-11:** 未找到关联的地址单独显示，注明"无关联"
- **D-12:** 支持JSON/CSV导出聚类结果
- **D-13:** 模板格式为HTML页面 + 文本导出（浏览器直接显示，用户可复制）
- **D-14:** 模板字段包含：案件基本信息、涉案地址与交易信息、调查背景说明、协查请求内容
- **D-15:** 案件基本信息：案件编号、调查机构、联系人、联系方式
- **D-16:** 涉案地址与交易信息：涉案地址列表、链类型、金额汇总、交易哈希
- **D-17:** 调查背景说明：可疑行为描述、资金流向简述、调查背景
- **D-18:** 协查请求内容：请求类型（信息查询、资产冻结等）、期望回复时间
- **D-19:** 输入流程为分步表单（案件信息 → 地址选择 → 模板生成）
- **D-20:** 支持从地址聚类结果导入地址列表（"导出到跨境协查"按钮）
- **D-21:** 使用标准模板（单一格式），不提供多辖区模板

### Claude's Discretion
- TRON/ETH/BTC API调用具体实现细节
- 聚类阈值设定（频繁互转账次数阈值、时间窗口重叠度阈值）
- 错误处理和重试逻辑
- Loading状态展示细节
- HTML模板具体样式设计

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CROSS-01 | User can cluster multiple addresses for association analysis | cluster_analyzer.py with 4 clustering heuristics (D-05 to D-08), existing api_client.py/eth_rpc_client.py/btc_analyzer.py patterns |
| CROSS-02 | User can generate cross-border investigation coordination templates | cross_border_generator.py with Jinja2 template, step-by-step form (D-19), import from clustering (D-20) |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Multi-address input validation | Backend (Flask) | — | Address format validation requires chain-type detection logic |
| Blockchain data fetching | Backend (Python modules) | — | API calls to Tronscan/Etherscan/Blockstream are backend operations |
| Clustering algorithm execution | Backend (Python) | — | Four heuristics (D-05 to D-08) require transaction data analysis |
| Cluster result rendering | Frontend (HTML/JS) | — | Cluster cards display follows established template patterns |
| Template field input | Frontend (HTML form) | Backend (validation) | Step-by-step form is UI, backend validates and processes |
| Template generation | Backend (Jinja2) | — | Template assembly from structured fields is server-side |
| Export functionality | Backend (Python) | Frontend (download trigger) | JSON/CSV generation via exporter.py, download via browser |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | 3.0+ | Web framework | Established in Phase 1-3, Blueprint pattern proven |
| requests | 2.31+ | HTTP client | Used in api_client.py, eth_rpc_client.py, btc_analyzer.py |
| Jinja2 | 3.1+ | Template engine | Flask built-in, used for cross-border template generation |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| web3.py | 7.15.0 | ETH RPC client | ETH address analysis (existing pattern) |
| csv (stdlib) | — | CSV export | Cluster result export |
| json (stdlib) | — | JSON export | Cluster result export |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom clustering library | NetworkX | NetworkX adds dependency for simple 4-heuristic clustering — hand-rolled sufficient per discretion |
| Template PDF generation | WeasyPrint | WeasyPrint adds complexity — text copy meets requirement (D-13) |

**Installation:** No new packages required — all dependencies already installed from Phase 1-3.

**Version verification:**
```
Flask: Established in app.py
requests: Used in modules/core/api_client.py
web3.py: Used in modules/core/eth_rpc_client.py
```

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Address Clustering Tool                          │
├─────────────────────────────────────────────────────────────────────────┤
│  Input Flow:                                                             │
│  [textarea: 10 addresses] → [detect chain type per address]             │
│      ↓                                                                   │
│  [ETH/BTC API key inputs] → [sample fill button]                         │
│      ↓                                                                   │
│  [Analyze button] → POST /cross/api/cluster/query                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Backend Processing (cluster_analyzer.py):                               │
│  [fetch transactions per address]                                        │
│      ↓                                                                   │
│  [apply 4 clustering heuristics]                                         │
│      ↓                                                                   │
│  [group addresses into clusters]                                         │
│      ↓                                                                   │
│  [return cluster result dict]                                            │
├─────────────────────────────────────────────────────────────────────────┤
│  Output:                                                                 │
│  [Cluster Cards: group + reason + stats]                                 │
│  [Unassociated addresses: "无关联"]                                       │
│  [Export buttons: JSON/CSV + "导出到跨境协查"]                            │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      Cross-Border Coordination Tool                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Input Flow (Step-by-step form):                                         │
│  Step 1: [Case info: 编号, 机构, 联系人, 联系方式]                        │
│      ↓                                                                   │
│  Step 2: [Address selection: import from cluster OR manual input]        │
│      ↓                                                                   │
│  Step 3: [Background: 可疑行为, 资金流向, 调查背景]                       │
│      ↓                                                                   │
│  [Request: 请求类型, 期望回复时间]                                        │
│      ↓                                                                   │
│  [Generate template button] → POST /cross/api/cross-border/generate      │
├─────────────────────────────────────────────────────────────────────────┤
│  Backend Processing (cross_border_generator.py):                         │
│  [validate form fields]                                                  │
│      ↓                                                                   │
│  [assemble template data dict]                                           │
│      ↓                                                                   │
│  [render Jinja2 template to HTML]                                        │
│      ↓                                                                   │
│  [return rendered template + plain text version]                         │
├─────────────────────────────────────────────────────────────────────────┤
│  Output:                                                                 │
│  [HTML template display: structured layout]                              │
│  [Copy button: plain text for clipboard]                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure
```
modules/
├── core/              # Existing shared modules (api_client.py, eth_rpc_client.py, exporter.py)
├── cross/             # NEW: Cross-chain analysis module
│   ├── routes.py      # Flask Blueprint routes (cluster + cross-border endpoints)
│   ├── cluster_analyzer.py    # Address clustering logic (4 heuristics)
│   ├── cross_border_generator.py  # Template generation logic
│   └── chain_detector.py      # Address chain type detection (TRON/ETH/BTC)
templates/
├── cross/             # NEW: Cross-chain tool pages
│   ├── cluster.html   # Address clustering UI (input + cards + export)
│   └── cross_border.html  # Cross-border form UI (3-step form + template display)
```

### Pattern 1: Address Clustering Algorithm
**What:** Group addresses based on four forensic heuristics (D-05 to D-08)
**When to use:** When user inputs multiple addresses for association analysis
**Example:**
```python
# Source: Established cryptocurrency forensics methodology [ASSUMED]

def cluster_addresses(addresses: list, api_keys: dict) -> dict:
    """
    Apply four clustering heuristics to group addresses.

    Returns:
        {
            'success': True,
            'clusters': [
                {
                    'cluster_id': 1,
                    'addresses': ['Txxx...', '0x123...'],
                    'reasons': ['首次资金来源相同: Tabc123...', '频繁互转账: 3次'],
                    'shared_source': 'Tabc123...',
                    'mutual_transfers': [{'from': 'Txxx', 'to': '0x123', 'count': 3}],
                    'time_window': {'overlap_pct': 85},
                    'shared_deposit': 'Tdeposit123...'
                }
            ],
            'unassociated': ['Tzzz...']
        }
    """
    # Step 1: Detect chain type per address
    address_data = {}
    for addr in addresses:
        chain = detect_chain_type(addr)  # 'tron', 'eth', 'btc'
        address_data[addr] = {
            'chain': chain,
            'transactions': fetch_transactions(addr, chain, api_keys),
            'first_incoming': find_first_funding_source(addr, chain),
            'activity_window': calculate_activity_window(addr)
        }

    # Step 2: Apply heuristics
    clusters = []
    checked = set()

    for addr1 in addresses:
        if addr1 in checked:
            continue

        cluster_addresses = [addr1]
        cluster_reasons = []

        for addr2 in addresses:
            if addr2 == addr1 or addr2 in checked:
                continue

            # D-05: First funding source match
            if address_data[addr1]['first_incoming'] == address_data[addr2]['first_incoming']:
                cluster_addresses.append(addr2)
                cluster_reasons.append(f"首次资金来源相同: {address_data[addr1]['first_incoming']}")

            # D-06: Frequent mutual transfers (threshold: 2+ transfers)
            mutual = check_mutual_transfers(addr1, addr2, address_data)
            if len(mutual) >= 2:
                cluster_addresses.append(addr2)
                cluster_reasons.append(f"频繁互转账: {len(mutual)}次")

            # D-07: Time window overlap (threshold: 70%+ overlap)
            overlap = calculate_time_overlap(
                address_data[addr1]['activity_window'],
                address_data[addr2]['activity_window']
            )
            if overlap >= 70:
                cluster_addresses.append(addr2)
                cluster_reasons.append(f"时间窗口关联: {overlap}%重叠")

            # D-08: Shared deposit address
            shared_deposit = find_shared_deposit(addr1, addr2, address_data)
            if shared_deposit:
                cluster_addresses.append(addr2)
                cluster_reasons.append(f"共享存款地址: {shared_deposit}")

        if len(cluster_addresses) > 1:
            clusters.append({
                'cluster_id': len(clusters) + 1,
                'addresses': cluster_addresses,
                'reasons': cluster_reasons,
                # ... additional fields per D-10
            })
            checked.update(cluster_addresses)

    unassociated = [a for a in addresses if a not in checked]

    return {'success': True, 'clusters': clusters, 'unassociated': unassociated}
```

### Pattern 2: Chain Type Detection
**What:** Identify blockchain type from address format
**When to use:** Before fetching transaction data for multi-chain clustering
**Example:**
```python
# Source: Established address format patterns [VERIFIED: existing btc_analyzer.py]

import re

def detect_chain_type(address: str) -> str:
    """
    Detect blockchain type from address format.

    Returns: 'tron', 'eth', 'btc', or 'unknown'
    """
    # TRON: Starts with 'T', 34 chars
    if re.match(r'^T[A-Za-z1-9]{33}$', address):
        return 'tron'

    # ETH: Starts with '0x', 40 hex chars
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return 'eth'

    # BTC: Legacy (1...), P2SH (3...), Native SegWit (bc1q...), Taproot (bc1p...)
    if re.match(r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return 'btc'
    if re.match(r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return 'btc'
    if re.match(r'^bc1q[ac-hj-np-z02-9]{39,59}$', address.lower()):
        return 'btc'
    if re.match(r'^bc1p[ac-hj-np-z02-9]{58}$', address.lower()):
        return 'btc'

    return 'unknown'
```

### Pattern 3: Cross-Border Template Structure
**What:** Standard template field structure per D-14 to D-18
**When to use:** Template generation for international coordination requests
**Example:**
```python
# Source: FATF guidance on virtual asset service provider cooperation [ASSUMED]

TEMPLATE_STRUCTURE = {
    'case_info': {
        'case_number': str,      # 案件编号 (D-15)
        'agency': str,           # 调查机构 (D-15)
        'contact_person': str,   # 联系人 (D-15)
        'contact_method': str    # 联系方式 (D-15)
    },
    'address_info': {
        'addresses': list,       # 涉案地址列表 (D-16)
        'chain_types': list,     # 链类型 (D-16)
        'total_amount': str,     # 金额汇总 (D-16)
        'tx_hashes': list        # 交易哈希 (D-16)
    },
    'background': {
        'suspicious_behavior': str,  # 可疑行为描述 (D-17)
        'fund_flow': str,            # 资金流向简述 (D-17)
        'investigation_context': str # 调查背景 (D-17)
    },
    'request': {
        'request_type': str,     # 请求类型 (D-18): "信息查询", "资产冻结"
        'expected_response': str # 期望回复时间 (D-18)
    }
}
```

### Anti-Patterns to Avoid
- **Mixing clustering logic with UI code:** Keep cluster_analyzer.py separate from routes.py — violates separation of concerns
- **Hardcoded API keys:** Never store keys — follow D-03 per-query input pattern
- **Complex clustering algorithms:** Use simple 4-heuristic approach — avoid over-engineering per discretion
- **PDF export for cross-border:** Text copy only per D-13 — DOCX/PDF out of scope

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Address transaction fetching | Custom HTTP client | modules/core/api_client.py, eth_rpc_client.py | Existing proven patterns, handles timeouts, retries |
| JSON/CSV export | Custom serialization | modules/core/exporter.py | export_json(), export_csv() already implemented |
| ETH/BTC address validation | Custom regex | btc_analyzer.py identify_address_type() | Established validation logic |
| HTML template rendering | String concatenation | Jinja2 templates | Flask built-in, proven in base.html pattern |

**Key insight:** Leverage existing Phase 1-3 code extensively — this phase is primarily about combining existing capabilities into new workflows (clustering + template generation).

## Common Pitfalls

### Pitfall 1: Cross-Chain API Key Management
**What goes wrong:** Mixing TRON (free) with ETH/BTC (requires keys) leads to confusing UI
**Why it happens:** TRON uses Tronscan (no key), ETH needs Etherscan key, BTC uses Blockstream (free)
**How to avoid:** Only show API key inputs when ETH/BTC addresses are detected in input
**Warning signs:** User confused about which key to enter, validation errors for missing keys

### Pitfall 2: Clustering Threshold Calibration
**What goes wrong:** Too strict thresholds yield no clusters, too loose yields everything clustered
**Why it happens:** Discretion allows threshold tuning, but wrong defaults frustrate users
**How to avoid:** Use reasonable defaults: mutual transfers >= 2, time overlap >= 70%
**Warning signs:** "无关联" for all addresses, or single giant cluster with weak reasons

### Pitfall 3: Template Field Validation Gaps
**What goes wrong:** Empty fields appear in generated template, making output unusable
**Why it happens:** Form validation not enforced before template generation
**How to avoid:** Validate all required fields (D-15 to D-18) before rendering template
**Warning signs:** Template shows "未知" or blank fields, user must manually edit

### Pitfall 4: Import Button Data Loss
**What goes wrong:** "导出到跨境协查" button doesn't pass cluster addresses correctly
**Why it happens:** sessionStorage or URL parameter encoding issues
**How to avoid:** Use sessionStorage.setItem('cit_cluster_export', JSON.stringify(cluster_result)) per existing pattern
**Warning signs:** Address list empty in cross-border form after import

## Code Examples

### Address Clustering Backend (cluster_analyzer.py)
```python
# Source: Pattern derived from existing api_client.py, btc_analyzer.py patterns

"""Address clustering module for multi-address association analysis"""

import logging
from typing import Dict, List, Any
from modules.core.api_client import get_account_info, get_trc20_transfers
from modules.core.api_client import get_eth_transactions, get_erc20_transfers
from modules.trace.btc_analyzer import fetch_transaction, identify_address_type

logger = logging.getLogger(__name__)

# Clustering thresholds (Claude's discretion)
MUTUAL_TRANSFER_THRESHOLD = 2  # D-06: minimum mutual transfers
TIME_OVERLAP_THRESHOLD = 70    # D-07: minimum overlap percentage

def detect_chain_type(address: str) -> str:
    """Detect blockchain type from address format."""
    import re
    # TRON: Starts with 'T', 34 chars
    if re.match(r'^T[A-Za-z1-9]{33}$', address):
        return 'tron'
    # ETH: Starts with '0x', 40 hex chars
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return 'eth'
    # BTC patterns (from btc_analyzer.py)
    if re.match(r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return 'btc'
    if re.match(r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return 'btc'
    if re.match(r'^bc1[qp][ac-hj-np-z02-9]{39,58}$', address.lower()):
        return 'btc'
    return 'unknown'

def cluster_addresses_web(addresses: List[str], api_keys: Dict[str, str]) -> Dict[str, Any]:
    """Web interface for address clustering.

    Args:
        addresses: List of wallet addresses (max 10 per D-01)
        api_keys: Dict with 'eth_key', 'btc_key' (optional for TRON)

    Returns:
        Dict with success, clusters, unassociated addresses
    """
    if len(addresses) > 10:
        return {'success': False, 'error': '地址数量超过10个限制'}

    # Detect chain types and validate
    address_chain_map = {}
    needs_eth_key = False
    needs_btc_key = False

    for addr in addresses:
        chain = detect_chain_type(addr)
        if chain == 'unknown':
            return {'success': False, 'error': f'无法识别地址链类型: {addr}'}
        address_chain_map[addr] = chain
        if chain == 'eth':
            needs_eth_key = True
        elif chain == 'btc':
            needs_btc_key = True

    # Validate API keys
    if needs_eth_key and not api_keys.get('eth_key'):
        return {'success': False, 'error': 'ETH地址需要Etherscan API密钥'}
    if needs_btc_key and not api_keys.get('btc_key'):
        return {'success': False, 'error': 'BTC地址需要Blockcypher API密钥'}

    # ... implementation continues with heuristic analysis
```

### Cross-Border Template Generator (cross_border_generator.py)
```python
# Source: Template generation pattern derived from Jinja2 best practices

"""Cross-border investigation coordination template generator"""

from typing import Dict, Any
from flask import render_template

REQUIRED_FIELDS = [
    'case_number', 'agency', 'contact_person', 'contact_method',
    'suspicious_behavior', 'request_type', 'expected_response'
]

def validate_template_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Validate template input fields.

    Returns:
        Dict with valid: bool, missing: list of missing required fields
    """
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
    return {'valid': len(missing) == 0, 'missing': missing}

def generate_template_web(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Generate cross-border coordination template.

    Args:
        fields: Dict with case_info, address_info, background, request

    Returns:
        Dict with success, html_content, plain_text
    """
    validation = validate_template_fields(fields)
    if not validation['valid']:
        return {
            'success': False,
            'error': f'缺少必填字段: {", ".join(validation["missing"])}'
        }

    # Render HTML template using Jinja2
    html_content = render_template('cross/template_display.html', **fields)

    # Generate plain text version for copy
    plain_text = generate_plain_text(fields)

    return {
        'success': True,
        'html_content': html_content,
        'plain_text': plain_text
    }

def generate_plain_text(fields: Dict[str, Any]) -> str:
    """Generate plain text version for clipboard copy."""
    template = """
跨境虚拟货币调查协查请求

案件编号: {case_number}
调查机构: {agency}
联系人: {contact_person}
联系方式: {contact_method}

涉案地址:
{address_list}

可疑行为描述: {suspicious_behavior}
资金流向简述: {fund_flow}

请求类型: {request_type}
期望回复时间: {expected_response}

---
本协查请求由虚拟币犯罪调查工具集生成，仅供合规调查使用。
"""
    return template.format(**fields)
```

### Flask Routes Pattern (routes.py)
```python
# Source: Pattern derived from modules/trace/routes.py

"""Flask Blueprint routes for cross-chain analysis tools"""

from flask import Blueprint, jsonify, request, render_template, Response
from modules.core.exporter import export_json
import datetime

cross_bp = Blueprint('cross', __name__, url_prefix='/cross')

# Sample data for clustering
SAMPLE_TRON_ADDRESS = "TUtP...NNw"
SAMPLE_ETH_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
SAMPLE_BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# ===================== Cluster Routes =====================

@cross_bp.route('/api/cluster/query', methods=['POST'])
def cluster_query():
    """API endpoint for address clustering.
    Request: {"addresses": ["..."], "eth_key": "...", "btc_key": "..."}
    Response: {"success": bool, "clusters": [...], "unassociated": [...]}
    """
    data = request.get_json()
    addresses = data.get('addresses', [])
    api_keys = {
        'eth_key': data.get('eth_key', ''),
        'btc_key': data.get('btc_key', '')
    }

    from .cluster_analyzer import cluster_addresses_web
    result = cluster_addresses_web(addresses, api_keys)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@cross_bp.route('/cluster')
def cluster_page():
    """Page route for address clustering tool."""
    return render_template('cross/cluster.html')

@cross_bp.route('/api/cluster/sample')
def cluster_sample():
    """Sample addresses for demo."""
    return jsonify({
        "sample_addresses": [
            SAMPLE_TRON_ADDRESS,
            SAMPLE_ETH_ADDRESS
        ]
    })

# ===================== Cross-Border Routes =====================

@cross_bp.route('/api/cross-border/generate', methods=['POST'])
def cross_border_generate():
    """API endpoint for template generation.
    Request: {"case_number": "...", "agency": "...", ...}
    Response: {"success": bool, "html_content": "...", "plain_text": "..."}
    """
    data = request.get_json()
    from .cross_border_generator import generate_template_web
    result = generate_template_web(data)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@cross_bp.route('/cross-border')
def cross_border_page():
    """Page route for cross-border coordination tool."""
    return render_template('cross/cross_border.html')
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single-address analysis only | Multi-address clustering | Phase 4 | Enables association detection across addresses |
| Manual template drafting | Template generator tool | Phase 4 | Reduces paperwork time, standardizes format |
| Per-chain separate tools | Integrated multi-chain clustering | Phase 4 | Single workflow for TRON/ETH/BTC |

**Deprecated/outdated:**
- Per-chain standalone analysis: Now integrated into clustering workflow

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | FATF template fields are appropriate for international coordination | Cross-Border Template Structure | Template may not match actual jurisdiction requirements |
| A2 | 70% time overlap threshold is reasonable for clustering | Clustering Threshold Calibration | May miss valid associations or create false positives |
| A3 | Blockstream API provides sufficient BTC address transaction history | BTC Address Analysis | May need fallback if Blockstream limits historical data |

**Recommendations for validation:**
- A1: User should confirm template fields match their jurisdiction's requirements
- A2: Tunable threshold per discretion — adjust based on user feedback
- A3: Verify Blockstream API coverage during implementation testing

## Open Questions (RESOLVED)

1. **BTC API Key Requirement** — RESOLVED: Use Blockstream free API (no key required)
   - Original question: Blockstream API is free but D-03 said BTC needs key
   - Resolution: D-03 updated to specify ETH needs key, BTC uses free Blockstream API
   - Decision: Aligns with btc_analyzer.py pattern, simpler for beginners

2. **Template Localization** — RESOLVED: Chinese only (standard template)
   - Original question: Should template support English for international requests?
   - Resolution: D-21 specifies standard template (单一格式), Chinese language confirmed
   - Decision: User can manually translate if needed for specific jurisdictions

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Flask | Web framework | ✓ | 3.0+ | — |
| requests | API calls | ✓ | 2.31+ | — |
| web3.py | ETH RPC | ✓ | 7.15.0 | — |
| Tronscan API | TRON data | ✓ | Free | — |
| Etherscan API V2 | ETH data | ✓ | Requires key | User-provided |
| Blockstream API | BTC data | ✓ | Free | Blockchain.info fallback |

**Missing dependencies with no fallback:**
- Etherscan API key: User must provide per-query (D-03)

**Missing dependencies with fallback:**
- Blockstream API: Falls back to Blockchain.info per btc_analyzer.py pattern

## Security Domain

> No security enforcement required for this phase (local-only tool, no data storage).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | Address format validation (regex per chain type) |
| V2 Authentication | no | Single-user local tool |
| V4 Access Control | no | No multi-user access |
| V6 Cryptography | no | No encryption requirements |

### Known Threat Patterns for Flask + External APIs

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| API key exposure in logs | Information Disclosure | Never log API keys, use per-query input |
| Invalid address injection | Tampering | Validate address format before API calls |
| API timeout cascades | Denial of Service | Timeout handling per api_client.py pattern |

## Sources

### Primary (HIGH confidence)
- Existing codebase patterns: modules/core/api_client.py, modules/core/eth_rpc_client.py, modules/trace/btc_analyzer.py, modules/core/exporter.py [VERIFIED: codebase]
- Flask Blueprint patterns: modules/trace/routes.py [VERIFIED: codebase]
- Template patterns: templates/base.html, templates/eth/transaction_query.html [VERIFIED: codebase]

### Secondary (MEDIUM confidence)
- Cryptocurrency forensics clustering heuristics [ASSUMED: training knowledge]
- FATF international cooperation guidance [ASSUMED: training knowledge]

### Tertiary (LOW confidence)
- Web search results returned empty — all domain knowledge based on training [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all components already established in Phase 1-3
- Architecture: HIGH — patterns proven in existing modules
- Pitfalls: MEDIUM — based on common error patterns in multi-API workflows

**Research date:** 2026-04-24
**Valid until:** 30 days (stable patterns, no new framework versions expected)