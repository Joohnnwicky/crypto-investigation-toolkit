# Phase 3: Transaction Tracking Tools - Research

**Researched:** 2026-04-24
**Domain:** Ethereum/BTC Transaction Tracing (Uniswap, Tornado Cash, BTC Analysis)
**Confidence:** HIGH

## Summary

本阶段将三个现有Python脚本转化为Web界面工具，复用Phase 1-2的Flask Blueprint架构和Card-based UI模式。核心技术栈为web3.py（ETH RPC连接）和Blockstream API（BTC交易查询），无需用户配置API密钥。

**Primary recommendation:** 直接复用现有脚本的核心逻辑，封装为Flask Blueprint模块，使用公共RPC/API节点，保持与Phase 1-2一致的UI风格。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** ETH RPC使用内置公共节点（eth.drpc.org），无需用户配置密钥
- **D-02:** BTC API使用内置公开API（Blockchain.info），无需用户配置密钥
- **D-03:** 与Phase 2 ETH工具不同，ETH RPC节点不需要用户输入（公共节点免费可用）
- **D-04:** 资金链条使用文字流程图展示（ASCII diagram风格），保持脚本原味
- **D-05:** 单个工具结果使用Card-based详情卡片，与Phase 1-2一致
- **D-06:** Uniswap显示Swap详情卡片，Mixer显示可疑提款卡片，BTC显示交易解析卡片
- **D-07:** 混币器时间窗口固定24小时（不需要用户配置）
- **D-08:** 追踪深度固定5层（不需要用户配置）
- **D-09:** BTC工具仅做单笔交易解析，不追踪后续流向
- **D-10:** Uniswap工具：地址输入（查询该地址的所有Swap交易）
- **D-11:** Mixer工具：仅存款时间输入（系统自动搜索所有混币池）
- **D-12:** BTC工具：交易哈希输入（解析单笔交易）
- **D-13:** 所有工具包含样本填充按钮，帮助初学者理解输入格式

### Claude's Discretion
- ETH RPC节点具体选择（drpc、llamarpc等）
- Blockchain.info vs Blockstream API选择
- 混币池地址列表更新（Tornado Cash V1/V2）
- 错误处理和重试逻辑
- Loading状态展示细节

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TRACE-01 | User can trace Uniswap DEX trading paths | Canonical script 002-day3 demonstrates Web3 connection, Swap parsing, flow visualization |
| TRACE-02 | User can trace mixer (混币器) laundering paths | Canonical script 002-day2 implements time_window_analysis with Tornado Cash pools |
| TRACE-03 | User can analyze BTC transaction flow | Canonical script 004-day1 provides parse_bitcoin_transaction, identify_address_type |

</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Uniswap Swap parsing | API / Backend | — | Web3 RPC calls require backend processing |
| Tornado Cash event filtering | API / Backend | — | Historical event logs fetched via Web3 get_logs |
| BTC transaction query | API / Backend | CDN / Static (Blockstream API) | Blockstream provides public API, backend acts as proxy |
| ASCII flow diagram display | Browser / Client | — | Pre-rendered text output, no client-side processing |
| Result card rendering | Browser / Client | — | Jinja2 template renders structured data |
| JSON/CSV export | API / Backend | — | exporter.py generates downloadable files |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| web3.py | 7.15.0 [VERIFIED: pip registry] | ETH RPC连接和事件解析 | 官方Ethereum Python库，ABI解析、事件过滤完整支持 |
| Flask | 3.1.3 [VERIFIED: requirements.txt] | Web框架和Blueprint | Phase 1-2已验证的架构 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| requests | 2.32.0+ [VERIFIED: requirements.txt] | HTTP API调用 | BTC Blockstream API查询 |
| datetime | stdlib | 时间处理 | 时间戳转换、时间窗口计算 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Blockstream API | Blockchain.info API | Blockstream无需API key，响应结构更清晰（vin/vout/fee/status） |
| eth.drpc.org | eth.llamarpc.com | drpc稳定性更好，llamarpc作为备用 |
| web3.py get_logs | Etherscan API events | 公共节点不支持过滤器，get_logs是唯一可行方案 |

**Installation:**
```bash
pip install web3==7.15.0
```

**Version verification:**
```
web3.py: 7.15.0 (latest as of pip index)
Flask: 3.1.3 (existing)
requests: 2.32.0+ (existing)
```

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Browser / Client                                │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
│  │ /trace/uniswap  │    │ /trace/mixer    │    │ /trace/btc      │      │
│  │  地址输入       │    │  存款时间输入   │    │  交易哈希输入   │      │
│  └───────┬─────────┘    └───────┬─────────┘    └───────┬─────────┘      │
│          │                      │                      │                 │
│          ▼                      ▼                      ▼                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              Flask Backend (Blueprint: trace_bp)                 │   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │                    routes.py                                 ││   │
│  │  │  /api/uniswap/query → uniswap_tracker.py                    ││   │
│  │  │  /api/mixer/query   → mixer_tracker.py                      ││   │
│  │  │  /api/btc/query     → btc_analyzer.py                       ││   │
│  │  │  /api/export/json   → exporter.py                           ││   │
│  │  │  /api/export/csv    → exporter.py                           ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  └─────────────────────────────────┬───────────────────────────────┘   │
│                                    │                                    │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          External APIs                                   │
│  ┌─────────────────────┐        ┌─────────────────────┐                 │
│  │  ETH RPC            │        │  Blockstream API    │                 │
│  │  eth.drpc.org       │        │  blockstream.info   │                 │
│  │  (Uniswap/Mixer)    │        │  /api/tx/{txid}     │                 │
│  └─────────────────────┘        └─────────────────────┘                 │
│                                                                          │
│  Tornado Cash Pools (contract addresses):                               │
│  0.1 ETH: 0x12D66f87A04A9E220743712cE6d9bB1B5616B8Fc                    │
│  1 ETH:   0x47CE0C6eD5B0Ce3d3A51fdb1C52DC66a7c3c2936                    │
│  10 ETH:  0x910Cbd523D972eb0a6f4cAe4678e38953813e14                     │
│  100 ETH: 0xA160cdAB225685dA1d56aa342Ad8841c3b53f291                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure
```
docs/superpowers/
├── modules/
│   ├── core/
│   │   ├── api_client.py      # 现有API client模式（Tronscan/Etherscan）
│   │   ├── formatter.py       # 现有格式化工具
│   │   ├── exporter.py        # 现有JSON/CSV导出
│   │   └── eth_rpc_client.py  # 新增：Web3 RPC client封装（重试逻辑）
│   └── trace/                  # 新增模块目录
│       ├── __init__.py
│       ├── routes.py           # Flask Blueprint路由
│       ├── uniswap_tracker.py  # Uniswap V2追踪逻辑
│       ├── mixer_tracker.py    # Tornado Cash时间窗口分析
│       ├── btc_analyzer.py     # BTC交易解析
│       └── tornado_pools.py    # 混币池地址配置
├── templates/
│   └── trace/                  # 新增模板目录
│       ├── uniswap.html        # Uniswap追踪页面
│       ├── mixer.html          # 混币器追踪页面
│       └── btc.html            # BTC交易分析页面
└── app.py                      # 注册trace_bp Blueprint
```

### Pattern 1: Flask Blueprint Registration
**What:** 每个工具类别创建独立Blueprint，注册到app.py
**When to use:** 所有新模块添加
**Example:**
```python
# Source: modules/eth/routes.py [VERIFIED: existing codebase]
from flask import Blueprint, jsonify, request, Response, render_template

eth_bp = Blueprint('eth', __name__, url_prefix='/eth')

@eth_bp.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    # ... processing logic
    return jsonify(result)

@eth_bp.route('/transaction-query')
def transaction_query_page():
    return render_template('eth/transaction_query.html')
```

### Pattern 2: Web3 Event Filtering (get_logs)
**What:** 使用contract.events.EventName.get_logs()获取历史事件
**When to use:** 公共RPC节点不支持create_filter，必须用get_logs
**Example:**
```python
# Source: 002-day2-完整混币追踪流程.py [VERIFIED: canonical script]
contract = self.w3.eth.contract(
    address=Web3.to_checksum_address(pool_address),
    abi=[self.withdrawal_event_abi]
)

# 公共节点不支持过滤器，必须使用get_logs
withdrawals = contract.events.Withdrawal.get_logs(
    from_block=start_block,
    to_block=end_block
)
```

### Pattern 3: Blockstream API Response Structure
**What:** BTC交易查询返回标准化JSON结构
**When to use:** BTC交易解析
**Example:**
```json
// Source: Blockstream API docs [VERIFIED: github.com/Blockstream/esplora]
{
  "txid": "...",
  "version": 1,
  "locktime": 0,
  "size": 225,
  "weight": 900,
  "fee": 1000,  // satoshis
  "vin": [{"txid": "...", "vout": 0, "scriptsig": "...", "sequence": 0xffffffff}],
  "vout": [{"scriptpubkey_address": "...", "value": 50000000}],
  "status": {"confirmed": true, "block_height": 785456, "block_time": 1713256800}
}
```

### Anti-Patterns to Avoid
- **不要使用create_filter:** 公共RPC节点不支持，必须用get_logs
- **不要硬编码混币池地址:** 使用tornado_pools.py配置文件，便于更新
- **不要在BTC工具追踪后续流向:** D-09锁定仅做单笔解析

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| ETH RPC连接 | 自建HTTP client | web3.py HTTPProvider | 已处理ABI编码、事件解析、单位转换 |
| BTC交易查询 | 自己构造API URL | requests + Blockstream API | 标准化响应结构，无需API key |
| 时间戳转换 | 手动计算 | formatter.format_timestamp | Phase 1-2已验证的格式化工具 |
| JSON/CSV导出 | 自己拼接字符串 | exporter.py | 已实现，统一格式 |

**Key insight:** web3.py库已处理所有ABI编码复杂性（Transfer事件签名0xddf252ad...），不要手动解析事件数据。

## Runtime State Inventory

> Not applicable for this phase (greenfield implementation, no rename/refactor).

## Common Pitfalls

### Pitfall 1: Public RPC Node Instability
**What goes wrong:** 公共节点（drpc、llamarpc）可能超时或拒绝请求
**Why it happens:** 免费节点有请求限制，高峰期不稳定
**How to avoid:** 实现重试逻辑（3次重试，5秒超时），备用节点切换
**Warning signs:** HTTP 429/503响应，长时间无响应

### Pitfall 2: Block Range Too Large
**What goes wrong:** get_logs查询区块范围过大导致超时
**Why it happens:** 24小时时间窗口约7200个区块，部分节点限制单次查询
**How to avoid:** 分批查询（每次1000区块），或使用更精确的时间估算
**Warning signs:** "exceeds maximum block range"错误

### Pitfall 3: BTC Address Regex False Positive
**What goes wrong:** 错误识别地址类型（P2PKH vs P2SH）
**Why it happens:** Base58字符集相似，正则边界不清
**How to avoid:** 使用canonical script中的已验证正则表达式
**Warning signs:** 识别为"Unknown"但地址有效

### Pitfall 4: Tornado Cash Pool Address Outdated
**What goes wrong:** 使用旧版混币池地址导致查询无结果
**Why it happens:** 2022年制裁后部分地址变更
**How to avoid:** 在tornado_pools.py配置最新地址，并标记版本
**Warning signs:** get_logs返回空列表，但Blockstream显示有提款

## Code Examples

### Uniswap Swap Transaction Parsing
```python
# Source: 002-day3-Uniswap 交易追踪器.py [VERIFIED: canonical script]
def parse_swap_transaction(self, tx_hash):
    tx = self.w3.eth.get_transaction(tx_hash)
    receipt = self.w3.eth.get_transaction_receipt(tx_hash)
    
    result = {
        "hash": tx_hash,
        "from": tx['from'],
        "to": tx['to'],
        "value": self.w3.from_wei(tx['value'], 'ether'),
        "logs": []
    }
    
    # 解析ERC-20 Transfer事件
    TRANSFER_EVENT_SIG = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b8"
    for log in receipt['logs']:
        if log['topics'][0].hex() == TRANSFER_EVENT_SIG:
            from_addr = "0x" + log['topics'][1].hex()[26:]
            to_addr = "0x" + log['topics'][2].hex()[26:]
            value = int(log['data'], 16)
            result['logs'].append({
                "event": "Transfer",
                "from": Web3.to_checksum_address(from_addr),
                "to": Web3.to_checksum_address(to_addr),
                "value": value
            })
    return result
```

### Tornado Cash Time Window Analysis
```python
# Source: 002-day2-完整混币追踪流程.py [VERIFIED: canonical script]
def time_window_analysis(self, pool_address, deposit_time, window_hours=24):
    deposit_ts = datetime.strptime(deposit_time, "%Y-%m-%d %H:%M:%S").timestamp()
    start_ts = deposit_ts
    end_ts = deposit_ts + (window_hours * 3600)
    
    # 区块估算：从创世区块开始计算
    genesis_ts = datetime(2015, 7, 30, 15, 26, 28).timestamp()
    avg_block_time = 12  # ETH平均区块时间约12秒
    start_block = int((start_ts - genesis_ts) / avg_block_time)
    end_block = int((end_ts - genesis_ts) / avg_block_time)
    
    withdrawals = self.get_withdrawals(pool_address, start_block, end_block)
    
    suspicious = []
    for wd in withdrawals:
        ts = wd['timestamp'].timestamp()
        if start_ts <= ts <= end_ts:
            suspicious.append(wd)
    return suspicious
```

### BTC Address Type Identification
```python
# Source: 004-day1-比特币交易分析.py [VERIFIED: canonical script]
import re

def identify_address_type(address):
    result = {"address": address, "type": None, "wallet_hint": None}
    
    if re.match(r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        result["type"] = "P2PKH"
        result["wallet_hint"] = "较老的钱包或冷钱包"
    
    elif re.match(r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        result["type"] = "P2SH"
        result["wallet_hint"] = "多重签名钱包、交易所热钱包"
    
    elif re.match(r'^bc1q[ac-hj-np-z02-9]{39,59}$', address.lower()):
        result["type"] = "P2WPKH"
        result["wallet_hint"] = "现代软件钱包（Coinbase、Blockstream Green）"
    
    elif re.match(r'^bc1p[ac-hj-np-z02-9]{58}$', address.lower()):
        result["type"] = "P2TR"
        result["wallet_hint"] = "最新钱包，支持Taproot"
    
    else:
        result["type"] = "Unknown"
    
    return result
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Web3 create_filter | get_logs | web3.py 5.x+ | 公共节点不支持过滤器 |
| Blockchain.info API | Blockstream API | 2022+ | 更清晰的响应结构，无API key |
| 手动事件解析 | web3.py contract.events | web3.py 6.x+ | ABI自动处理编码 |

**Deprecated/outdated:**
- Etherscan V1 API: 使用V2 API with chainid=1 [VERIFIED: Phase 2 fix]
- Tornado Cash旧版地址: 使用最新配置文件中的地址列表

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Blockstream API无需API key，直接可用 | BTC分析 | 需验证API是否需要认证 |
| A2 | Tornado Cash合约仍可查询事件 | Mixer追踪 | 制裁后可能被节点屏蔽 |
| A3 | Uniswap Router地址固定不变 | Uniswap | 仅V2版本，V3不同 |

## Open Questions (RESOLVED)

1. **Blockstream API vs Blockchain.info** — RESOLVED: 使用Blockstream作为主API，Blockchain.info作为备用。Blockstream响应结构更清晰，无需API key，已在Plan 03采用。

2. **Tornado Cash Pool Address Verification** — RESOLVED: 使用tornado_pools.py配置文件管理地址列表，便于后续更新。Plan 02实现了配置化混币池地址。

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| web3.py | Uniswap/Mixer tools | ✗ (needs install) | — | pip install web3==7.15.0 |
| Flask | Web framework | ✓ | 3.1.3 | — |
| requests | BTC API calls | ✓ | 2.32.5 | — |
| ETH RPC (drpc) | Uniswap/Mixer | ✓ (public) | — | llamarpc备用 |
| Blockstream API | BTC analysis | ✓ (public) | — | Blockchain.info备用 |

**Missing dependencies with no fallback:**
- None — all dependencies have install commands or public alternatives

**Missing dependencies with fallback:**
- web3.py: pip install web3==7.15.0 (install command)
- ETH RPC: drpc主节点，llamarpc备用
- BTC API: Blockstream主API，Blockchain.info备用

## Validation Architecture

> nyquist_validation is false in config.json — skip automated test framework setup.

**Manual validation approach:**
- 每个工具使用样本数据进行功能验证
- 真实交易哈希测试（Uniswap已知Swap、Tornado已知提款、BTC已知交易）
- 用户手动验证输出格式正确

## Security Domain

> Minimal security requirements for this phase (no user auth, no data storage).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | 单用户本地工具，无认证需求 |
| V3 Session Management | no | 无session，无持久化 |
| V4 Access Control | no | 无用户权限区分 |
| V5 Input Validation | yes | 地址/哈希格式验证（正则表达式） |
| V6 Cryptography | no | 无加密需求 |

### Known Threat Patterns for Flask + Public APIs

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| RPC节点欺骗 | Spoofing | 使用知名公共节点（drpc官方） |
| 输入注入 | Tampering | 地址格式严格验证（正则） |
| API响应篡改 | Tampering | 验证响应结构完整性 |
| 服务拒绝 | Denial | 重试逻辑、备用节点 |

## Sources

### Primary (HIGH confidence)
- Canonical scripts: 002-day3-Uniswap, 002-day2-Tornado, 004-day1-BTC [VERIFIED: existing files]
- Blockstream API docs: github.com/Blockstream/esplora/API.md [VERIFIED: WebFetch]
- Existing patterns: modules/eth/routes.py, modules/core/exporter.py [VERIFIED: codebase]

### Secondary (MEDIUM confidence)
- web3.py pip registry: version 7.15.0 available [VERIFIED: pip index]
- Tornado Cash pool addresses: from canonical scripts [VERIFIED: script]

### Tertiary (LOW confidence)
- Blockstream API稳定性: [ASSUMED] based on public availability
- Tornado Cash合约可查询性: [ASSUMED] based on script functionality

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - web3.py版本已验证，Flask已安装
- Architecture: HIGH - Blueprint模式已在Phase 1-2验证
- Pitfalls: HIGH - 从canonical脚本分析得出
- API patterns: MEDIUM - Blockstream结构已验证，稳定性待确认

**Research date:** 2026-04-24
**Valid until:** 2026-05-24 (stable APIs, 30 days)