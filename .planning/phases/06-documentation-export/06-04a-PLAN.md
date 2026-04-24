---
phase: 06-documentation-export
plan: 04a
type: execute
wave: 3
depends_on: [06-01, 06-02]
files_modified:
  - modules/docs/routes.py
  - templates/docs/api_guide.html
  - templates/base.html
autonomous: true
requirements: [DOC-02]
user_setup: []

must_haves:
  truths:
    - "User can follow API key registration guide for Tronscan, Etherscan, Blockstream"
    - "API guide has 4 parts per service: 注册流程, 使用限制, 安全说明, 问题排查"
    - "User can navigate to API guide from sidebar"
    - "Manual page routes exist for all 11 tools"
  artifacts:
    - path: "templates/docs/api_guide.html"
      provides: "API key registration guide"
      contains: "Tronscan"
      contains: "Etherscan"
      contains: "Blockstream"
      min_lines: 80
    - path: "templates/base.html"
      provides: "Sidebar API guide link"
      contains: "/docs/api-guide"
    - path: "modules/docs/routes.py"
      provides: "Documentation page routes"
      contains: "@docs_bp.route('/manuals')"
      contains: "@docs_bp.route('/api-guide')"
  key_links:
    - from: "templates/base.html sidebar"
      to: "/docs/api-guide"
      via: "a href link"
      pattern: "href=\"/docs/api-guide\""
---

<objective>
Add manual page routes to docs Blueprint, create API guide page, add sidebar navigation link.

Purpose: Set up route infrastructure and API key guide (per D-05, D-06).
Output: Routes for all 12 doc pages, API guide template with 3 service sections, sidebar API guide link.
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
@.planning/phases/06-documentation-export/06-01-SUMMARY.md
@.planning/phases/06-documentation-export/06-02-SUMMARY.md
</context>

<interfaces>
<!-- Key patterns executor needs from existing templates and routes -->

From modules/tron/routes.py (lines 99-108) - Page route pattern:
```python
@tron_bp.route('/behavior-analyzer')
def behavior_analyzer_page():
    return render_template('tron/behavior_analyzer.html')
```

From templates/base.html (line 54) - Sidebar link pattern:
```python
<a href="/docs/manuals" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/manuals' %} bg-gray-700{% endif %}">使用手册</a>
```

<!-- Route slugs for manual pages: -->
- /docs/manuals -> renders manuals.html
- /docs/manual/tron-suspicious -> renders manual_tron_suspicious.html
- /docs/manual/tron-behavior -> renders manual_tron_behavior.html
- /docs/manual/eth-query -> renders manual_eth_query.html
- /docs/manual/uniswap -> renders manual_uniswap.html
- /docs/manual/mixer -> renders manual_mixer.html
- /docs/manual/btc -> renders manual_btc.html
- /docs/manual/cluster -> renders manual_cluster.html
- /docs/manual/cross-border -> renders manual_cross_border.html
- /docs/manual/monitor -> renders manual_monitor.html
- /docs/manual/obfuscation -> renders manual_obfuscation.html
- /docs/manual/asset-freeze -> renders manual_asset_freeze.html

<!-- API services to document: -->
- Tronscan API: https://api.tronscan.org/api - FREE, NO KEY NEEDED
- Etherscan API V2: https://api.etherscan.io/v2/api - KEY REQUIRED, 5 calls/sec free tier
- Blockstream API: https://blockstream.info/api - FREE, NO KEY NEEDED
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Add manual page routes to docs Blueprint</name>
  <files>modules/docs/routes.py</files>
  <read_first>
    - modules/docs/routes.py (existing PDF endpoint from 06-01)
    - modules/tron/routes.py (page route pattern lines 99-108)
  </read_first>
  <action>Add page routes to modules/docs/routes.py for all 12 documentation pages. Routes: /docs/manuals (renders manuals.html), /docs/manual/<tool_slug> (renders manual_{slug}.html), /docs/api-guide (renders api_guide.html). Use Flask route pattern with render_template. For /docs/manual/<slug>, create single route handler that maps slug to template. Example: @docs_bp.route('/manual/<tool>') def manual_page(tool): return render_template(f'docs/manual_{tool}.html'). Handle 11 slugs: tron-suspicious, tron-behavior, eth-query, uniswap, mixer, btc, cluster, cross-border, monitor, obfuscation, asset-freeze. Note: modules/docs/routes.py was created in 06-01 with PDF endpoint - this task adds page routes to existing file.
  </action>
  <verify>
    <automated>grep -n "@docs_bp.route('/manuals')" modules/docs/routes.py && grep -n "@docs_bp.route('/api-guide')" modules/docs/routes.py && grep -n "@docs_bp.route('/manual/" modules/docs/routes.py</automated>
  </verify>
  <acceptance_criteria>
    - modules/docs/routes.py contains @docs_bp.route('/manuals') returning render_template('docs/manuals.html')
    - modules/docs/routes.py contains @docs_bp.route('/api-guide') returning render_template('docs/api_guide.html')
    - modules/docs/routes.py contains route for /docs/manual/<slug> pattern
    - All routes follow existing Blueprint pattern
  </acceptance_criteria>
  <done>Documentation page routes added to docs Blueprint.</done>
</task>

<task type="auto">
  <name>Task 2: Create API guide page</name>
  <files>templates/docs/api_guide.html</files>
  <read_first>
    - templates/index.html (static page layout pattern)
    - modules/core/api_client.py (actual API endpoints used, if exists)
  </read_first>
  <action>Create templates/docs/api_guide.html extending base.html. Title: "API密钥获取指南". Content: header card with title and subtitle "Tronscan、Etherscan、Blockstream API注册指南", then 3 service sections. Each section has 4 subsections per D-06: 注册流程, 使用限制, 安全说明, 问题排查. Tronscan section: FREE API, https://tronscan.org, no registration needed, direct API access. Etherscan section: requires registration at https://etherscan.io, free tier 5 calls/sec, key storage warning. Blockstream section: FREE API, https://blockstream.info, no key needed. Use h2 for service names, h3 for subsection titles. Each section in bg-white rounded-lg shadow p-6 mb-6 card.
  </action>
  <verify>
    <automated>grep -n "Tronscan" templates/docs/api_guide.html && grep -n "Etherscan" templates/docs/api_guide.html && grep -n "Blockstream" templates/docs/api_guide.html && grep -n "注册流程" templates/docs/api_guide.html && grep -n "使用限制" templates/docs/api_guide.html && grep -n "安全说明" templates/docs/api_guide.html && grep -n "问题排查" templates/docs/api_guide.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/docs/api_guide.html exists
    - Template extends base.html
    - Template contains 3 service sections (Tronscan, Etherscan, Blockstream)
    - Each service section contains 4 subsections (注册流程, 使用限制, 安全说明, 问题排查)
    - Etherscan section mentions 5 calls/sec rate limit
    - Tronscan and Blockstream sections state no key needed
  </acceptance_criteria>
  <done>API guide page created with Tronscan, Etherscan, Blockstream sections.</done>
</task>

<task type="auto">
  <name>Task 3: Add API guide sidebar link</name>
  <files>templates/base.html</files>
  <read_first>
    - templates/base.html (sidebar lines 53-55)
  </read_first>
  <action>Add API guide link to templates/base.html sidebar after the "使用手册" link (after line 54). Link pattern: <a href="/docs/api-guide" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/api-guide' %} bg-gray-700{% endif %}">API获取指南</a>. Place in Documentation section of sidebar, right after 使用手册 link.
  </action>
  <verify>
    <automated>grep -n "href=\"/docs/api-guide\"" templates/base.html && grep -n "API获取指南" templates/base.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/base.html contains href="/docs/api-guide" link
    - Link text is "API获取指南"
    - Link placed after 使用手册 link in sidebar
    - Link follows same CSS class pattern as other sidebar links
    - Link has active state highlighting via request.path check
  </acceptance_criteria>
  <done>API guide sidebar navigation link added.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Client to API guide | Static page, no input |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-06-09 | Tampering | API guide content | accept | Static Jinja2 template, no user input |
| T-06-10 | Information Disclosure | API key guidance | mitigate | Emphasize never share keys, use per-project keys in 安全说明 sections |
</threat_model>

<verification>
1. API guide template exists: ls templates/docs/api_guide.html
2. Sidebar has API guide link: grep "api-guide" templates/base.html
3. Routes registered: grep "/manual" and "/api-guide" in modules/docs/routes.py
</verification>

<success_criteria>
- API guide template created with 3 service sections
- Sidebar contains API获取指南 link
- All page routes registered in docs Blueprint
</success_criteria>

<output>
After completion, create `.planning/phases/06-documentation-export/06-04a-SUMMARY.md`
</output>