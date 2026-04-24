# Phase 4: Cross-Chain Analysis Tools - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-24
**Phase:** 04-cross-chain-analysis
**Areas discussed:** 地址聚类输入与聚类逻辑, 地址聚类结果展示, 跨境协查模板内容, 跨境协查工具流程

---

## 地址聚类输入与聚类逻辑

### 输入方式

| Option | Description | Selected |
|--------|-------------|----------|
| 文本域（多行输入框） | 简单直观，适合初学者，每行一个地址，最多10个 | ✓ |
| 多个单独输入框（动态添加） | 更灵活，但界面复杂，初学者可能困惑 | |

**User's choice:** 文本域（多行输入框）
**Notes:** Recommended option selected

---

### 支持链

| Option | Description | Selected |
|--------|-------------|----------|
| 仅 TRON | TRON API免费可用，适合初学者 | |
| TRON + ETH | 复用ETH API client，但需要用户输入Etherscan密钥 | |
| TRON + ETH + BTC | BTC需要Blockstream API，增加复杂性 | ✓ |

**User's choice:** TRON + ETH + BTC
**Notes:** 选择三链支持，复用现有API clients

---

### 聚类依据

| Option | Description | Selected |
|--------|-------------|----------|
| 首次资金来源相同 | 追踪所有地址的首次入账来源，相同来源的地址聚类 | ✓ |
| 频繁互转账 | 检查地址之间的直接转账频率，频繁交互的地址聚类 | ✓ |
| 时间窗口关联 | 分析地址活动时间重叠度，同一时间段活跃的地址可能关联 | ✓ |
| 共享存款地址 | 识别地址是否使用相同的存款地址（如交易所或平台地址） | ✓ |

**User's choice:** 全选（首次资金来源、频繁互转账、时间窗口关联、共享存款地址）
**Notes:** 四个聚类依据全部启用

---

### API密钥

| Option | Description | Selected |
|--------|-------------|----------|
| ETH/BTC需要密钥输入 | TRON免费，ETH/BTC需要密钥（每个查询时输入） | ✓ |
| 仅使用免费API（TRON） | 仅分析TRON地址，不支持ETH/BTC | |

**User's choice:** ETH/BTC需要密钥输入
**Notes:** 与Phase 2 ETH工具一致，密钥每次输入不存储

---

### 地址数量限制

| Option | Description | Selected |
|--------|-------------|----------|
| 最多10个 | 限制为最多10个地址，避免API调用过多 | ✓ |
| 最多20个 | 最多20个地址，但可能增加等待时间 | |
| 不限制（显示警告） | 不限制数量，但警告用户可能较慢 | |

**User's choice:** 最多10个
**Notes:** Recommended option selected

---

## 地址聚类结果展示

### 结果形式

| Option | Description | Selected |
|--------|-------------|----------|
| 分组卡片（Cluster Cards） | 按聚类分组显示，每组显示地址列表和关联原因，符合现有 Card 风格 | ✓ |
| 表格形式 | 表格显示地址和关联信息，更紧凑但不直观 | |
| 可视化图表（Graph） | 可视化网络图，展示地址关系，但对初学者可能复杂 | |

**User's choice:** 分组卡片（Cluster Cards）
**Notes:** 与现有工具UI风格一致

---

### 每个聚类显示信息

| Option | Description | Selected |
|--------|-------------|----------|
| 关联类型和原因 | 标注每个聚类的核心原因（如"首次资金来源相同: TXxx..."） | ✓ |
| 交易统计 | 显示聚类内地址的总交易额和互转账次数 | ✓ |
| 时间窗口信息 | 显示地址活动时间重叠度 | ✓ |
| 共享地址信息 | 显示聚类内共同的存款/交易所地址 | ✓ |

**User's choice:** 全选（关联类型和原因、交易统计、时间窗口信息、共享地址信息）
**Notes:** 四类信息全部显示

---

### 未关联地址处理

| Option | Description | Selected |
|--------|-------------|----------|
| 单独显示 | 显示未聚类的地址列表，注明"无关联" | ✓ |
| 不显示 | 不显示未关联地址，仅显示聚类结果 | |

**User's choice:** 单独显示
**Notes:** Recommended option selected

---

## 跨境协查模板内容

### 模板格式

| Option | Description | Selected |
|--------|-------------|----------|
| HTML页面 + 文本导出 | 浏览器直接显示模板，用户可复制文本或导出PDF，简单直观 | ✓ |
| DOCX文档生成 | 生成标准Word格式，用户可直接下载，但需额外库支持 | |
| 纯文本 | 仅生成纯文本，用户复制使用 | |

**User's choice:** HTML页面 + 文本导出
**Notes:** Recommended option selected，简单直观

---

### 模板字段

| Option | Description | Selected |
|--------|-------------|----------|
| 案件基本信息 | 案件编号、调查机构、联系人、联系方式 | ✓ |
| 涉案地址与交易信息 | 涉案地址列表、链类型、金额汇总、交易哈希 | ✓ |
| 调查背景说明 | 可疑行为描述、资金流向简述、调查背景 | ✓ |
| 协查请求内容 | 请求类型（信息查询、资产冻结等）、期望回复时间 | ✓ |

**User's choice:** 全选（案件基本信息、涉案地址与交易信息、调查背景说明、协查请求内容）
**Notes:** 四类字段全部包含

---

### 导出功能

| Option | Description | Selected |
|--------|-------------|----------|
| 页面显示 + 文本复制 | HTML页面可复制文本，用户自行导出 | ✓ |
| PDF导出 | 生成标准PDF文件，可下载保存 | |

**User's choice:** 页面显示 + 文本复制
**Notes:** Recommended option selected

---

## 跨境协查工具流程

### 输入流程

| Option | Description | Selected |
|--------|-------------|----------|
| 分步表单输入 | 用户填写案件信息，然后选择地址（可从聚类结果导入），最后生成模板 | ✓ |
| 单一表单 | 一个大表单，用户填写所有信息后一次性生成 | |

**User's choice:** 分步表单输入
**Notes:** Recommended option selected

---

### 与聚类关联

| Option | Description | Selected |
|--------|-------------|----------|
| 支持从聚类结果导入 | 聚类结果页面提供"导出到跨境协查"按钮，直接导入地址列表 | ✓ |
| 不关联 | 跨境协查工具单独使用，不与聚类关联 | |

**User's choice:** 支持从聚类结果导入
**Notes:** Recommended option selected，实现工具联动

---

### 模板类型

| Option | Description | Selected |
|--------|-------------|----------|
| 标准模板（单一格式） | 使用标准模板，用户填写字段即可，简单直观 | ✓ |
| 多辖区模板（需选择目标地区） | 根据目标管辖区选择模板格式（如香港、新加坡、美国等） | |

**User's choice:** 标准模板（单一格式）
**Notes:** Recommended option selected

---

## Claude's Discretion

- TRON/ETH/BTC API调用具体实现细节
- 聚类阈值设定（频繁互转账次数阈值、时间窗口重叠度阈值）
- 错误处理和重试逻辑
- Loading状态展示细节
- HTML模板具体样式设计

---

## Deferred Ideas

None — discussion stayed within phase scope.

---

*Phase: 04-cross-chain-analysis*
*Discussion log generated: 2026-04-24*