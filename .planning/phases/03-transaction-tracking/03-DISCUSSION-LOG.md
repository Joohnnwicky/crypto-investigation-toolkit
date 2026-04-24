# Phase 3: Transaction Tracking Tools - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-24
**Phase:** 03-transaction-tracking
**Areas discussed:** API/RPC配置方式, 结果展示格式, 追踪深度与时间窗口, 输入参数设计

---

## API/RPC Configuration

### ETH RPC节点选择

| Option | Description | Selected |
|--------|-------------|----------|
| 内置公共节点 | 使用公共节点（eth.drpc.org），无需密钥，但可能不稳定或限速。适合初学者一键使用 | ✓ |
| 用户自备RPC URL | 用户每次查询时输入自己的RPC URL，更可靠，但需要用户自行获取 | |
| 混合模式 | 默认使用公共节点，界面提供"高级设置"让用户输入自定义RPC | |

**User's choice:** 内置公共节点（推荐）
**Notes:** 与Phase 2 ETH工具不同，ETH RPC节点不需要用户输入密钥（公共节点免费可用）

### BTC API选择

| Option | Description | Selected |
|--------|-------------|----------|
| 内置公开API | Blockchain.info公开API，无需密钥，有请求限制约5次/秒。适合初学者和单次查询 | ✓ |
| 用户自备API key | 用户输入自己的API key，更稳定、请求限制更高 | |
| 双API源备份 | 默认blockchain.info，界面提供"切换API源"选项（blockstream作为备用） | |

**User's choice:** 内置公开API（推荐）

---

## Result Display Format

### 资金链条展示方式

| Option | Description | Selected |
|--------|-------------|----------|
| 文字流程图 | 保持脚本中的ASCII diagram风格，简单直观，与现有工具卡片风格一致 | ✓ |
| 分层卡片组件 | 使用HTML卡片组件展示每一层，可展开/折叠查看详情 | |
| 时间线可视化 | 显示时间线（时间点+事件），每层一个节点 | |

**User's choice:** 文字流程图（推荐）

### 单个工具结果展示

| Option | Description | Selected |
|--------|-------------|----------|
| Card-based详情卡片 | 与Phase 1-2一致：分析结果以卡片形式展示，每个发现一张卡片 | ✓ |
| 表格列表形式 | 以表格形式列出所有结果 | |
| 表格+卡片混合 | 结果表格 + 点击展开详情卡片 | |

**User's choice:** Card-based详情卡片（推荐）

---

## Tracking Depth & Time Window

### 混币器时间窗口

| Option | Description | Selected |
|--------|-------------|----------|
| 固定24小时 | 脚本默认24小时，足够覆盖大多数快速提款场景。初学者不需要调整参数 | ✓ |
| 用户可配置 | 界面提供时间窗口输入框，默认24小时，用户可调整为6/12/48/72小时 | |

**User's choice:** 固定24小时（推荐）

### 追踪深度

| Option | Description | Selected |
|--------|-------------|----------|
| 固定5层 | 脚本默认3-5层，足以追踪到交易所或明显终点。初学者不需要调整参数 | ✓ |
| 用户可配置 | 界面提供深度选择（1/3/5/10层），适应不同复杂度案件 | |

**User's choice:** 固定5层（推荐）

### BTC分析范围

| Option | Description | Selected |
|--------|-------------|----------|
| 单笔交易解析 | 仅分析单笔交易：解析输入输出、计算手续费、识别交易类型、识别地址类型 | ✓ |
| 解析+流向追踪 | 除了单笔解析，还追踪后续流向（trace_bitcoin_flow功能） | |

**User's choice:** 单笔交易解析（推荐）

---

## Input Parameters

### Uniswap输入方式

| Option | Description | Selected |
|--------|-------------|----------|
| 地址输入 | 输入以太坊地址，查询该地址的所有Swap交易。适合追踪可疑地址的DEX活动 | ✓ |
| 交易哈希输入 | 输入交易哈希，解析单笔Swap交易详情 | |
| 双模式切换 | 界面提供切换：可选择按地址查询或按交易解析 | |

**User's choice:** 地址输入（推荐）

### Mixer输入方式

| Option | Description | Selected |
|--------|-------------|----------|
| 仅存款时间 | 输入存款时间，系统自动在所有混币池中搜索24小时内的提款 | ✓ |
| 混币池+存款时间 | 用户需要先选择混币池（1ETH/10ETH/100ETH），再输入存款时间 | |
| 存款交易哈希 | 输入交易哈希，系统解析交易获取存款时间和混币池信息 | |

**User's choice:** 仅存款时间（推荐）

### 样本填充按钮

| Option | Description | Selected |
|--------|-------------|----------|
| 包含样本填充按钮 | 与Phase 1-2一致：每个输入框旁边有样本填充按钮，帮助初学者理解输入格式 | ✓ |
| 不包含样本填充 | 不提供样本填充，用户需要自行准备真实数据 | |

**User's choice:** 包含样本填充按钮（推荐）

---

## Claude's Discretion

- ETH RPC节点具体选择（drpc、llamarpc等）
- Blockchain.info vs Blockstream API选择
- 混币池地址列表更新（Tornado Cash V1/V2）
- 错误处理和重试逻辑
- Loading状态展示细节

## Deferred Ideas

None — discussion stayed within phase scope.