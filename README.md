# 区块猎影 BLOCKSHADE

虚拟币犯罪调查工具集

---

## 简介

区块猎影是为虚拟货币犯罪调查构建的专业分析工具集，提供本地运行、零配置的完整解决方案，涵盖地址分析、交易追踪、跨链分析和案件处理四大模块。

## 功能模块

### 地址分析

| 工具 | 说明 |
|------|------|
| TRON可疑分析 | 识别诈骗/洗钱可疑特征，自动检测异常交易模式 |
| TRON行为分析 | 分析地址交易行为模式，生成行为特征报告 |
| ETH交易查询 | 查询以太坊交易记录，支持批量地址检索 |

### 交易追踪

| 工具 | 说明 |
|------|------|
| Uniswap追踪 | 还原DEX交易路径，追踪代币兑换流向 |
| 混币器追踪 | 还原洗钱路径，追踪Tornado Cash等混币器资金流向 |
| BTC交易分析 | 查询比特币流向，分析UTXO关联 |

### 跨链分析

| 工具 | 说明 |
|------|------|
| 地址聚类 | 关联多个地址，识别同一控制主体 |
| 跨境协查 | 生成国际协作模板，支持跨境调查协作 |

### 案件处理

| 工具 | 说明 |
|------|------|
| 多链监控 | 实时监控地址状态，支持多链同时监控 |
| 混淆对抗 | 识别攻击手法，检测地址混淆技术 |
| 资产追回 | 生成冻结建议模板，辅助资产冻结申请 |

## 技术架构

- **后端**: Python Flask
- **前端**: Tailwind CSS + 自定义Hacker主题
- **数据源**: 公链API (TronGrid, Etherscan, Blockchain.com)

## 安装部署

### 环境要求

- Python 3.10+
- pip

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/Joohnnwicky/BLOCKSHADE.git
cd BLOCKSHADE

# 安装依赖
pip install -r requirements.txt

# 运行服务
python app.py
```

### Windows快捷启动

双击 `run.bat` 或在命令行执行：

```cmd
run.bat
```

### Linux/macOS快捷启动

```bash
chmod +x run.sh
./run.sh
```

访问 http://127.0.0.1:5000

## API配置

部分工具需要配置外部API密钥。访问 `/docs/api-guide` 获取详细配置指南。

### TronGrid API

1. 访问 https://www.trongrid.io/
2. 申请API Key
3. 配置到系统设置

### Etherscan API

1. 访问 https://etherscan.io/apis
2. 注册并获取API Key
3. 配置到系统设置

## 使用手册

访问 `/docs/manuals` 查看各工具详细使用手册：

- TRON可疑分析手册
- TRON行为分析手册
- ETH交易查询手册
- Uniswap追踪手册
- 混币器追踪手册
- BTC交易分析手册
- 地址聚类手册
- 跨境协查手册
- 多链监控手册
- 混淆对抗手册
- 资产追回手册

## UI特性

- **Hacker主题**: 深色背景 + 绿色虚线边框，终端风格设计
- **中文字体**: 字魂凹凸世界体，专业视觉效果
- **缓存功能**: 分析结果自动缓存，表单内容自动保存
- **地址优化**: 完整地址显示，水平滚动查看

## 目录结构

```
BLOCKSHADE/
├── app.py                 # Flask入口
├── requirements.txt       # 依赖列表
├── run.bat                # Windows启动脚本
├── run.sh                 # Linux/macOS启动脚本
├── modules/               # 后端模块
│   ├── core/              # 核心功能
│   ├── tron/              # TRON分析
│   ├── eth/               # ETH分析
│   ├── trace/             # 交易追踪
│   ├── cross/             # 跨链分析
│   ├── case/              # 案件处理
│   └── docs/              # 文档路由
├── templates/             # 前端页面
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页
│   ├── tron/              # TRON工具页面
│   ├── eth/               # ETH工具页面
│   ├── trace/             # 追踪工具页面
│   ├── cross/             # 跨链工具页面
│   ├── case/              # 案件工具页面
│   └── docs/              # 文档页面
├── static/                # 静态资源
│   ├── logo.png           # Logo图片
│   └── fonts/             # 字体文件
└── .planning/             # 开发计划文档
```

## 许可证

本项目仅供教育和研究目的使用。

## 贡献

欢迎提交Issue和Pull Request。

---

**区块猎影** - 让虚拟货币犯罪调查更高效