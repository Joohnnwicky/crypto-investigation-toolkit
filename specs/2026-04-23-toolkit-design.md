# 虚拟币犯罪调查工具集 - 设计文档

**日期:** 2026-04-23
**状态:** 已批准
**作者:** Claude (brainstorming)

---

## 项目概述

为虚拟货币犯罪调查初学者构建一个本地运行的Web工具集，整合11个链上分析工具，提供统一的操作界面和用户手册。

### 目标用户

- 链上调查初学者
- 金融机构合规调查人员
- 内部审计调查团队

### 核心价值

**一键本地启动，零配置使用。** 初学者无需理解Python代码，通过Web界面完成链上分析，配合说明书理解结果含义。

---

## 技术栈

| 层级 | 技术 | 选择理由 |
|------|------|----------|
| 后端 | Flask + Python | 直接复用现有Python脚本，学习成本低 |
| 前端 | 原生 HTML + Tailwind CSS | 简单直观，初学者可维护 |
| 部署 | 本地运行 | 保密需求，无需服务器 |
| 数据 | 导出JSON/CSV/PDF | 证据保全，不持久存储 |

---

## 文件结构

```
虚拟币犯罪调查工具集/
├── app.py                  # Flask主应用入口
├── config.py               # 配置管理（API密钥模板）
├── requirements.txt        # Python依赖列表
├── run.bat                 # Windows一键启动脚本
├── run.sh                  # Linux/Mac启动脚本
├── static/
│   ├── css/
│   │   ├── tailwind.min.css    # Tailwind CSS
│   │   └── custom.css          # 自定义样式
│   ├── js/
│   │   ├── main.js             # 主交互逻辑
│   │   ├── sidebar.js          # 侧边栏导航
│   │   └── exporter.js         # 导出功能
│   └── assets/
│   │   ├── icons/              # 工具图标
│   │   └── logo.png            # 工具集logo
├── templates/
│   ├── base.html           # 基础模板（侧边栏布局）
│   ├── index.html          # 首页（工具概览）
│   └── tools/
│   │   ├── tron-suspicious.html    # TRON可疑特征分析
│   │   ├── tron-behavior.html      # TRON行为分析
│   │   ├── eth-transactions.html   # ETH交易查询
│   │   ├── uniswap-trace.html      # Uniswap追踪
│   │   ├── mixer-trace.html        # 混币器追踪
│   │   ├── btc-tx.html             # BTC交易分析
│   │   ├── btc-clustering.html     # 地址聚类
│   │   ├── cross-border.html       # 跨境协查
│   │   ├── multi-chain.html        # 多链监控
│   │   ├── obfuscation.html        # 混淆攻击对抗
│   │   └── recovery.html           # 资产追回冻结
├── modules/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── api_client.py   # API调用基类
│   │   ├── formatter.py    # 输出格式化
│   │   ├── exporter.py     # 导出功能
│   │   └── error_handler.py
│   ├── tron/
│   │   ├── __init__.py
│   │   ├── suspicious_analyzer.py   # TRON可疑特征分析
│   │   └── behavior_analyzer.py     # TRON地址行为分析
│   ├── eth/
│   │   ├── __init__.py
│   │   ├── tx_analyzer.py           # ETH交易查询（含跨链桥识别）
│   │   └── stargate_parser.py       # Stargate事件解析
│   ├── btc/
│   │   ├── __init__.py
│   │   ├── tx_analyzer.py       # BTC交易分析
│   │   └── clustering.py        # 地址聚类
│   ├── defi/
│   │   ├── __init__.py
│   │   ├── uniswap_tracer.py    # Uniswap追踪
│   │   └── mixer_tracer.py      # 混币器追踪
│   ├── monitor/
│   │   ├── __init__.py
│   │   ├── multi_chain.py       # 多链监控
│   │   └── obfuscation.py       # 混淆攻击对抗
│   └── recovery/
│   │   ├── __init__.py
│   │   ├── freeze.py            # 资产冻结建议
│   │   └── cross_border.py      # 跨境协查
├── docs/
│   ├── README.md           # 工具集总说明
│   ├── tools/              # 各工具说明书（11个）
│   └── api-guide/          # API获取指南
└── .planning/              # GSD规划文档
```

---

## 工具分组

### 侧边栏结构（修正版 - 对应11个Python脚本）

```
┌─────────────────────┐
│ 🔍 地址分析         │  (3个工具)
├─────────────────────┤
│ • TRON地址可疑分析  │  检测可疑特征、评分
│ • TRON地址行为分析  │  行为模式、资金流向
│ • ETH交易查询       │  全部交易+跨链桥识别
├─────────────────────┤
│ 💸 交易追踪         │  (3个工具)
├─────────────────────┤
│ • Uniswap追踪       │  DEX交易路径
│ • 混币器追踪        │  洗钱路径还原
│ • BTC交易分析       │  比特币流向
├─────────────────────┤
│ 🔗 跨链分析         │  (2个工具)
├─────────────────────┤
│ • 地址聚类          │  多地址关联分析
│ • 跨境协查          │  国际协作模板
├─────────────────────┤
│ 🛡️ 案件处理         │  (3个工具)
├─────────────────────┤
│ • 多链监控          │  实时地址监控
│ • 混淆攻击对抗      │  对抗手法识别
│ • 资产追回冻结      │  冻结流程建议
└─────────────────────┘
```

**说明：ETH交易查询工具已包含跨链桥识别功能，不单独列出。**

### 工具映射表（修正版 - 精确对应11个脚本）

| 工具名称 | 原脚本 | API端点 | 输入参数 |
|----------|--------|---------|----------|
| TRON地址可疑分析 | 001-day1-TRON地址可疑特征分析工具.py | /api/v1/tron/address | address |
| TRON地址行为分析 | 001-day2-分析地址行为特征.py | /api/v1/tron/behavior | address |
| ETH交易查询 | 002-day1-查询以太坊地址的所有交易.py | /api/v1/eth/transactions | address, api_key |
| 混币器追踪 | 002-day2-完整混币追踪流程.py | /api/v1/defi/mixer-trace | address, tx_hash |
| Uniswap追踪 | 002-day3-Uniswap 交易追踪器.py | /api/v1/defi/uniswap-trace | address, tx_hash |
| BTC交易分析 | 004-day1-比特币交易分析.py | /api/v1/btc/address | address, api_key |
| 地址聚类 | 004-day2-地址聚类.py | /api/v1/btc/clustering | addresses (多个) |
| 跨境协查 | 004-day3-跨境协查.py | /api/v1/recovery/cross-border | address, country |
| 多链监控 | 005-day1-多链实时监控系统.py | /api/v1/monitor/multi-chain | addresses, chains |
| 混淆对抗 | 005-day2-混淆攻击手法对抗.py | /api/v1/monitor/obfuscation | address, tx_hash |
| 资产追回 | 005-day3-资产追回与冻结.py | /api/v1/recovery/freeze | address, amount |

---

## API设计

### 请求格式

所有API遵循统一格式：

```json
POST /api/v1/{module}/{action}
{
  "address": "TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw",
  "api_key": "用户自行输入",
  "tx_hash": "可选，部分工具需要",
  "options": {
    "limit": 50,
    "chain": "tron"
  }
}
```

### 响应格式

```json
{
  "status": "success",
  "data": {
    "address": "...",
    "balance": { ... },
    "transactions": [ ... ],
    "alerts": {
      "red": [ ... ],
      "yellow": [ ... ],
      "green": [ ... ]
    },
    "score": 90
  },
  "metadata": {
    "query_time": "2026-04-23T10:30:00Z",
    "source": "Tronscan API"
  }
}
```

### 导出端点

```
POST /api/v1/export/json   → 返回JSON文件下载
POST /api/v1/export/csv    → 返回CSV文件下载
POST /api/v1/export/pdf    → 返回PDF文件下载
```

---

## 前端界面

### 页面布局

```
┌────────────────────────────────────────────────────┐
│  📊 虚拟币犯罪调查工具集         [使用手册] [导出]  │
├──────────────┬─────────────────────────────────────┤
│              │                                     │
│  侧边栏      │           工具工作区               │
│  (固定)      │                                     │
│              │  ┌─────────────────────────────────┐ │
│  4个分组     │  │ 工具标题 + 简介                 │ │
│  11个工具    │  ├─────────────────────────────────┤ │
│              │  │ 输入参数区                      │ │
│              │  │ - API密钥输入框 + 样本填充按钮  │ │
│              │  │ - 地址/交易哈希输入框          │ │
│              │  │ - 开始分析按钮                  │ │
│              │  ├─────────────────────────────────┤ │
│              │  │ 分析结果区                      │ │
│              │  │ - 可疑特征列表 (红/黄/绿)      │ │
│              │  │ - 风险评分                      │ │
│              │  │ - 导出按钮区                    │ │
│              │  └─────────────────────────────────┘ │
│              │                                     │
└──────────────┴─────────────────────────────────────┤
│  ⚠️ 本工具仅供合法调查使用，请遵守相关法律法规     │
└────────────────────────────────────────────────────┘
```

### 交互流程

1. 用户点击侧边栏工具名称
2. 右侧加载工具页面（输入表单）
3. 用户输入参数（可点击"样本填充"查看示例）
4. 点击"开始分析"
5. 显示加载状态
6. 结果区域展示分析结果
7. 用户可导出结果（JSON/CSV/PDF）

### 样本数据

每个工具提供样本数据按钮，点击后自动填充：

| 工具 | 样本地址 | 样本API提示 |
|------|----------|-------------|
| TRON地址分析 | TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw | "从tronscan.org获取" |
| ETH地址查询 | 0x71C7656EC7ab88b098defB751B7401B5f6d8976F | "从etherscan.io/apis获取" |
| BTC交易分析 | bc1qar0srrr7xfkvy5l643lydnw9re59gt... | "从blockchain.com/api获取" |

---

## 用户手册

### 手册结构

```
docs/
├── README.md               # 总说明
│   ├── 1. 安装与启动
│   ├── 2. API密钥获取指南
│   ├── 3. 法律合规声明
│   ├── 4. 快速入门（5分钟教程）
│   └── 5. 工具概览表格
│
├── tools/                  # 11个工具说明书
│   ├── tron-suspicious.md      # TRON可疑特征分析
│   ├── tron-behavior.md        # TRON地址行为分析
│   ├── eth-transactions.md     # ETH交易查询（含跨链桥）
│   ├── uniswap-trace.md        # Uniswap追踪
│   ├── mixer-trace.md          # 混币器追踪
│   ├── btc-tx.md               # BTC交易分析
│   ├── btc-clustering.md       # 地址聚类
│   ├── cross-border.md         # 跨境协查
│   ├── multi-chain.md          # 多链监控
│   ├── obfuscation.md          # 混淆攻击对抗
│   └── recovery.md             # 资产追回冻结
│
└── api-guide/              # API注册指南
│   ├── tronscan-api.md     # Tronscan注册步骤
│   ├── etherscan-api.md    # Etherscan注册步骤
│   └── blockchain-api.md   # Blockchain.com注册步骤
```

### 每个工具说明书内容

1. **功能概述** - 这个工具做什么
2. **输入参数** - 需要填什么（附样本）
3. **输出解读** - 结果怎么看（红/黄/绿含义）
4. **应用场景** - 什么时候用（案件类型）
5. **注意事项** - API限制、数据准确性

---

## 核心模块设计

### api_client.py（共享API基类）

```python
class BaseAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.timeout = 10
        self.headers = {"User-Agent": "..."}

    def get(self, url: str, params: dict) -> dict:
        # 统一GET请求处理
        # 错误处理、重试逻辑

    def validate_response(self, data: dict) -> bool:
        # 验证API返回有效性
```

### formatter.py（输出格式化）

```python
class OutputFormatter:
    def format_address_info(self, data: dict) -> dict:
        # 格式化地址基本信息

    def format_alerts(self, alerts: dict) -> list:
        # 格式化可疑警报（红/黄/绿分类）

    def format_timestamp(self, ts: int) -> str:
        # 时间戳转可读格式
```

### exporter.py（导出功能）

```python
class Exporter:
    def to_json(self, data: dict, filename: str) -> str:
        # 导出JSON

    def to_csv(self, data: dict, filename: str) -> str:
        # 导出CSV

    def to_pdf(self, data: dict, filename: str) -> str:
        # 导出PDF（使用pdfkit或reportlab）
```

---

## 本地运行方案

### run.bat（Windows）

```batch
@echo off
echo 正在启动虚拟币犯罪调查工具集...
echo.
echo 请确保已安装Python 3.8+
echo.

REM 检查Python
python --version 2>NUL
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装
    pause
    exit /b 1
)

REM 安装依赖
pip install -r requirements.txt

REM 启动Flask
python app.py

echo 工具集已启动，请在浏览器打开 http://localhost:5000
pause
```

### 依赖文件 requirements.txt

```
flask==2.3.0
requests==2.31.0
python-dotenv==1.0.0
pdfkit==1.0.0  # PDF导出
werkzeug==2.3.0
```

---

## 法律合规

### 底部声明（所有页面）

> ⚠️ **本工具仅供合法调查使用，请遵守相关法律法规**
>
> - 仅用于依法授权的调查工作
> - 用户需自行获取合法的API密钥
> - 分析结果仅供参考，不作为司法证据
> - 使用者需遵守相关法律法规

---

## 与原培训材料的区别

| 原培训材料 | 本工具集 |
|------------|----------|
| 包含情景故事（老张对话等） | 仅工具说明，无情景 |
| 需要运行Python脚本 | Web界面，零代码操作 |
| 代码+说明文档分开 | 说明嵌入工具页面 |
| 无导出功能 | 支持JSON/CSV/PDF导出 |
| 无样本数据 | 样本填充按钮 |

---

## 开发里程碑（修正版 - 对应11个工具）

### Phase 1: 核心框架
- Flask应用结构
- 基础模板（base.html）
- 侧边栏导航
- API路由骨架
- 共享模块（api_client, formatter, exporter）

### Phase 2: 地址分析工具（3个）
- TRON可疑特征分析模块 + 前端页面
- TRON地址行为分析模块 + 前端页面
- ETH交易查询模块 + 前端页面（含跨链桥识别）

### Phase 3: 交易追踪工具（3个）
- Uniswap追踪模块 + 前端页面
- 混币器追踪模块 + 前端页面
- BTC交易分析模块 + 前端页面

### Phase 4: 跨链分析与协查工具（2个）
- 地址聚类模块 + 前端页面
- 跨境协查模块 + 前端页面

### Phase 5: 案件处理工具（3个）
- 多链监控模块 + 前端页面
- 混淆攻击对抗模块 + 前端页面
- 资产追回冻结模块 + 前端页面

### Phase 6: 导出与手册
- 导出功能完善（JSON/CSV/PDF）
- 用户手册编写（11个工具说明书）
- API获取指南（Tronscan/Etherscan/Blockchain）
- 测试与优化

---

## 成功标准

1. **一键启动** - Windows用户双击run.bat即可启动
2. **零代码使用** - 初学者无需接触Python代码
3. **完整覆盖** - 11个工具全部可用
4. **证据导出** - 结果可导出为标准格式
5. **手册完备** - 每个工具有完整说明书
6. **样本引导** - 样本数据帮助理解输入格式

---

*设计批准日期: 2026-04-23*