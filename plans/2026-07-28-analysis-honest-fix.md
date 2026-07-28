# BLOCKSHADE 分析逻辑诚实化修复

## 约束
- **保持响应顶层字段不变**：路由是透传，前端/CSV 只读特定键（`balance`/`tx_count`/`cluster_id`/`reasons`/`attack_cards`/`suspicious_withdrawals`/`swaps`/`bridge_events` 等）。只改内部逻辑，可新增子字段，不删前端依赖的键。
- **不新增依赖**：仍用 Tronscan / Etherscan / Blockstream / 现有 public ETH RPC（drpc/llamarpc）。
- **不新增图遍历**、不实现 Tornado merkle 去匿名、不实现 BTC co-spend 聚类（用户选 A）。
- 不动前端样式（Anduril 重构已完成）。

---

## 修复清单（按文件，附问题编号）

### 1. `modules/tron/suspicious_analyzer.py` — 修 ①⑦⑧
- **① 快进快出时间反向**（`:84-109`）：先 `sorted(transfers, key=block_timestamp)` 升序；找大额入金后，向**后**遍历找该地址出金，`time_diff = out_ts - in_ts`，条件改 `0 < time_diff <= 24h`。修后红牌能真正触发。
- **⑦ 余额清空误报**（`:61`）：条件改为「曾持有 USDT（`trc20_transfers` 中存在 `to==address` 入账）且当前余额 0」。纯 TRX 钱包不再误报。新增 yellow 提示「仅分析 TRC20，TRX/TRC10/内部合约交易未覆盖」。
- **⑧ 风险评分伪精确**：保留 `score` 字段（前端兼容），新增 `risk_level`（低/中/高，由 score 区间映射：0-30低 / 31-60中 / 61-100高）。下调「余额清空」权重，仅当「曾持有+清空」才计分。`meaning` 统一加「仅供参考，非司法证据」提示。

### 2. `modules/case/monitor.py` — 修 ②
- **ETH 余额造假**（`:130-143`）：删除「最近100笔 normal tx 加减」估算。改用 Etherscan `module=account&action=balance` 取真实 ETH 余额（单次、免费）。失败时 `balance=None`、`balance_note='API查询失败'`，不再给假数。保留 `balance`/`balance_note`/`tx_count`/`last_active` 字段。TRX 余额已真实，保留。

### 3. `modules/cross/cluster_analyzer.py` — 修 ③
- **删除两个弱信号**：①「首次资金来源相同」（D-05，交易所热钱包致海量假阳性）；②「时间窗口重叠≥70%」（D-07，纯噪声）。
- **保留并强化**：互转账（提高阈值，要求双向或单向≥3次）、共享存款地址。
- **修传递闭包**（`:387`）：`checked.update` 单趟合并改为并查集（union-find），O(n²) 配对后合并连通分量，保证 a-b、a-c 能推出 b-c 同簇。
- **BTC 诚实降级**：标注「BTC 聚类需 co-spend 启发式，当前未实现」，`limited_data=True`，不参与聚类。
- 保留响应字段 `clusters[{cluster_id, addresses, chain_types, reasons, shared_source, mutual_transfers, time_window, shared_deposit, stats}]`、`unassociated`。`reasons` 内容随逻辑更新。

### 4. `modules/trace/mixer_tracker.py` + `tornado_pools.py` — 修 ④
- **重命名语义**：结果改称「时间窗内提款参考列表」，不再叫「可疑提款」。
- **置信度重写**（`mixer_tracker.py:128`）：删除「前缀匹配交易所=HIGH」。新分级：recipient 与存款地址相同→HIGH（诚实，极少触发）；提款在存款后短时间内（<1h）→MEDIUM（弱时间信号）；其余→LOW/参考。每个结果加 `note`：「时间窗无法单独确定关联，需 deposit-note 匹配」。
- **block 估算**（`:57`）：线性估算改为按 chunk 限制 `get_logs` 范围（每段≤2000块），避免被公共 RPC 拒绝；失败跳过并记录。
- **删除 `EXCHANGE_PREFIXES` 前缀误判用法**（`tornado_pools.py:50`）：该前缀表不再用于提款 recipient 判定。
- 保留 `suspicious_withdrawals[{pool, recipient, fee, date, tx_hash, confidence, reason}]` + 新增 `note`、`flow_diagram`。

### 5. `modules/case/obfuscation_detector.py` — 修 ⑤
- **闪贷**（`:83`）：删除「value>100ETH=Flash Loan」。改为标注「大额交易，需人工复核闪贷可能」，`confidence=LOW`，`type='大额交易(待复核)'`，不再用 Flash Loan 诬告。
- **三明治**（`:51`）：单地址无法检测三方，诚实降级——仅当同区块内该地址对同一 router 有「卖出后买回」反向模式才标 MEDIUM；否则不报。加 note 说明单地址视角局限。加 V3/Universal Router 识别。
- **Dusting**（`:95`）：保留，修正为仅 ETH 转账（ERC20 dust 看不到，标注盲区）。
- **协议漏洞**（`:133`）：保留「高价值失败交易」，`confidence=LOW`，`type='失败交易(待复核)'`。
- 保留 `attack_cards[{type, confidence, tx_hash, details, ...}]` + 可选 `note`。

### 6. `modules/trace/uniswap_tracker.py` — 修 ⑥
- **激活死代码**：`get_address_transactions`（`:263`）改为对每笔 `to=router` 的 tx 调用 `parse_swap_transaction` 解析真实 receipt logs，填充真实 `amount_in`/`amount_out` 数值，不再返回「查看交易详情」字符串。
- **加 Router**：V3 Router（`0xE592427A0AEce92De3Edee1F18E0157C05861564`）+ Universal Router（`0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD`）。
- **RPC 降级**：RPC 不可用时回退原浅逻辑并在结果里标注 `parse_note`。
- 保留 `swaps[{hash, type, amount_in, amount_out, time, from_token, to_token}]`、`swap_count`、`flow_diagram`。

### 7. `modules/eth/eth_analyzer.py` — 修 框架③
- **清理 `BRIDGE_ADDRESSES`**（`:19`）：删除伪造地址（`7c7c7c7c` 重复模式多条），保留可验证地址；Stargate router 改用 `stargate_detector.py` 的正确地址（`0x8731d54E9D02c286767d56ac03e8037C07e01e98`），删除错误的 `0xDef1C0...`（那是 CoW Swap）。
- **去重 Stargate 逻辑**：`eth_analyzer` 的桥检测复用 `stargate_detector.detect_stargate_bridge`，避免两套不一致地址。

### 8. `modules/eth/routes.py` — 修 CSV 死字段
- **CSV 导出读 `stargate_events`**（`:152`）但 analyzer 返回 `bridge_events` → 该段恒空。改为读 `bridge_events`。

### 9. `modules/core/api_client.py` + 去重 — 修 框架②
- 删除 `uniswap_tracker.py:361` 和 `eth_analyzer.py:80` 的本地 `get_eth_transactions`/`get_erc20_transfers`，统一 import 自 `api_client.py`。
- 统一签名（排序/limit/校验）。`eth_analyzer` 原用 asc+末尾 limit，`api_client` 用 desc+offset——统一为 desc+limit，调用方适配（聚类/混淆用 desc 即可）。

### 10. 文档归类 — 框架④（低优先）
- README/侧边栏说明「资产追回/跨境协查」是模板生成而非分析工具。

---

## 验证
1. `python -c "import modules.tron.suspicious_analyzer, modules.case.monitor, modules.cross.cluster_analyzer, modules.trace.mixer_tracker, modules.case.obfuscation_detector, modules.trace.uniswap_tracker, modules.eth.eth_analyzer, modules.core.api_client"` 导入冒烟。
2. `python app.py` 启动，访问各页面确认无 500。
3. 逻辑回归（TRON 可疑分析用样本地址验「快进快出」路径、monitor ETH 余额取真实值、cluster 不再假阳性）。
4. 受 API key 限制的 ETH 工具，验证失败路径不崩、降级标注正确。

## 不做
- Tornado merkle 去匿名 / BTC co-spend 聚类 / 多跳图遍历 / 前端样式改动。

## 风险
- Uniswap 解析依赖 public RPC，可能限流；已规划降级。
- Etherscan balance 端点属免费额度，单次查询 OK。
- 统一 `get_eth_transactions` 排序后，少数调用方依赖 asc 顺序（eth_analyzer 取末尾），需逐一适配，避免回归。
