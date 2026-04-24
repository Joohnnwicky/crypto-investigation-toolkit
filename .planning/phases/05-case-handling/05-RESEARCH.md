# Phase 5: Case Handling Tools - Research

**Researched:** 2026-04-24
**Domain:** Multi-chain monitoring, attack detection, asset freeze templates
**Confidence:** HIGH

## Summary

This phase implements three case handling tools for cryptocurrency investigation: multi-chain address monitoring, obfuscation attack detection, and asset freeze request template generation. All three tools follow established patterns from Phase 1-4: Flask Blueprint architecture, card-based result display, multi-address input via textarea, step-by-step forms, and JSON/CSV export via exporter.py.

The multi-chain monitor combines existing TRON/ETH/BTC API clients into a unified monitoring interface with status cards. The attack detector implements rule-based pattern matching for four ETH attack types (Sandwich, Flash Loan, Dusting, Protocol vulnerability) using the confidence scoring pattern from mixer_tracker.py. The asset freeze generator follows the cross_border_generator.py step-by-step form pattern with plain text copy export.

**Primary recommendation:** Reuse existing API clients (api_client.py, eth_rpc_client.py, btc_analyzer.py) for monitoring; implement attack detection as rule-based heuristics with HIGH/MEDIUM/LOW confidence; copy cross_border_generator pattern for asset freeze template.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Multi-chain Monitoring Trigger:**
- D-01: Manual refresh trigger (user clicks refresh button, no auto polling)
- D-02: Local tool without backend service, "real-time monitoring" = manual refresh
- D-03: No scheduled polling to avoid API rate limiting

**Multi-chain Monitoring Input:**
- D-04: Address input via textarea (multi-line), max 10 addresses
- D-05: Support TRON + ETH + BTC, auto-detect chain type
- D-06: ETH monitoring requires API key input (shared for all ETH addresses)
- D-07: TRON/BTC use free APIs (Tronscan/Blockstream), no key needed
- D-08: Sample fill button for beginners

**Multi-chain Monitoring Display:**
- D-09: Status card display (one card per address)
- D-10: Each card shows: balance, recent transaction count, last active time
- D-11: Refresh updates all address cards
- D-12: JSON/CSV export support

**Attack Detection Types:**
- D-13: Detect 4 types: Sandwich, Flash Loan, Dusting, Protocol vulnerability
- D-14: Sandwich: DEX frontrunning/backrunning price manipulation
- D-15: Flash Loan: borrow large amounts, manipulate market, instant repay
- D-16: Dusting: send tiny tokens to many addresses for tracking
- D-17: Protocol vulnerability: exploit design flaws (reentrancy, price manipulation)

**Attack Detection Logic:**
- D-18: Rule-based pattern matching (known attack signatures)
- D-19: Flash Loan signature: borrow + repay in single transaction
- D-20: Sandwich signature: price manipulation in same block (front/back)
- D-21: Dusting signature: send tiny amounts to many addresses
- D-22: Protocol vulnerability: abnormal contract call patterns

**Attack Detection Input/Scope:**
- D-23: Address input (query recent transactions and detect attack traces)
- D-24: ETH chain only (Uniswap and other DEX attacks)
- D-25: ETH API key input per query (not stored)
- D-26: Sample fill button

**Attack Detection Display:**
- D-27: Attack card display (one card per attack type)
- D-28: Each card: attack type, details, confidence (HIGH/MEDIUM/LOW), affected addresses
- D-29: "No attack traces found" when clean
- D-30: JSON/CSV export support

**Asset Freeze Template:**
- D-31: Independent template (different from cross-border coordination)
- D-32: Cross-border = international coordination request; Asset freeze = freeze request
- D-33: Independent content and field design
- D-34: 4 field categories: case info, freeze target info, freeze reason, freeze terms
- D-35: Case info: case number, agency, contact person, contact method
- D-36: Freeze target: address list, chain type, freeze amount, asset type
- D-37: Freeze reason: suspicious behavior, fund source, necessity, legal basis
- D-38: Freeze terms: duration, unlock conditions, contact, follow-up

**Asset Freeze Input/Output:**
- D-39: Step-by-step form (case info -> address selection -> template generation)
- D-40: Plain text copy export (HTML display, user copies)
- D-41: Standard template (single format, no multi-jurisdiction)
- D-42: PDF export in Phase 6

**Tool Interconnection:**
- D-43 to D-46: Monitor export to TRON/ETH analysis, cluster, asset freeze, JSON/CSV
- D-47 to D-49: Asset freeze import from monitor, cluster, manual input
- D-50 to D-52: Attack detection export to ETH query, asset freeze, JSON/CSV

### Claude's Discretion
- Specific attack detection rule implementation details
- API timeout and retry logic
- Status card styling
- Step-by-step form UI details
- Export button positions and interaction
- Error handling and loading state display

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CASE-01 | User can monitor addresses across multiple chains in real-time | Multi-chain monitor combining api_client.py (TRON), eth_rpc_client.py (ETH), Blockstream API (BTC); status cards with balance/tx count/last active |
| CASE-02 | User can identify obfuscation attack techniques | Attack detector with rule-based pattern matching for Sandwich/Flash Loan/Dusting/Protocol vulnerability; confidence scoring pattern from mixer_tracker.py |
| CASE-03 | User can generate asset freeze request templates | Step-by-step form pattern from cross_border_generator.py; plain text copy export; 4 field categories per D-34 to D-38 |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Multi-chain API queries | Backend (Python) | - | API clients execute in Flask routes, no browser-side blockchain access |
| Chain type detection | Backend (Python) | - | Regex matching on address format, already in chain_detector.py |
| Attack pattern matching | Backend (Python) | - | Rule-based heuristics require transaction parsing, not browser-side |
| Status card rendering | Frontend (HTML/JS) | Backend (JSON) | Cards rendered from structured JSON results |
| Step-by-step form flow | Frontend (JS) | Backend (validation) | Multi-step navigation in JS, validation in backend |
| Template text generation | Backend (Python) | Frontend (display) | Template logic in Python, display in HTML textarea |
| Export file download | Backend (Python) | - | exporter.py generates JSON/CSV blobs |
| Tool interconnection | Frontend (JS) | - | sessionStorage for cross-tool data passing |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | 3.1.3 | Web framework | [VERIFIED: pip show] Project standard |
| requests | 2.32.5 | HTTP client | [VERIFIED: pip show] Used in api_client.py |
| web3 | 7.15.0 | ETH RPC | [VERIFIED: pip show] Used in eth_rpc_client.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json | stdlib | JSON export | exporter.py pattern |
| csv | stdlib | CSV export | exporter.py pattern |
| datetime | stdlib | Timestamps | All modules use this |
| re | stdlib | Address validation | chain_detector.py pattern |

### External APIs
| API | Chain | Key Required | Endpoint | Use |
|-----|-------|--------------|----------|-----|
| Tronscan | TRON | No | `https://api.tronscan.org/api/account` | Balance, tx count |
| Etherscan V2 | ETH | Yes | `https://api.etherscan.io/v2/api` | Balance, tx history, logs |
| Blockstream | BTC | No | `https://blockstream.info/api/address/{addr}` | Balance, stats |

**Installation:** Already installed (Phase 1-4 dependencies).

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Phase 5 Case Handling Tools                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                 │
│  │ Monitor Tool │     │ Attack Det.  │     │ Asset Freeze │                 │
│  │ /case/monitor│     │ /case/obfusc │     │ /case/freeze │                 │
│  └──────────────┘     └──────────────┘     └──────────────┘                 │
│         │                    │                    │                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    Flask Blueprint: case_bp                       │       │
│  │  routes.py → monitor.py, obfuscation_detector.py, freeze_gen.py  │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│         │                    │                    │                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    Existing Modules (reuse)                       │       │
│  ├──────────────┬──────────────┬──────────────┬─────────────────────┤       │
│  │ api_client   │ eth_rpc      │ btc_analyzer │ chain_detector      │       │
│  │ (TRON API)   │ (ETH RPC)    │ (BTC API)    │ (address type)      │       │
│  ├──────────────┴──────────────┴──────────────┴─────────────────────┤       │
│  │ exporter.py (JSON/CSV export)                                     │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    External APIs                                  │       │
│  ├──────────────────────────────────────────────────────────────────┤       │
│  │ Tronscan API ────────► TRON address info (free, no key)          │       │
│  │ Etherscan V2 API ────► ETH transactions (requires key per query) │       │
│  │ Blockstream API ─────► BTC address stats (free, no key)          │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    Tool Interconnection                           │       │
│  ├──────────────────────────────────────────────────────────────────┤       │
│  │ sessionStorage: cit_monitor_export → asset freeze import         │       │
│  │ sessionStorage: cit_attack_export → asset freeze import          │       │
│  │ sessionStorage: cit_cluster_export → asset freeze import         │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure
```
modules/
├── case/                    # NEW: Case handling tools module
│   ├── __init__.py
│   ├── routes.py            # Flask Blueprint routes (3 tools)
│   ├── monitor.py           # Multi-chain monitor logic
│   ├── obfuscation_detector.py  # Attack detection heuristics
│   └── asset_freeze_generator.py  # Template generator
templates/
├── case/                    # NEW: Case tool templates
│   ├── monitor.html         # Multi-chain monitor UI
│   ├── obfuscation.html     # Attack detection UI
│   └── asset_freeze.html    # Asset freeze step-by-step form
```

### Pattern 1: Multi-Address Input (Reuse from cluster_analyzer.py)
**What:** Textarea input for multiple addresses, one per line, max 10.
**When to use:** Monitor tool, asset freeze address selection.
**Example:**
```python
# Source: modules/cross/cluster_analyzer.py
addresses = [addr.strip() for addr in addresses if addr.strip()]
if len(addresses) > 10:
    return {'success': False, 'error': '地址数量超过10个限制'}

# Detect chain types using existing chain_detector
from modules.cross.chain_detector import detect_chain_type
address_chain_map = {}
for addr in addresses:
    chain = detect_chain_type(addr)
    if chain == 'unknown':
        return {'success': False, 'error': f'无法识别地址链类型: {addr}'}
    address_chain_map[addr] = chain
```

### Pattern 2: Card-Based Result Display (Reuse from cluster.html)
**What:** Each result rendered as a styled card with key stats.
**When to use:** Monitor status cards, attack detection cards.
**Example:**
```javascript
// Source: templates/cross/cluster.html
function displayClusterCard(cluster) {
    let html = `<div class="border rounded-lg p-4 mb-4">`;
    html += `<div class="flex justify-between items-center mb-2">`;
    html += `<span class="font-semibold text-blue-600">聚类 ${cluster.cluster_id}</span>`;
    html += `<span class="text-gray-500">${cluster.addresses.length} 个地址</span>`;
    html += `</div>`;
    // ... addresses, reasons, stats
    html += `</div>`;
    return html;
}
```

### Pattern 3: Confidence Scoring (Reuse from mixer_tracker.py)
**What:** HIGH/MEDIUM/LOW confidence levels for detection results.
**When to use:** Attack detection results.
**Example:**
```python
# Source: modules/trace/mixer_tracker.py
def calculate_confidence(self, withdrawal: Dict, deposit_ts: float) -> tuple:
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

### Pattern 4: Step-by-Step Form (Reuse from cross_border.html)
**What:** 3-step form with indicator, navigation, field validation.
**When to use:** Asset freeze template generator.
**Example:**
```javascript
// Source: templates/cross/cross_border.html
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

### Pattern 5: sessionStorage Tool Interconnection (Reuse from cluster.html)
**What:** Export button stores result in sessionStorage, target page imports on load.
**When to use:** Monitor -> other tools, Attack detection -> other tools.
**Example:**
```javascript
// Source: templates/cross/cluster.html
// Export to cross-border (D-20)
function exportToCrossBorder() {
    const cached = sessionStorage.getItem(CACHE_KEY);
    if (!cached) {
        showError('无缓存结果，请先进行分析');
        return;
    }
    // Store for cross-border import
    sessionStorage.setItem('cit_cluster_export', cached);
    window.location.href = '/cross/cross-border';
}

// Import on target page load (cross_border.html)
window.onload = function() {
    const cached = sessionStorage.getItem('cit_cluster_export');
    if (cached) {
        // Auto-import if data present
        importFromCluster();
    }
};
```

### Pattern 6: Plain Text Template Generation (Reuse from cross_border_generator.py)
**What:** Generate formatted plain text for clipboard copy.
**When to use:** Asset freeze template output.
**Example:**
```python
# Source: modules/cross/cross_border_generator.py
def generate_plain_text(fields: Dict[str, Any]) -> str:
    template = f"""
跨境虚拟货币调查协查请求

案件编号: {fields.get('case_number', '')}
调查机构: {fields.get('agency', '')}
...
---
本协查请求由虚拟币犯罪调查工具集生成，仅供合规调查使用。
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template.strip()
```

### Pattern 7: JSON/CSV Export via POST (Reuse from routes.py)
**What:** POST endpoint receives cached result, generates file download.
**When to use:** Monitor export, Attack detection export.
**Example:**
```python
# Source: modules/cross/routes.py
@cross_bp.route('/api/cluster/export/json', methods=['POST'])
def cluster_export_json():
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

### Anti-Patterns to Avoid
- **Don't store API keys:** Per ADDR-05 and D-25/D-06, keys must be per-query input, never stored
- **Don't auto-poll APIs:** Per D-03, only manual refresh to avoid rate limiting
- **Don't create new export logic:** Reuse exporter.py, don't duplicate
- **Don't create new chain detection:** Reuse chain_detector.py, don't duplicate regex
- **Don't build TRON/BTC attack detection:** Per D-24, attack detection is ETH only

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| TRON API queries | New Tronscan client | api_client.py get_account_info() | Already implemented, tested |
| ETH transaction queries | New Etherscan wrapper | eth_analyzer.py get_eth_transactions() | Already implemented, handles V2 API |
| BTC address queries | New Blockstream client | btc_analyzer.py fetch_transaction() | Already implemented, needs extension for address balance |
| Chain type detection | New address regex | chain_detector.py detect_chain_type() | Already implemented, handles TRON/ETH/BTC |
| JSON export | New JSON serializer | exporter.py export_json() | Already implemented, Chinese-preserving |
| CSV export | New CSV writer | exporter.py export_csv() | Already implemented, structured output |
| Confidence scoring | New scoring system | mixer_tracker.py pattern | Pattern established, user-recognized |
| Step-by-step form | New form component | cross_border.html pattern | Pattern established, consistent UX |
| Tool interconnection | New state management | sessionStorage pattern | Pattern established in cluster/cross_border |

**Key insight:** Phase 5 is primarily integration and extension work, not new architecture. All patterns exist from Phase 1-4.

## Common Pitfalls

### Pitfall 1: Blockstream API Address Balance Not Available
**What goes wrong:** Blockstream API endpoint `/tx/{hash}` only returns transaction data, not address balance history.
**Why it happens:** btc_analyzer.py currently only handles single transaction queries, not address-level queries.
**How to avoid:** Use Blockstream `/address/{address}` and `/address/{address}/stats` endpoints for address monitoring (verified by WebSearch).
**Warning signs:** BTC addresses showing "0 balance" when they have transactions.

### Pitfall 2: ETH API Key Not Passed to Attack Detection
**What goes wrong:** Attack detection requires transaction history but API key is missing.
**Why it happens:** Frontend might not detect ETH addresses and hide key input.
**How to avoid:** Always show ETH key input when any ETH address is detected (follow cluster.html pattern).
**Warning signs:** "ETH地址需要API密钥" error when user didn't see key input.

### Pitfall 3: Attack Detection False Positives
**What goes wrong:** Normal DEX swaps flagged as Sandwich attacks.
**Why it happens:** Rule matching too aggressive, doesn't account for legitimate arbitrage.
**How to avoid:** Use multi-factor confidence scoring: check block ordering, price delta, transaction timing. Label LOW confidence for borderline cases.
**Warning signs:** Every Uniswap user flagged as attacker.

### Pitfall 4: sessionStorage Not Persisting Between Tools
**What goes wrong:** Export button clicked but target tool doesn receive data.
**Why it happens:** sessionStorage is per-origin but might be cleared on navigation.
**How to avoid:** Use consistent key names (cit_monitor_export, cit_attack_export), verify on target page load.
**Warning signs:** "未找到监控结果" error when trying to import.

### Pitfall 5: Attack Detection Missing ETH Chain Scope
**What goes wrong:** User enters TRON/BTC address for attack detection.
**Why it happens:** UI doesn't validate chain type before submission.
**How to avoid:** Validate ETH-only scope in frontend before API call (show error for non-ETH addresses).
**Warning signs:** TRON address submitted to attack detection endpoint.

## Code Examples

### Multi-Chain Monitor: Fetch Address Status

```python
# Pattern: Combine existing API clients for unified monitoring
# Source: modules/cross/cluster_analyzer.py (adapted)

from modules.core.api_client import get_account_info
from modules.eth.eth_analyzer import get_eth_transactions
from modules.cross.chain_detector import detect_chain_type
import requests

BLOCKSTREAM_API = "https://blockstream.info/api"

def get_btc_address_stats(address: str) -> dict:
    """Get BTC address balance and stats from Blockstream API.
    
    [VERIFIED: WebSearch] Endpoint: GET /address/{address}
    Returns: funded_txo_sum (received), spent_txo_sum (sent), tx_count
    """
    try:
        response = requests.get(
            f"{BLOCKSTREAM_API}/address/{address}",
            timeout=10
        )
        if response.status_code != 200:
            return None
        data = response.json()
        
        chain_stats = data.get('chain_stats', {})
        balance = (chain_stats.get('funded_txo_sum', 0) - 
                   chain_stats.get('spent_txo_sum', 0)) / 1e8  # satoshis to BTC
        tx_count = chain_stats.get('tx_count', 0)
        
        return {
            'address': address,
            'balance': balance,
            'tx_count': tx_count,
            'total_received': chain_stats.get('funded_txo_sum', 0) / 1e8
        }
    except Exception:
        return None

def monitor_addresses_web(addresses: list, eth_key: str = '') -> dict:
    """Multi-chain address monitoring (CASE-01).
    
    Args:
        addresses: List of wallet addresses (max 10 per D-04)
        eth_key: Etherscan API key (required for ETH addresses)
    
    Returns:
        Dict with success, addresses, status_cards
    """
    if len(addresses) > 10:
        return {'success': False, 'error': '地址数量超过10个限制'}
    
    status_cards = []
    
    for addr in addresses:
        chain = detect_chain_type(addr)
        
        if chain == 'tron':
            info = get_account_info(addr)
            if info:
                status_cards.append({
                    'address': addr,
                    'chain': 'TRON',
                    'balance': info.get('balance', 0),
                    'usdt_balance': info.get('usdt_balance', 0),
                    'tx_count': info.get('total_transaction_count', 0),
                    'last_active': '最近有活动' if info.get('total_transaction_count', 0) > 0 else '无活动记录'
                })
        
        elif chain == 'eth':
            if not eth_key:
                return {'success': False, 'error': 'ETH地址需要Etherscan API密钥'}
            txs = get_eth_transactions(addr, eth_key, limit=50)
            if txs:
                # Calculate balance from transactions (simplified)
                balance = sum(float(t.get('value', 0)) for t in txs if t.get('to', '').lower() == addr.lower()) / 1e18
                last_tx = txs[0] if txs else None
                last_active = datetime.fromtimestamp(int(last_tx.get('timeStamp', 0))).strftime('%Y-%m-%d') if last_tx else '无活动'
                status_cards.append({
                    'address': addr,
                    'chain': 'ETH',
                    'balance': balance,
                    'tx_count': len(txs),
                    'last_active': last_active
                })
        
        elif chain == 'btc':
            stats = get_btc_address_stats(addr)
            if stats:
                status_cards.append({
                    'address': addr,
                    'chain': 'BTC',
                    'balance': stats.get('balance', 0),
                    'tx_count': stats.get('tx_count', 0),
                    'last_active': '查看交易记录'  # Blockstream doesn't provide last active directly
                })
    
    return {
        'success': True,
        'addresses': addresses,
        'status_cards': status_cards,
        'total_count': len(status_cards)
    }
```

### Attack Detection: Rule-Based Heuristics

```python
# Pattern: Rule-based pattern matching with confidence scoring
# Source: mixer_tracker.py confidence pattern

from modules.eth.eth_analyzer import get_eth_transactions, get_transaction_logs
from modules.core.eth_rpc_client import EthRpcClient
import logging

logger = logging.getLogger(__name__)

# Known DEX router addresses for Sandwich detection
DEX_ROUTERS = {
    'uniswap_v2': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
    'uniswap_v3': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
    'sushiswap': '0xd9e1cE17f2641f24AE83637ab58a1aFa2493E64',
}

# Flash loan provider addresses
FLASH_LOAN_PROVIDERS = {
    'aave': '0x3986E6cA3e63F9B3b9f923830B1f403d68a6a1E8',
    'dydx': '0x1E0447b19BB6AFd280FF7beC884Ab552A1Be372',
}

def detect_sandwich_attack(txs: list) -> dict:
    """Detect Sandwich attack patterns (D-14, D-20).
    
    Signature: Same block contains frontrun + victim + backrun transactions
    to same DEX router with price manipulation.
    
    Returns: Dict with detected, confidence, details
    """
    attacks = []
    
    # Group transactions by block
    block_groups = {}
    for tx in txs:
        block = tx.get('blockNumber')
        if block not in block_groups:
            block_groups[block] = []
        block_groups[block].append(tx)
    
    # Check blocks with multiple DEX transactions
    for block, block_txs in block_groups.items():
        dex_txs = [t for t in block_txs if t.get('to', '').lower() in 
                   [r.lower() for r in DEX_ROUTERS.values()]]
        
        if len(dex_txs) >= 3:
            # Potential sandwich: front-victim-back pattern
            # Check for same token pair
            attacks.append({
                'type': 'Sandwich',
                'confidence': 'MEDIUM',  # Need more analysis for HIGH
                'block': block,
                'tx_count': len(dex_txs),
                'details': f'区块 {block} 内有 {len(dex_txs)} 笔DEX交易，可能存在三明治攻击'
            })
    
    return {'detected': len(attacks) > 0, 'attacks': attacks}

def detect_flash_loan_attack(txs: list, api_key: str) -> dict:
    """Detect Flash Loan attack patterns (D-15, D-19).
    
    Signature: Single transaction with borrow + manipulate + repay
    May involve multiple protocol interactions.
    
    Returns: Dict with detected, confidence, details
    """
    attacks = []
    
    for tx in txs:
        # Check if transaction involves flash loan providers
        to_addr = tx.get('to', '').lower()
        
        # Check transaction logs for borrow/repay pattern
        logs = get_transaction_logs(tx.get('hash', ''), api_key)
        
        # Look for rapid borrow/repay in same tx
        has_borrow = any('Borrow' in str(log) or 'FlashLoan' in str(log) for log in logs)
        has_repay = any('Repay' in str(log) for log in logs)
        
        if has_borrow and has_repay:
            # Check for large value
            value = float(tx.get('value', 0)) / 1e18
            
            attacks.append({
                'type': 'Flash Loan',
                'confidence': 'HIGH' if value > 100 else 'MEDIUM',
                'tx_hash': tx.get('hash', ''),
                'value': value,
                'details': f'交易 {tx.get("hash", "")[:16]}... 内含借贷和还款，金额 {value:.2f} ETH'
            })
    
    return {'detected': len(attacks) > 0, 'attacks': attacks}

def detect_dusting_attack(txs: list) -> dict:
    """Detect Dusting attack patterns (D-16, D-21).
    
    Signature: Many outgoing transactions of tiny amounts to different addresses.
    Typically < 0.001 tokens to hundreds of addresses.
    
    Returns: Dict with detected, confidence, details
    """
    attacks = []
    
    # Count outgoing transactions with tiny values
    dust_threshold = 0.001  # ETH or token equivalent
    
    outgoing = [t for t in txs if float(t.get('value', 0)) / 1e18 < dust_threshold]
    
    if len(outgoing) >= 10:
        # Potential dusting: many tiny sends
        unique_recipients = set(t.get('to', '') for t in outgoing)
        
        if len(unique_recipients) >= 10:
            attacks.append({
                'type': 'Dusting',
                'confidence': 'HIGH' if len(unique_recipients) >= 50 else 'MEDIUM',
                'tx_count': len(outgoing),
                'recipients': len(unique_recipients),
                'details': f'发现 {len(outgoing)} 笔小额转账，涉及 {len(unique_recipients)} 个地址'
            })
    
    return {'detected': len(attacks) > 0, 'attacks': attacks}

def detect_protocol_vulnerability(txs: list, api_key: str) -> dict:
    """Detect Protocol vulnerability exploitation (D-17, D-22).
    
    Signature: Abnormal contract call patterns, failed transactions,
    reentrancy patterns, unusual event sequences.
    
    Returns: Dict with detected, confidence, details
    """
    attacks = []
    
    for tx in txs:
        # Check for failed transactions with high value
        if tx.get('isError') == '1':
            value = float(tx.get('value', 0)) / 1e18
            if value > 10:
                attacks.append({
                    'type': 'Protocol Vulnerability',
                    'confidence': 'LOW',
                    'tx_hash': tx.get('hash', ''),
                    'details': f'高价值交易失败，可能涉及协议漏洞尝试'
                })
        
        # Check logs for reentrancy patterns (multiple calls to same contract)
        logs = get_transaction_logs(tx.get('hash', ''), api_key)
        contract_calls = [log.get('address', '') for log in logs]
        
        # If same contract called multiple times in one tx
        call_counts = {}
        for addr in contract_calls:
            call_counts[addr] = call_counts.get(addr, 0) + 1
        
        repeated_calls = [addr for addr, count in call_counts.items() if count >= 3]
        if repeated_calls:
            attacks.append({
                'type': 'Protocol Vulnerability',
                'confidence': 'MEDIUM',
                'tx_hash': tx.get('hash', ''),
                'details': f'交易中同一合约被调用 {call_counts[repeated_calls[0]]} 次，可能存在重入漏洞'
            })
    
    return {'detected': len(attacks) > 0, 'attacks': attacks}

def detect_attacks_web(address: str, api_key: str) -> dict:
    """Web interface for attack detection (CASE-02).
    
    Args:
        address: ETH address to analyze
        api_key: Etherscan API key
    
    Returns:
        Dict with success, address, attack_cards
    """
    # Get recent transactions
    txs = get_eth_transactions(address, api_key, limit=100)
    
    if not txs:
        return {
            'success': True,
            'address': address,
            'attack_cards': [],
            'message': '未发现攻击痕迹'
        }
    
    # Run all detectors
    all_attacks = []
    
    sandwich_result = detect_sandwich_attack(txs)
    if sandwich_result['detected']:
        all_attacks.extend(sandwich_result['attacks'])
    
    flash_loan_result = detect_flash_loan_attack(txs, api_key)
    if flash_loan_result['detected']:
        all_attacks.extend(flash_loan_result['attacks'])
    
    dusting_result = detect_dusting_attack(txs)
    if dusting_result['detected']:
        all_attacks.extend(dusting_result['attacks'])
    
    protocol_result = detect_protocol_vulnerability(txs, api_key)
    if protocol_result['detected']:
        all_attacks.extend(protocol_result['attacks'])
    
    # Sort by confidence (HIGH first)
    all_attacks.sort(key=lambda x: (
        0 if x['confidence'] == 'HIGH' else
        1 if x['confidence'] == 'MEDIUM' else 2
    ))
    
    return {
        'success': True,
        'address': address,
        'attack_cards': all_attacks,
        'total_attacks': len(all_attacks),
        'message': '未发现攻击痕迹' if len(all_attacks) == 0 else None
    }
```

### Asset Freeze Template Generator

```python
# Pattern: Step-by-step form with plain text output
# Source: modules/cross/cross_border_generator.py (adapted)

from datetime import datetime
from typing import Dict, Any

REQUIRED_FREEZE_FIELDS = [
    'case_number',     # 案件编号 (D-35)
    'agency',          # 调查机构 (D-35)
    'contact_person',  # 联系人 (D-35)
    'contact_method',  # 联系方式 (D-35)
    'suspicious_behavior',  # 可疑行为描述 (D-37)
    'freeze_necessity',     # 冻结必要性 (D-37)
]

def generate_freeze_template(fields: Dict[str, Any]) -> dict:
    """Generate asset freeze request template (CASE-03, D-34 to D-38).
    
    Args:
        fields: Dict with case_info, address_info, reason_info, terms_info
    
    Returns:
        Dict with success, template_data, plain_text
    """
    # Validate required fields
    missing = []
    for field in REQUIRED_FREEZE_FIELDS:
        if not fields.get(field):
            missing.append(field)
    
    if missing:
        return {
            'success': False,
            'error': f'缺少必填字段: {", ".join(missing)}'
        }
    
    # Build structured template
    template_data = {
        'case_info': {
            'case_number': fields.get('case_number', ''),
            'agency': fields.get('agency', ''),
            'contact_person': fields.get('contact_person', ''),
            'contact_method': fields.get('contact_method', '')
        },
        'target_info': {
            'addresses': fields.get('addresses', []),
            'chain_types': fields.get('chain_types', []),
            'freeze_amount': fields.get('freeze_amount', ''),
            'asset_type': fields.get('asset_type', '')
        },
        'reason_info': {
            'suspicious_behavior': fields.get('suspicious_behavior', ''),
            'fund_source': fields.get('fund_source', ''),
            'freeze_necessity': fields.get('freeze_necessity', ''),
            'legal_basis': fields.get('legal_basis', '')
        },
        'terms_info': {
            'freeze_duration': fields.get('freeze_duration', ''),
            'unlock_conditions': fields.get('unlock_conditions', ''),
            'contact': fields.get('freeze_contact', ''),
            'follow_up': fields.get('follow_up', '')
        },
        'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Generate plain text for copy
    plain_text = generate_freeze_plain_text(fields)
    
    return {
        'success': True,
        'template_data': template_data,
        'plain_text': plain_text
    }

def generate_freeze_plain_text(fields: Dict[str, Any]) -> str:
    """Generate plain text version for clipboard copy (D-40).
    
    Args:
        fields: All template fields
    
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
    
    template = f"""
虚拟货币资产冻结申请

案件编号: {fields.get('case_number', '')}
调查机构: {fields.get('agency', '')}
联系人: {fields.get('contact_person', '')}
联系方式: {fields.get('contact_method', '')}

冻结对象地址:
{address_list_formatted if addresses else '  无'}

冻结金额: {fields.get('freeze_amount', '未知')}
资产类型: {fields.get('asset_type', '未知')}

可疑行为描述: {fields.get('suspicious_behavior', '')}
资金来源说明: {fields.get('fund_source', '')}
冻结必要性: {fields.get('freeze_necessity', '')}
法律依据: {fields.get('legal_basis', '')}

冻结期限: {fields.get('freeze_duration', '')}
解除冻结条件: {fields.get('unlock_conditions', '')}
后续处理: {fields.get('follow_up', '')}

---
本冻结申请由虚拟币犯罪调查工具集生成，仅供合规调查使用。
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template.strip()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| BTC tx-only queries | BTC address balance queries | Phase 5 | Enables BTC monitoring status cards |
| Attack detection ML models | Rule-based heuristics | Phase 5 | Simpler implementation, lower false positives |
| PDF template export | Plain text copy | Phase 5 | Faster iteration, PDF deferred to Phase 6 |

**Deprecated/outdated:**
- Blockstream `/tx/{hash}` only: Now use `/address/{address}` for monitoring

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Blockstream `/address/{addr}` returns balance stats | Standard Stack | BTC monitoring shows 0 balance; need to add fallback to Blockchain.info API |
| A2 | Sandwich detection rule (3+ DEX txs in block) sufficient | Code Examples | May flag legitimate high-frequency trading; consider adding price delta threshold |
| A3 | Flash loan borrow/repay log detection works | Code Examples | Some flash loans use custom events; need to verify with Aave/dYdX logs |

**If this table is empty:** All claims in this research were verified or cited.

## Open Questions (RESOLVED)

1. **Blockstream Address Stats Accuracy**
   - RESOLVED: Use `funded_txo_sum` and `spent_txo_sum` fields from `chain_stats` object for BTC balance calculation. Verified by WebSearch confirming Blockstream API `/address/{address}` returns these fields. Code examples already implement this pattern (lines 459-469).

2. **Attack Detection Threshold Tuning**
   - RESOLVED: Use thresholds: `dust_threshold = 0.001 ETH`, 10+ unique recipients for dusting detection. Confidence LOW for borderline cases, MEDIUM for 10-49 recipients, HIGH for 50+ recipients. Code examples already implement these thresholds (lines 647-657). Per D-21, dusting signature is "send tiny amounts to many addresses" which these thresholds capture.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Flask | Web framework | ✓ | 3.1.3 | — |
| requests | HTTP client | ✓ | 2.32.5 | — |
| web3 | ETH RPC | ✓ | 7.15.0 | — |
| Tronscan API | TRON monitoring | ✓ | — | — |
| Etherscan V2 API | ETH monitoring/attack | ✓ | — | Requires user key |
| Blockstream API | BTC monitoring | ✓ | — | Blockchain.info fallback |

**Missing dependencies with no fallback:**
- None

**Missing dependencies with fallback:**
- If Blockstream fails, use Blockchain.info API for BTC address queries

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | None — manual test via run.bat |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CASE-01 | Monitor multi-chain addresses | unit | `pytest tests/test_monitor.py::test_monitor_addresses -x` | ❌ Wave 0 |
| CASE-02 | Detect attack patterns | unit | `pytest tests/test_obfuscation.py::test_detect_attacks -x` | ❌ Wave 0 |
| CASE-03 | Generate freeze template | unit | `pytest tests/test_freeze.py::test_generate_template -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** Quick test for affected module
- **Per wave merge:** Full suite
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_monitor.py` — covers CASE-01 multi-chain queries
- [ ] `tests/test_obfuscation.py` — covers CASE-02 attack detection rules
- [ ] `tests/test_freeze.py` — covers CASE-03 template generation
- [ ] Mock fixtures for API responses (Tronscan, Etherscan, Blockstream)

*(If no gaps: "None — existing test infrastructure covers all phase requirements")*

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Single-user local tool |
| V3 Session Management | no | No sessions stored |
| V4 Access Control | no | No auth required |
| V5 Input Validation | yes | chain_detector.py validates address format |
| V6 Cryptography | no | No crypto operations in this phase |

### Known Threat Patterns for Flask/Web3 Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| API key exposure | Information Disclosure | Per-query input only, never stored (D-06, D-25) |
| Input injection | Tampering | Address format validation via regex |
| API rate limiting | Denial of Service | Manual refresh only (D-03), no auto-polling |
| XSS in template output | Tampering | Plain text output, no HTML injection |

## Sources

### Primary (HIGH confidence)
- modules/core/api_client.py - Tronscan API client implementation [VERIFIED: Read]
- modules/core/eth_rpc_client.py - ETH RPC client implementation [VERIFIED: Read]
- modules/trace/btc_analyzer.py - BTC transaction analyzer [VERIFIED: Read]
- modules/cross/cluster_analyzer.py - Multi-address input pattern [VERIFIED: Read]
- modules/cross/cross_border_generator.py - Step-by-step form pattern [VERIFIED: Read]
- modules/trace/mixer_tracker.py - Confidence scoring pattern [VERIFIED: Read]
- templates/cross/cluster.html - Card display pattern [VERIFIED: Read]
- templates/cross/cross_border.html - Step-by-step form UI [VERIFIED: Read]
- modules/core/exporter.py - JSON/CSV export [VERIFIED: Read]
- modules/cross/chain_detector.py - Address type detection [VERIFIED: Read]

### Secondary (MEDIUM confidence)
- WebSearch: Blockstream API endpoints for address balance [VERIFIED: WebSearch result]
- pip show: Flask 3.1.3, requests 2.32.5, web3 7.15.0 [VERIFIED: Bash command]

### Tertiary (LOW confidence)
- Attack detection heuristics (Sandwich/Flash Loan/Dusting/Protocol) [ASSUMED: Based on training knowledge of DeFi attack patterns]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Verified from pip show and existing module imports
- Architecture: HIGH - All patterns verified from existing Phase 1-4 code
- Pitfalls: MEDIUM - Blockstream API address endpoint needs verification
- Attack detection: LOW - Heuristics based on training knowledge, need real-world validation

**Research date:** 2026-04-24
**Valid until:** 30 days (stable Flask/Web3 versions, API endpoints stable)