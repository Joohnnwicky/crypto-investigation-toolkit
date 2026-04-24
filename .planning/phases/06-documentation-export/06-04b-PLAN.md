---
phase: 06-documentation-export
plan: 04b
type: execute
wave: 4
depends_on: [06-04a]
files_modified:
  - templates/docs/manual_tron_suspicious.html
  - templates/docs/manual_tron_behavior.html
  - templates/docs/manual_eth_query.html
  - templates/docs/manual_uniswap.html
  - templates/docs/manual_mixer.html
  - templates/docs/manual_btc.html
  - templates/docs/manual_cluster.html
  - templates/docs/manual_cross_border.html
  - templates/docs/manual_monitor.html
  - templates/docs/manual_obfuscation.html
  - templates/docs/manual_asset_freeze.html
autonomous: true
requirements: [DOC-01]
user_setup: []

must_haves:
  truths:
    - "User can read detailed manual for any of the 11 tools"
    - "Each manual has 4 sections: 操作步骤, 结果解释, API密钥说明, 案例演示"
  artifacts:
    - path: "templates/docs/manual_tron_suspicious.html"
      provides: "TRON suspicious analyzer manual"
      contains: "操作步骤"
      min_lines: 40
    - path: "templates/docs/manual_tron_behavior.html"
      provides: "TRON behavior analyzer manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_eth_query.html"
      provides: "ETH transaction query manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_uniswap.html"
      provides: "Uniswap tracker manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_mixer.html"
      provides: "Mixer tracker manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_btc.html"
      provides: "BTC analyzer manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_cluster.html"
      provides: "Cluster analyzer manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_cross_border.html"
      provides: "Cross-border template manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_monitor.html"
      provides: "Multi-chain monitor manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_obfuscation.html"
      provides: "Obfuscation detector manual"
      contains: "操作步骤"
    - path: "templates/docs/manual_asset_freeze.html"
      provides: "Asset freeze template manual"
      contains: "操作步骤"
  key_links:
    - from: "modules/docs/routes.py"
      to: "templates/docs/manual_*.html"
      via: "render_template"
      pattern: "render_template('docs/manual_"
---

<objective>
Create 11 tool manual pages with 4-section structure.

Purpose: Complete documentation system for all tools (per D-03, D-04).
Output: 11 manual templates with 操作步骤, 结果解释, API密钥说明, 案例演示 sections.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/06-documentation-export/06-CONTEXT.md
@.planning/phases/06-documentation-export/06-RESEARCH.md
@.planning/phases/06-documentation-export/06-PATTERNS.md
@.planning/phases/06-documentation-export/06-04a-SUMMARY.md
</context>

<interfaces>
<!-- Key patterns executor needs from existing templates -->

From templates/tron/suspicious_analyzer.html (lines 1-10) - Page structure:
```html
{% extends "base.html" %}
{% block title %}TRON可疑特征分析{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">TRON地址可疑特征分析</h1>
        <p class="text-gray-600">识别诈骗/洗钱等可疑行为特征，生成风险评分报告</p>
    </div>
</div>
{% endblock %}
```

<!-- Manual page 4-section structure per D-04: -->
1. 操作步骤 - numbered list of usage steps
2. 结果解释 - explanation of result types and meanings
3. API密钥说明 - whether API key needed, where to get it
4. 案例演示 - sample case walkthrough

<!-- Template naming and API key requirements: -->
- manual_tron_suspicious.html -> Tronscan API (no key needed)
- manual_tron_behavior.html -> Tronscan API (no key needed)
- manual_eth_query.html -> Etherscan API (key required)
- manual_uniswap.html -> Etherscan/Web3 API (key required for Etherscan)
- manual_mixer.html -> Etherscan/Web3 API (key required for Etherscan)
- manual_btc.html -> Blockstream API (no key needed)
- manual_cluster.html -> Multi-chain (Tronscan, Etherscan, Blockstream)
- manual_cross_border.html -> No API (local template generation)
- manual_monitor.html -> Multi-chain (TRON/ETH/BTC APIs)
- manual_obfuscation.html -> Etherscan API (ETH-only scope)
- manual_asset_freeze.html -> No API (imports data from other tools)
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Create TRON manual pages</name>
  <files>templates/docs/manual_tron_suspicious.html, templates/docs/manual_tron_behavior.html</files>
  <read_first>
    - templates/tron/suspicious_analyzer.html (page structure pattern)
    - templates/docs/manuals.html (created in 06-02)
  </read_first>
  <action>Create two TRON manual templates extending base.html. Each has title block with tool name + " - 使用手册". Content structure: header card with tool name and subtitle "操作步骤、结果解释、API说明与案例演示", then 4 white cards for each section. Section 1 (操作步骤): numbered list (ol class="list-decimal list-inside space-y-2") with 4-5 steps. Section 2 (结果解释): explain basic_info, alerts (red/yellow/green), score meanings. Section 3 (API密钥说明): "本工具使用Tronscan API，无需API密钥。" Section 4 (案例演示): brief sample walkthrough. Use bg-white rounded-lg shadow p-6 mb-6 for each section card.
  </action>
  <verify>
    <automated>grep -n "操作步骤" templates/docs/manual_tron_suspicious.html && grep -n "无需API密钥" templates/docs/manual_tron_suspicious.html && grep -n "操作步骤" templates/docs/manual_tron_behavior.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/docs/manual_tron_suspicious.html exists with 4 sections
    - templates/docs/manual_tron_behavior.html exists with 4 sections
    - Both templates extend base.html
    - Both contain "操作步骤" section with numbered list
    - Both contain "API密钥说明" stating Tronscan API no key needed
    - Both contain "结果解释" section
    - Both contain "案例演示" section
  </acceptance_criteria>
  <done>TRON manual pages created (suspicious, behavior).</done>
</task>

<task type="auto">
  <name>Task 2: Create ETH and trace manual pages</name>
  <files>templates/docs/manual_eth_query.html, templates/docs/manual_uniswap.html, templates/docs/manual_mixer.html, templates/docs/manual_btc.html</files>
  <read_first>
    - templates/docs/manual_tron_suspicious.html (pattern to follow)
  </read_first>
  <action>Create 4 manual templates with same 4-section structure. ETH Query: API密钥说明 explains "需要Etherscan API密钥，请在下方API获取指南查看注册方法。" Uniswap/Mixer: "需要Etherscan API密钥" + Web3 RPC explanation. BTC: "本工具使用Blockstream API，无需API密钥。" Operation steps differ per tool - describe specific input/analysis/export flow for each.
  </action>
  <verify>
    <automated>grep -l "操作步骤" templates/docs/manual_eth_query.html templates/docs/manual_uniswap.html templates/docs/manual_mixer.html templates/docs/manual_btc.html && grep -n "Etherscan API密钥" templates/docs/manual_eth_query.html && grep -n "Blockstream API" templates/docs/manual_btc.html</automated>
  </verify>
  <acceptance_criteria>
    - All 4 templates exist with 4-section structure
    - manual_eth_query.html mentions Etherscan API密钥 required
    - manual_uniswap.html and manual_mixer.html mention Etherscan/Web3 API
    - manual_btc.html states Blockstream API no key needed
    - All extend base.html with proper title blocks
  </acceptance_criteria>
  <done>ETH and trace manual pages created (eth_query, uniswap, mixer, btc).</done>
</task>

<task type="auto">
  <name>Task 3: Create cross and case manual pages</name>
  <files>templates/docs/manual_cluster.html, templates/docs/manual_cross_border.html, templates/docs/manual_monitor.html, templates/docs/manual_obfuscation.html, templates/docs/manual_asset_freeze.html</files>
  <read_first>
    - templates/docs/manual_tron_suspicious.html (pattern to follow)
  </read_first>
  <action>Create 5 manual templates with 4-section structure. Cluster: API密钥说明 lists Tronscan + Etherscan + Blockstream (multi-chain). Cross-border: "无需API密钥，本地生成模板。" Monitor: lists all 3 APIs (TRON/ETH/BTC). Obfuscation: "需要Etherscan API密钥，ETH链检测专用。" Asset-freeze: "无需API密钥，从其他工具导入数据。"
  </action>
  <verify>
    <automated>grep -l "操作步骤" templates/docs/manual_cluster.html templates/docs/manual_cross_border.html templates/docs/manual_monitor.html templates/docs/manual_obfuscation.html templates/docs/manual_asset_freeze.html && grep -c "操作步骤" templates/docs/manual_cluster.html</automated>
  </verify>
  <acceptance_criteria>
    - All 5 templates exist with 4-section structure
    - Each has correct API密钥说明 content for its tool
    - All extend base.html with proper title blocks
    - manual_cluster.html mentions multi-chain APIs
    - manual_obfuscation.html specifies ETH-only scope
    - manual_asset_freeze.html mentions import from other tools
  </acceptance_criteria>
  <done>Cross and case manual pages created (cluster, cross_border, monitor, obfuscation, asset_freeze).</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Client to manual pages | Static pages, no input |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-06-11 | Tampering | Manual content | accept | Static Jinja2 templates, no user input |
</threat_model>

<verification>
1. All 11 manual templates exist: ls templates/docs/manual_*.html returns 11 files
2. All templates have 4 sections: grep -l "操作步骤" templates/docs/manual_*.html returns 11 files
</verification>

<success_criteria>
- 11 manual templates created with 4-section structure
- Each template has correct API密钥说明 for its tool
- All templates extend base.html
</success_criteria>

<output>
After completion, create `.planning/phases/06-documentation-export/06-04b-SUMMARY.md`
</output>