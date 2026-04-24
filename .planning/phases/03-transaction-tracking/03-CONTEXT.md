# Phase 3: Transaction Tracking Tools - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

完成三个交易追踪工具：Uniswap DEX路径追踪、Tornado Cash混币器追踪、BTC交易分析。复用Phase 1-2的核心框架，将现有Python脚本转化为Web界面。

**In scope:**
- Uniswap追踪工具（地址输入，查询Swap交易历史）
- 混币器追踪工具（存款时间输入，时间窗口分析）
- BTC交易分析工具（交易哈希输入，单笔交易解析）
- 文字流程图展示资金链条
- Card-based结果展示
- JSON/CSV导出功能
- 样本填充按钮

**Out of scope:**
- 用户认证系统
- 数据持久化存储
- 云端部署
- 实时监控功能
- 其他链（Solana、BSC等）支持
- BTC后续流向追踪（仅单笔解析）

</domain>

<decisions>
## Implementation Decisions

### API/RPC Configuration
- **D-01:** ETH RPC使用内置公共节点（eth.drpc.org），无需用户配置密钥
- **D-02:** BTC API使用内置公开API（Blockchain.info），无需用户配置密钥
- **D-03:** 与Phase 2 ETH工具不同，ETH RPC节点不需要用户输入（公共节点免费可用）

### Result Display
- **D-04:** 资金链条使用文字流程图展示（ASCII diagram风格），保持脚本原味
- **D-05:** 单个工具结果使用Card-based详情卡片，与Phase 1-2一致
- **D-06:** Uniswap显示Swap详情卡片，Mixer显示可疑提款卡片，BTC显示交易解析卡片

### Tracking Parameters
- **D-07:** 混币器时间窗口固定24小时（不需要用户配置）
- **D-08:** 追踪深度固定5层（不需要用户配置）
- **D-09:** BTC工具仅做单笔交易解析，不追踪后续流向

### Input Parameters
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

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Original Scripts (MUST read before implementing)
- `../002-day3-Uniswap 交易追踪器.py` — Uniswap V2追踪完整逻辑，包括Web3连接、Swap解析、资金链还原
- `../002-day2-完整混币追踪流程.py` — Tornado Cash时间窗口分析、交易所识别、追踪流程
- `../004-day1-比特币交易分析.py` — BTC交易解析、手续费计算、地址类型识别

### Requirements
- `.planning/REQUIREMENTS.md` §TRACE-01, TRACE-02, TRACE-03 — 交易追踪工具需求定义

### Existing Patterns (reference from Phase 1-2)
- `modules/core/api_client.py` — API client模式，可扩展为ETH RPC client
- `modules/core/formatter.py` — 数据格式化工具
- `modules/core/exporter.py` — JSON/CSV导出功能
- `templates/base.html` — 基础模板（侧边栏、底部声明）
- `templates/eth/transaction_query.html` — ETH工具页面布局参考

### External APIs
- Etherscan API Documentation — https://docs.etherscan.io/（ETH RPC查询可用）
- Blockchain.info API — https://blockchain.info/rawtx/{tx_hash}（BTC交易查询）
- Tornado Cash Pool Addresses — 需要更新最新混币池地址

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/core/api_client.py` — API client模式，可扩展为Web3 client
- `modules/core/formatter.py` — 数据格式化工具（BTC金额格式化可复用）
- `modules/core/exporter.py` — JSON/CSV导出功能
- `modules/eth/routes.py` — Flask Blueprint模式，可复用创建transaction tracking blueprint
- `templates/base.html` — 基础模板（侧边栏、底部声明）

### Established Patterns
- Flask Blueprint modular architecture — 每个工具类别一个模块
- Analysis pattern: structured result dict (success, address, basic_info, alerts/results)
- UI pattern: address input → analyze button → results cards
- Sample filling button: 每个输入框旁提供样本数据按钮

### Integration Points
- `app.py` — 需注册新的transaction tracking blueprint
- `templates/transaction/` — 新建追踪工具页面目录
- `modules/transaction/` — 新建追踪模块目录（routes.py, uniswap_tracker.py, mixer_tracker.py, btc_analyzer.py）

### Web3 Integration (new for Phase 3)
- 需要安装web3.py库（pip install web3）
- ETH RPC连接需要处理公共节点不稳定情况（重试逻辑）
- ERC-20 Transfer事件解析需要ABI定义

</code_context>

<specifics>
## Specific Ideas

- Uniswap工具应该显示完整资金链条（受害者→跨链桥→混币器→DEX→交易所），帮助初学者理解洗钱路径
- Mixer工具的置信度评分（HIGH/MEDIUM）应该以颜色区分显示
- BTC工具的地址类型识别（P2PKH、P2SH、P2WPKH、P2TR）应该清晰标注钱包类型提示
- 所有工具界面保持简洁，与现有TRON/ETH工具风格一致

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 03-transaction-tracking*
*Context gathered: 2026-04-24*