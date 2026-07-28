---
saved: "2026-07-28T00:00:00.000Z"
status: complete
---

# Progress Handoff — 分析逻辑诚实化修复

## 背景
用户要求审查 BLOCKSHADE 区块链分析逻辑的不合理之处，确认框架问题后要求"全改"。选择**诚实化修复**（选项 A）：修 bug + 删假阳性 + 诚实标注，不新增图遍历/不实现 Tornado merkle 去匿名。计划文件：`plans/2026-07-28-analysis-honest-fix.md`。

## What Was Done This Session（已落地 + 验证通过）

| # | 问题 | 文件 | 修复 |
|---|------|------|------|
| ① | 快进快出时间方向反（永不触发） | `modules/tron/suspicious_analyzer.py` | 升序遍历、向前找出金，`0<diff≤24h`。**已验证能触发** |
| ⑦ | 余额清空误报（TRX 钱包） | 同上 | 改为「曾持有 USDT 且归零」才告警。**已验证不再误报** |
| ⑧ | 风险评分伪精确 | 同上 | 新增 `risk_level`（低/中/高），权重下调，加「仅供参考」 |
| ② | ETH 余额造假 | `modules/core/api_client.py`（加 `get_eth_balance`）、`modules/case/monitor.py`、`templates/case/monitor.html`（`formatBalance` null 安全） | 改用 Etherscan balance 端点取真实余额，失败标「不可得」 |
| ③ | 聚类假阳性 | `modules/cross/cluster_analyzer.py` | 删「同源交易所」「时间重叠」两弱信号；保留互转账+「被同一调查地址资助」；**并查集修传递闭包**；BTC 诚实降级；删孤儿函数 `calculate_activity_window`/`calculate_time_overlap`/`find_shared_deposit` + `TIME_OVERLAP_THRESHOLD` |
| ④ | 混币器不追踪 | `modules/trace/mixer_tracker.py`、`modules/trace/tornado_pools.py` | 重命名「提款参考列表」；删前缀误判 HIGH；**修 `start_ts=deposit_time` 字符串/整数比较 bug**（原会崩）；block 范围分 chunk（2000）；加 `note`；删 `EXCHANGE_PREFIXES` + `identify_exchange` |
| ⑤ | 闪贷/三明治假检测 | `modules/case/obfuscation_detector.py` | 闪贷→「大额交易(待复核)」LOW；三明治→「疑似参与(待复核)」LOW；加 V3/Universal Router；协议漏洞→「失败交易(待复核)」 |
| ⑥ | Uniswap 死代码 | `modules/trace/uniswap_tracker.py` | 激活 `parse_swap_transaction` 解析真实 token 流，RPC 失败降级；加 V3/Universal Router；`identify_swap_type` 识别所有 router |
| 框架② | `get_eth_transactions` 三份 | `uniswap_tracker.py`、`eth_analyzer.py` | 删本地副本，统一用 `api_client`；清孤儿 `requests`/`ETHERSCAN_API_URL`/`ETH_CHAIN_ID`/`DEFAULT_TIMEOUT`（uniswap）；eth_analyzer 保留 `get_transaction_logs`+`requests` |
| 框架③ | 桥地址库伪造/冲突 | `modules/eth/eth_analyzer.py`、`modules/eth/routes.py` | 删 7 个伪造地址（`7c7c`/`f5f5`）+ 误标 Stargate（0xDef1 实为 CoW）；CSV 死字段 `stargate_events`→`bridge_events` |

## 验证（已通过）
- 全模块 `import` 通过；`app` 注册 6 blueprint（case/cross/docs/eth/trace/tron）正常。
- 快进快出现在触发（score=55，risk_level=中）；TRX-only 钱包不再误报余额清空。
- 聚类空输入、混币器坏格式输入均不崩。

## Outstanding Work：无（全部完成）

本会话清零两项低风险遗留：

1. ✅ **`BRIDGE_ADDRESSES` 末尾 2 个伪造地址已删**（Base L1 Bridge、LayerZero Endpoint，均以 `7c7c` 重复填充结尾），原在 `modules/eth/eth_analyzer.py` BRIDGE_ADDRESSES 末尾。
   - 此前 Edit 因"行尾不可见空白"连续失败；复查发现已无尾空白，Edit 一次成功。
   - 已用 Etherscan 核验真地址：Base L1StandardBridgeProxy `0x3154Cf16ccdb4C6d922629664174b904d80F2C35`、LayerZero Endpoint V1 `0x66a71dcef29a0ffbdbe3c6a460a3b5bc225cd675`。文件中假地址仅前缀与真地址相同、尾部为 `7c7c` 重复填充，确认伪造。
   - **删除（非替换）**，与此前 7 个假地址处理一致。现 BRIDGE_ADDRESSES 共 13 条，无 `7c7c` 残留，import OK。

2. ✅ **README「模板归类」说明已做**（框架④）：README 加「工具类型说明」blockquote（区分「跨境协查/资产追回」模板生成工具 vs 其余链上分析工具）；侧边栏两链接加「（模板）」后缀。

**验证**：全模块 + `app` import OK；杀 2 个 stale app.py 后重启 dev server，8 页面 HTTP 200，侧边栏 marker=2。

## Resume Instructions
1-2. 已完成（遗留 1、2 均清零，见上）。
3. （可选）若用户要更深，做选项 B：TRON/ETH 2-3 跳资金流向 BFS（需注意 Etherscan/Tronscan 免费额度）。
4. 不要做的事：Tornado merkle 去匿名、BTC co-spend 聚类、动前端 Anduril 样式。
5. dev server 当前后台运行（python app.py，端口 5000，任务 bgp0q17we）；如不需要可停。

## Key Files Modified
- `modules/tron/suspicious_analyzer.py`
- `modules/case/monitor.py`、`templates/case/monitor.html`
- `modules/core/api_client.py`
- `modules/cross/cluster_analyzer.py`
- `modules/trace/mixer_tracker.py`、`modules/trace/tornado_pools.py`
- `modules/case/obfuscation_detector.py`
- `modules/trace/uniswap_tracker.py`
- `modules/eth/eth_analyzer.py`、`modules/eth/routes.py`
