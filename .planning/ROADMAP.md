# ROADMAP: Crypto Investigation Toolkit

**Project:** CIT
**Updated:** 2026-04-24
**Status:** Active

---

## Progress

| Milestone | Status | Phases | Progress |
|-----------|--------|--------|----------|
| v1 | ◆ Active | 0/6 | 0% |

---

## Phases

### Phase 1: Core Framework
**Goal:** 构建Flask应用核心框架，包含基础模板、侧边栏导航、共享模块，以及第一个完整工具（TRON可疑特征分析）

**Status:** ✅ Complete
**Requirements:** CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, ADDR-01, ADDR-02, EXPORT-01, EXPORT-02
**Plans:** 7 plans in 4 waves

**Success Criteria:**
- [x] run.bat双击可启动Flask应用
- [x] 首页显示工具概览和4个分组
- [x] 侧边栏导航正常切换
- [x] TRON可疑分析工具完整可用（样本填充、API调用、结果展示、导出）
- [x] 底部法律声明显示

**Key Files:**
- app.py (Flask入口)
- templates/base.html (侧边栏布局)
- modules/core/ (共享模块)
- modules/tron/suspicious_analyzer.py (TRON分析)

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 01-01-PLAN.md | Base template with sidebar + footer | CORE-03, CORE-05 | DONE |
| 1 | [x] 01-02-PLAN.md | Core modules (API client, formatter, exporter) | EXPORT-01, EXPORT-02 | DONE |
| 2 | [x] 01-03-PLAN.md | Flask app + homepage with 4 categories | CORE-02 | DONE |
| 2 | [x] 01-04-PLAN.md | TRON analyzer backend (alerts + score) | ADDR-01, ADDR-02 | DONE |
| 3 | [x] 01-05-PLAN.md | TRON frontend page + sample loading | CORE-04 | DONE |
| 3 | [x] 01-06-PLAN.md | Startup scripts (run.bat/run.sh) | CORE-01 | DONE |
| 4 | [x] 01-07-PLAN.md | Final verification + integration | Verification only | DONE |

---

### Phase 2: Address Analysis Tools
**Goal:** 完成TRON地址行为分析和ETH交易查询工具（含跨链桥识别）

**Status:** ○ Pending
**Requirements:** ADDR-03, ADDR-04, ADDR-05
**Plans:** 4 plans in 3 waves

**Success Criteria:**
- [ ] TRON地址行为分析工具完整可用
- [ ] ETH交易查询工具可查询全部交易
- [ ] ETH工具可识别跨链桥（Stargate）事件
- [ ] ETH工具支持API密钥输入

**Dependencies:** Phase 1 complete

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [ ] 02-01-PLAN.md | TRON behavior analyzer backend + frontend | ADDR-03 | Pending |
| 1 | [ ] 02-02-PLAN.md | ETH backend module (API + Stargate detector) | ADDR-04, ADDR-05 | Pending |
| 2 | [ ] 02-03-PLAN.md | ETH frontend UI with API key input | ADDR-04, ADDR-05 | Pending |
| 3 | [ ] 02-04-PLAN.md | Integration + end-to-end verification | ADDR-03, ADDR-04, ADDR-05 | Pending |

---

### Phase 3: Transaction Tracking Tools
**Goal:** 完成Uniswap追踪、混币器追踪、BTC交易分析工具

**Status:** ○ Pending
**Requirements:** TRACE-01, TRACE-02, TRACE-03
**Plans:** 3

**Success Criteria:**
- [ ] Uniswap追踪可还原DEX交易路径
- [ ] 混币器追踪可还原洗钱路径
- [ ] BTC交易分析可查询比特币流向

**Dependencies:** Phase 2 complete

---

### Phase 4: Cross-Chain Analysis Tools
**Goal:** 完成地址聚类和跨境协查工具

**Status:** ○ Pending
**Requirements:** CROSS-01, CROSS-02
**Plans:** 2

**Success Criteria:**
- [ ] 地址聚类可关联多个地址
- [ ] 跨境协查可生成国际协作模板

**Dependencies:** Phase 3 complete

---

### Phase 5: Case Handling Tools
**Goal:** 完成多链监控、混淆攻击对抗、资产追回冻结工具

**Status:** ○ Pending
**Requirements:** CASE-01, CASE-02, CASE-03
**Plans:** 3

**Success Criteria:**
- [ ] 多链监控可实时监控地址
- [ ] 混淆对抗可识别攻击手法
- [ ] 资产追回可生成冻结建议

**Dependencies:** Phase 4 complete

---

### Phase 6: Documentation & Export
**Goal:** 完善导出功能和用户手册

**Status:** ○ Pending
**Requirements:** EXPORT-03, DOC-01, DOC-02
**Plans:** 4

**Success Criteria:**
- [ ] PDF导出功能完整可用
- [ ] 11个工具有完整说明书
- [ ] API获取指南（Tronscan、Etherscan、Blockchain）完整

**Dependencies:** Phase 5 complete

---

## Coverage

- Total v1 Requirements: 22
- Mapped to Phases: 22
- Coverage: 100% ✓

## Requirements Traceability

| Phase 1 Plans | Requirements Covered |
|---------------|---------------------|
| 01-01-PLAN.md | CORE-03, CORE-05 |
| 01-02-PLAN.md | EXPORT-01, EXPORT-02 |
| 01-03-PLAN.md | CORE-02 |
| 01-04-PLAN.md | ADDR-01, ADDR-02 |
| 01-05-PLAN.md | CORE-04 |
| 01-06-PLAN.md | CORE-01 |

**Phase 1 Coverage:** 9/9 requirements ✓

| Phase 2 Plans | Requirements Covered |
|---------------|---------------------|
| 02-01-PLAN.md | ADDR-03 |
| 02-02-PLAN.md | ADDR-04, ADDR-05 |
| 02-03-PLAN.md | ADDR-04, ADDR-05 |
| 02-04-PLAN.md | ADDR-03, ADDR-04, ADDR-05 |

**Phase 2 Coverage:** 3/3 requirements ✓

---

*Updated: 2026-04-24 after Phase 2 plan creation*