# PROJECT: Crypto Investigation Toolkit (CIT)

**Code:** CIT
**Title:** 虚拟币犯罪调查工具集
**Started:** 2026-04-23
**Status:** Active

---

## What This Is

为虚拟货币犯罪调查初学者构建一个本地运行的Web工具集，整合11个链上分析工具，提供统一的操作界面和用户手册。

**Core Value:** 一键本地启动，零配置使用。初学者无需理解Python代码，通过Web界面完成链上分析，配合说明书理解结果含义。

---

## Target Users

- 链上调查初学者 — 主要用户群
- 金融机构合规调查人员
- 内部审计调查团队

---

## Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| Backend | Flask + Python | 直接复用现有Python脚本，学习成本低 |
| Frontend | 原生 HTML + Tailwind CSS | 简单直观，初学者可维护 |
| Deployment | 本地运行 | 保密需求，无需服务器 |
| Data Export | JSON/CSV/PDF | 证据保全，不持久存储 |

---

## Constraints

- **本地运行优先** — 数据保密，无需外部服务器
- **零代码使用** — 用户无需接触Python代码
- **API密钥自行获取** — 工具不内置密钥，用户需从官方API获取
- **不持久化数据** — 所有分析结果导出，不留存本地

---

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **CORE-01**: Flask应用核心框架（app.py, base.html, 侧边栏）
- [ ] **CORE-02**: 共享模块（api_client, formatter, exporter）
- [ ] **ADDR-01**: TRON可疑特征分析工具
- [ ] **ADDR-02**: TRON地址行为分析工具
- [ ] **ADDR-03**: ETH交易查询工具（含跨链桥识别）
- [ ] **TRACE-01**: Uniswap追踪工具
- [ ] **TRACE-02**: 混币器追踪工具
- [ ] **TRACE-03**: BTC交易分析工具
- [ ] **CROSS-01**: 地址聚类工具
- [ ] **CROSS-02**: 跨境协查工具
- [ ] **CASE-01**: 多链监控工具
- [ ] **CASE-02**: 混淆攻击对抗工具
- [ ] **CASE-03**: 资产追回冻结工具
- [ ] **DOC-01**: 用户手册（11个工具说明书）
- [ ] **DOC-02**: API获取指南（Tronscan/Etherscan/Blockchain）

### Out of Scope

- 实时数据持久化 — 保密需求，不留存数据
- 云端部署 — 本地运行优先
- 多用户权限系统 — 单用户本地工具
- 情景故事培训内容 — 仅工具说明，无情景

---

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Flask单应用结构 | 直接复用现有Python脚本，学习成本低 | Pending |
| Tailwind CSS CDN | 无需构建，简单直观 | Pending |
| 样本数据填充按钮 | 帮助初学者理解输入格式 | Pending |

---

## Context

This project converts existing Python training scripts (001-day1, 002-day1, etc.) into a unified Web interface for cryptocurrency investigation beginners. The goal is "one-click local startup, zero-config usage."

---

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-23 after initialization*