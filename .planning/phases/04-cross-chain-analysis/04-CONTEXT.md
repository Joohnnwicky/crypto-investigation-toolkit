# Phase 4: Cross-Chain Analysis Tools - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

完成两个跨链分析工具：地址聚类工具和跨境协查工具。地址聚类用于关联多个地址（首次资金来源、频繁互转账、时间窗口、共享存款），跨境协查用于生成国际协作模板。

**In scope:**
- 地址聚类工具（多地址输入，四维聚类分析，分组卡片结果展示）
- 跨境协查工具（分步表单输入，标准模板生成，支持从聚类导入）
- TRON + ETH + BTC 三链支持
- ETH API密钥输入（每次查询输入，不存储）
- 样本填充按钮
- JSON/CSV导出功能（地址聚类）
- 文本复制导出（跨境协查模板）

**Out of scope:**
- 用户认证系统
- 数据持久化存储
- 云端部署
- 实时监控功能
- 其他链（Solana、BSC等）支持
- 多辖区模板（仅标准模板）
- DOCX/PDF导出（跨境协查仅文本复制）

</domain>

<decisions>
## Implementation Decisions

### 地址聚类工具 - 输入设计
- **D-01:** 输入方式为文本域（多行输入框），每行一个地址，最多10个地址
- **D-02:** 支持TRON + ETH + BTC三链地址聚类
- **D-03:** ETH分析需要用户输入API密钥（每次查询输入，不存储），BTC使用免费Blockstream API（无需密钥）
- **D-04:** 提供样本填充按钮，帮助初学者理解输入格式

### 地址聚类工具 - 聚类逻辑
- **D-05:** 聚类依据1：首次资金来源相同（追踪所有地址的首次入账来源）
- **D-06:** 聚类依据2：频繁互转账（检查地址之间的直接转账频率）
- **D-07:** 聚类依据3：时间窗口关联（分析地址活动时间重叠度）
- **D-08:** 聚类依据4：共享存款地址（识别是否使用相同的存款地址）

### 地址聚类工具 - 结果展示
- **D-09:** 结果采用分组卡片（Cluster Cards）形式，每组显示地址列表和关联原因
- **D-10:** 每个聚类显示：关联类型和原因、交易统计、时间窗口信息、共享地址信息
- **D-11:** 未找到关联的地址单独显示，注明"无关联"
- **D-12:** 支持JSON/CSV导出聚类结果

### 跨境协查工具 - 模板内容
- **D-13:** 模板格式为HTML页面 + 文本导出（浏览器直接显示，用户可复制）
- **D-14:** 模板字段包含：案件基本信息、涉案地址与交易信息、调查背景说明、协查请求内容
- **D-15:** 案件基本信息：案件编号、调查机构、联系人、联系方式
- **D-16:** 涉案地址与交易信息：涉案地址列表、链类型、金额汇总、交易哈希
- **D-17:** 调查背景说明：可疑行为描述、资金流向简述、调查背景
- **D-18:** 协查请求内容：请求类型（信息查询、资产冻结等）、期望回复时间

### 跨境协查工具 - 工作流程
- **D-19:** 输入流程为分步表单（案件信息 → 地址选择 → 模板生成）
- **D-20:** 支持从地址聚类结果导入地址列表（"导出到跨境协查"按钮）
- **D-21:** 使用标准模板（单一格式），不提供多辖区模板

### Claude's Discretion
- TRON/ETH/BTC API调用具体实现细节
- 聚类阈值设定（频繁互转账次数阈值、时间窗口重叠度阈值）
- 错误处理和重试逻辑
- Loading状态展示细节
- HTML模板具体样式设计

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §CROSS-01, CROSS-02 — 跨链分析工具需求定义

### Existing Patterns (reference from Phase 1-3)
- `modules/core/api_client.py` — Tronscan API client（TRON地址分析）
- `modules/core/eth_rpc_client.py` — ETH RPC client（ETH地址分析）
- `modules/trace/btc_analyzer.py` — BTC analyzer（BTC地址分析参考）
- `modules/core/exporter.py` — JSON/CSV导出功能
- `templates/base.html` — 基础模板（侧边栏、底部声明）
- `templates/eth/transaction_query.html` — ETH工具页面布局参考（API密钥输入）
- `templates/trace/uniswap.html` — 追踪工具页面布局参考

### External APIs
- Tronscan API — https://api.tronscan.org/api（TRON地址查询，免费）
- Etherscan API V2 — https://api.etherscan.io/v2/api（ETH地址查询，需密钥）
- Blockstream API — https://blockstream.info/api（BTC地址查询，免费）
- Blockchain.info API — https://blockchain.info（BTC交易查询，免费）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/core/api_client.py` — Tronscan API client，可用于TRON地址聚类分析
- `modules/core/eth_rpc_client.py` — ETH RPC client，可用于ETH地址聚类分析
- `modules/trace/btc_analyzer.py` — BTC analyzer，可扩展用于BTC地址聚类分析
- `modules/core/formatter.py` — 数据格式化工具
- `modules/core/exporter.py` — JSON/CSV导出功能
- `templates/base.html` — 基础模板（侧边栏、底部声明）
- `templates/eth/transaction_query.html` — ETH工具页面（含API密钥输入UI）

### Established Patterns
- Flask Blueprint modular architecture — 每个工具类别一个模块
- Analysis pattern: structured result dict (success, addresses, clusters/results)
- UI pattern: input → analyze button → results cards
- API密钥输入: 每次查询时输入，不存储
- Sample filling button: 每个输入框旁提供样本数据按钮

### Integration Points
- `app.py` — 需注册新的cross-chain blueprint
- `templates/cross/` — 新建跨链工具页面目录（cluster.html, cross_border.html）
- `modules/cross/` — 新建跨链模块目录（routes.py, cluster_analyzer.py, cross_border_generator.py）

### Sidebar Already Configured
- `/cross/cluster` → 地址聚类
- `/cross/cross-border` → 跨境协查

</code_context>

<specifics>
## Specific Ideas

- 地址聚类应该清晰标注每个聚类的核心原因（如"首次资金来源相同: TXxx..."）
- 跨境协查模板应该简洁实用，便于初学者复制使用
- 地址聚类结果页面提供"导出到跨境协查"按钮，实现工具联动
- 跨境协查的分步表单应该有清晰的步骤指示（Step 1/2/3）
- 所有工具界面保持简洁，与现有TRON/ETH工具风格一致

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 04-cross-chain-analysis*
*Context gathered: 2026-04-24*