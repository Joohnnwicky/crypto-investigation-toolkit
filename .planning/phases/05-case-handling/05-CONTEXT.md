# Phase 5: Case Handling Tools - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

完成三个案件处理工具：多链监控工具、混淆攻击对抗工具、资产追回冻结工具。构建本地化监控、攻击检测、冻结模板生成能力，复用Phase 1-4的核心框架和API模块。

**In scope:**
- 多链监控工具（多地址输入，手动刷新，状态卡片展示）
- 混淆攻击对抗工具（4种攻击类型检测，规则匹配逻辑）
- 资产追回冻结工具（分步表单，标准冻结申请模板）
- TRON + ETH + BTC 三链支持（监控）
- ETH链攻击检测（混淆攻击）
- ETH API密钥统一输入（每次查询输入，不存储）
- 样本填充按钮
- JSON/CSV导出功能（监控、攻击检测）
- 文本复制导出（资产追回模板）
- 工具间联动（监控→地址分析/聚类/资产追回，攻击检测→ETH查询/资产追回）

**Out of scope:**
- 用户认证系统
- 数据持久化存储
- 云端部署
- 实时后台监控（无后台服务，仅手动刷新）
- TRON/BTC链攻击检测（仅ETH）
- 多辖区冻结模板（仅标准模板）
- PDF导出（Phase 6实现）
- 机器学习攻击检测模型

</domain>

<decisions>
## Implementation Decisions

### 多链监控工具 - 触发机制
- **D-01:** 监控触发机制为手动刷新（用户点击刷新按钮查询各链API，不自动轮询）
- **D-02:** 本地工具无后台服务，"实时监控"定义为手动刷新状态查询
- **D-03:** 不设置定时轮询，避免API限流和资源消耗问题

### 多链监控工具 - 输入设计
- **D-04:** 地址输入为文本域（多行输入框），每行一个地址，最多10个地址
- **D-05:** 支持TRON + ETH + BTC三链地址监控，系统自动检测链类型
- **D-06:** ETH监控需要用户输入API密钥（统一输入框，所有ETH地址共用）
- **D-07:** TRON/BTC使用免费API（Tronscan/Blockstream），无需密钥
- **D-08:** 提供样本填充按钮，帮助初学者理解输入格式

### 多链监控工具 - 结果展示
- **D-09:** 状态采用卡片形式展示（每个地址一个状态卡片）
- **D-10:** 每个状态卡片显示：当前余额、最近交易数、最后活跃时间
- **D-11:** 每次刷新更新所有地址的状态卡片
- **D-12:** 支持JSON/CSV导出监控结果

### 混淆攻击对抗工具 - 攻击类型
- **D-13:** 识别4种混淆攻击类型：Sandwich攻击、闪电贷攻击、粉尘攻击、协议漏洞攻击
- **D-14:** Sandwich攻击：DEX三明治攻击，大户在用户交易前后插入交易操纵价格
- **D-15:** 闪电贷攻击：利用闪电贷借出大量资金，操纵市场后瞬间还款
- **D-16:** 粉尘攻击：向大量地址发送微量代币，用于追踪地址关联
- **D-17:** 协议漏洞攻击：利用协议设计缺陷盗取资金（重入攻击、价格操纵等）

### 混淆攻击对抗工具 - 检测逻辑
- **D-18:** 检测逻辑采用规则匹配方法（已知攻击特征规则匹配）
- **D-19:** 闪电贷特征：单笔交易内借贷和还款
- **D-20:** Sandwich特征：同一区块内前后交易价格操纵
- **D-21:** 粉尘特征：向大量地址发送微量代币
- **D-22:** 协议漏洞特征：异常合约调用模式

### 混淆攻击对抗工具 - 输入与范围
- **D-23:** 输入方式为地址输入（查询该地址的最近交易并检测攻击痕迹）
- **D-24:** 仅检测ETH链上的攻击（Uniswap等DEX攻击）
- **D-25:** ETH分析需要用户输入API密钥（每次查询输入，不存储）
- **D-26:** 提供样本填充按钮，帮助初学者理解输入格式

### 混淆攻击对抗工具 - 结果展示
- **D-27:** 结果采用攻击卡片形式展示（每种攻击类型一个卡片）
- **D-28:** 每个攻击卡片显示：攻击类型、攻击详情、置信度（HIGH/MEDIUM/LOW）、影响地址
- **D-29:** 未检测到攻击时显示"未发现攻击痕迹"
- **D-30:** 支持JSON/CSV导出检测结果

### 资产追回冻结工具 - 模板定位
- **D-31:** 资产追回为独立模板（与跨境协查不同定位）
- **D-32:** 跨境协查是国际协作请求模板，资产追回是冻结申请模板
- **D-33:** 内容和字段设计独立，不依赖跨境协查模板

### 资产追回冻结工具 - 模板字段
- **D-34:** 模板字段包含4类：案件基本信息、冻结对象信息、冻结理由说明、冻结条款
- **D-35:** 案件基本信息：案件编号、调查机构、联系人、联系方式
- **D-36:** 冻结对象信息：涉案地址列表、链类型、冻结金额、资产类型
- **D-37:** 冻结理由说明：可疑行为描述、资金来源说明、冻结必要性、法律依据
- **D-38:** 冻结条款：冻结期限、解除冻结条件、联系人、后续处理

### 资产追回冻结工具 - 输入与输出
- **D-39:** 输入流程为分步表单（案件信息 → 地址选择 → 模板生成）
- **D-40:** 输出格式为文本复制（HTML页面显示，用户复制文本导出）
- **D-41:** 使用标准模板（单一格式），不提供多辖区模板
- **D-42:** PDF导出功能在Phase 6实现

### 工具间联动 - 监控导出
- **D-43:** 多链监控结果可导出到TRON/ETH地址分析工具
- **D-44:** 多链监控结果可导出到地址聚类工具
- **D-45:** 多链监控结果可导出到资产追回冻结工具
- **D-46:** 多链监控结果可导出为JSON/CSV文件

### 工具间联动 - 资产追回导入
- **D-47:** 资产追回可从多链监控结果导入地址列表
- **D-48:** 资产追回可从地址聚类结果导入地址列表
- **D-49:** 资产追回支持手动输入地址

### 工具间联动 - 混淆检测导出
- **D-50:** 混淆攻击检测结果可导出到ETH交易查询工具
- **D-51:** 混淆攻击检测结果可导出到资产追回冻结工具
- **D-52:** 混淆攻击检测结果可导出为JSON/CSV文件

### Claude's Discretion
- 具体攻击检测规则实现细节（闪电贷/Sandwich/粉尘/漏洞特征编码）
- API调用超时和重试逻辑
- 状态卡片具体样式设计
- 分步表单UI细节
- 联动导出按钮位置和交互细节
- 错误处理和Loading状态展示

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §CASE-01, CASE-02, CASE-03 — 案件处理工具需求定义

### Existing Patterns (reference from Phase 1-4)
- `modules/core/api_client.py` — Tronscan API client（TRON地址查询）
- `modules/core/eth_rpc_client.py` — ETH RPC client（ETH地址查询）
- `modules/trace/btc_analyzer.py` — BTC analyzer（BTC地址查询）
- `modules/trace/mixer_tracker.py` — 混币追踪（置信度评分模式参考）
- `modules/cross/cluster_analyzer.py` — 地址聚类（多地址输入模式参考）
- `modules/cross/cross_border_generator.py` — 跨境协查模板（分步表单模式参考）
- `modules/core/exporter.py` — JSON/CSV导出功能
- `templates/base.html` — 基础模板（侧边栏、底部声明）

### External APIs
- Tronscan API — https://api.tronscan.org/api（TRON地址查询，免费）
- Etherscan API V2 — https://api.etherscan.io/v2/api（ETH地址查询，需密钥）
- Blockstream API — https://blockstream.info/api（BTC地址查询，免费）

### Attack Detection References
- Sandwich Attack Detection — https://ethereum.stackexchange.com/（技术参考）
- Flash Loan Attack Patterns — DeFi安全审计报告参考
- Dusting Attack Detection — 区块链分析工具特征参考

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/core/api_client.py` — Tronscan API client，可用于TRON监控
- `modules/core/eth_rpc_client.py` — ETH RPC client，可用于ETH监控和攻击检测
- `modules/trace/btc_analyzer.py` — BTC analyzer，可用于BTC监控
- `modules/cross/cluster_analyzer.py` — 多地址输入模式，可复用于监控输入
- `modules/cross/cross_border_generator.py` — 分步表单模式，可复用于资产追回
- `modules/trace/mixer_tracker.py` — 置信度评分模式，可复用于攻击检测结果
- `modules/core/exporter.py` — JSON/CSV导出功能
- `templates/base.html` — 基础模板（侧边栏已配置Case工具入口）

### Established Patterns
- Flask Blueprint modular architecture — 每个工具类别一个模块
- Analysis pattern: structured result dict (success, addresses, results/cards)
- Multi-address input: 文本域输入，每行一个地址
- Step-by-step form: 分步表单输入（案件信息 → 地址选择 → 模板生成）
- Confidence scoring: HIGH/MEDIUM/LOW 置信度评分
- Card-based result display: 每个结果一个卡片
- API密钥输入: 统一输入框（每次查询输入，不存储）
- Sample filling button: 每个输入框旁提供样本数据按钮

### Integration Points
- `app.py` — 需注册新的case blueprint
- `templates/case/` — 新建案件工具页面目录（monitor.html, obfuscation.html, asset_freeze.html）
- `modules/case/` — 新建案件模块目录（routes.py, monitor.py, obfuscation_detector.py, asset_freeze_generator.py）

### Sidebar Already Configured
- `/case/monitor` → 多链监控
- `/case/obfuscation` → 混淆对抗
- `/case/asset-freeze` → 资产追回

</code_context>

<specifics>
## Specific Ideas

- 多链监控状态卡片应该清晰显示每条链的余额和交易数
- 混淆攻击检测结果应该标注攻击类型和置信度（颜色区分）
- 资产追回模板应该简洁实用，便于初学者复制使用
- 工具间联动按钮应该放在结果卡片底部（"导出到XXX"按钮）
- 所有工具界面保持简洁，与现有工具风格一致

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 05-case-handling*
*Context gathered: 2026-04-24*