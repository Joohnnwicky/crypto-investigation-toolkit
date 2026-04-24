---
phase: 06-documentation-export
plan: 03b
type: execute
wave: 2
depends_on: [06-01]
files_modified:
  - templates/trace/uniswap.html
  - templates/trace/mixer.html
  - templates/trace/btc.html
  - templates/cross/cluster.html
  - templates/cross/cross_border.html
  - templates/case/monitor.html
  - templates/case/obfuscation.html
  - templates/case/asset_freeze.html
autonomous: true
requirements: [EXPORT-03]
user_setup: []

must_haves:
  truths:
    - "User sees PDF export button alongside JSON/CSV buttons on trace tools"
    - "User sees PDF export button alongside JSON/CSV buttons on cross tools"
    - "User sees PDF export button alongside JSON/CSV buttons on case tools"
    - "PDF button triggers /docs/api/export/pdf endpoint with correct tool_type"
  artifacts:
    - path: "templates/trace/uniswap.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/trace/mixer.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/trace/btc.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/cross/cluster.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/cross/cross_border.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/case/monitor.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/case/obfuscation.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/case/asset_freeze.html"
      provides: "PDF export button"
      contains: "exportPDF()"
  key_links:
    - from: "exportPDF() JavaScript"
      to: "/docs/api/export/pdf"
      via: "fetch POST"
      pattern: "fetch('/docs/api/export/pdf'"
---

<objective>
Add PDF export button to trace, cross, and case tool result pages.

Purpose: Enable PDF export for remaining 8 tools (per D-02).
Output: 8 templates have purple PDF button in export section with exportPDF() JavaScript function.
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
@.planning/phases/06-documentation-export/06-03a-SUMMARY.md
</context>

<interfaces>
<!-- Key patterns executor needs from existing templates -->

From templates/tron/suspicious_analyzer.html (lines 83-96) - Export button trio:
```html
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-lg font-bold text-gray-700 mb-4">导出结果</h2>
    <div class="flex space-x-4">
        <button onclick="exportJSON()"
                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
            导出JSON
        </button>
        <button onclick="exportCSV()"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
            导出CSV
        </button>
    </div>
</div>
```

<!-- tool_type values for each template: -->
1. trace/uniswap.html -> tool_type: 'uniswap'
2. trace/mixer.html -> tool_type: 'mixer'
3. trace/btc.html -> tool_type: 'btc'
4. cross/cluster.html -> tool_type: 'cluster'
5. cross/cross_border.html -> tool_type: 'cross_border'
6. case/monitor.html -> tool_type: 'monitor'
7. case/obfuscation.html -> tool_type: 'obfuscation'
8. case/asset_freeze.html -> tool_type: 'asset_freeze'
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Add PDF button to trace templates</name>
  <files>templates/trace/uniswap.html, templates/trace/mixer.html, templates/trace/btc.html</files>
  <read_first>
    - templates/trace/uniswap.html (export section and JavaScript)
    - templates/trace/mixer.html (export section and JavaScript)
    - templates/trace/btc.html (export section lines 77-89)
  </read_first>
  <action>Add PDF button and exportPDF() function to all three templates. Button HTML: <button onclick="exportPDF()" class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">导出PDF</button>. Add after CSV button. JavaScript function pattern: check analysisResult, POST to /docs/api/export/pdf with {result: analysisResult, tool_type: 'uniswap'} for uniswap.html, {result: analysisResult, tool_type: 'mixer'} for mixer.html, {result: analysisResult, tool_type: 'btc'} for btc.html. Handle response same as existing export functions (blob download with filename from Content-Disposition). Alert: 'PDF导出失败' on error. Note: templates/trace/btc.html may have slightly different export button location - find export section and add button there.
  </action>
  <verify>
    <automated>grep -n "exportPDF()" templates/trace/uniswap.html && grep -n "'tool_type': 'uniswap'" templates/trace/uniswap.html && grep -n "exportPDF()" templates/trace/mixer.html && grep -n "'tool_type': 'mixer'" templates/trace/mixer.html && grep -n "exportPDF()" templates/trace/btc.html && grep -n "'tool_type': 'btc'" templates/trace/btc.html</automated>
  </verify>
  <acceptance_criteria>
    - All three templates contain exportPDF() button with bg-purple-500 class
    - All three templates contain exportPDF() JavaScript function
    - uniswap.html uses tool_type 'uniswap'
    - mixer.html uses tool_type 'mixer'
    - btc.html uses tool_type 'btc'
  </acceptance_criteria>
  <done>PDF export button added to all trace templates (uniswap, mixer, btc).</done>
</task>

<task type="auto">
  <name>Task 2: Add PDF button to cross templates</name>
  <files>templates/cross/cluster.html, templates/cross/cross_border.html</files>
  <read_first>
    - templates/cross/cluster.html (export section and JavaScript)
    - templates/cross/cross_border.html (export section and JavaScript)
  </read_first>
  <action>Add PDF button and exportPDF() function to both templates. Button HTML: <button onclick="exportPDF()" class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">导出PDF</button>. Add after CSV button. JavaScript: tool_type values: 'cluster' for cluster.html, 'cross_border' for cross_border.html. Alert: 'PDF导出失败' on error. Follow same pattern as Task 1.
  </action>
  <verify>
    <automated>grep -n "exportPDF()" templates/cross/cluster.html && grep -n "'tool_type': 'cluster'" templates/cross/cluster.html && grep -n "exportPDF()" templates/cross/cross_border.html && grep -n "'tool_type': 'cross_border'" templates/cross/cross_border.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/cross/cluster.html contains exportPDF() button and JavaScript
    - cluster.html uses tool_type 'cluster'
    - templates/cross/cross_border.html contains exportPDF() button and JavaScript
    - cross_border.html uses tool_type 'cross_border'
  </acceptance_criteria>
  <done>PDF export button added to cross templates (cluster, cross_border).</done>
</task>

<task type="auto">
  <name>Task 3: Add PDF button to case templates</name>
  <files>templates/case/monitor.html, templates/case/obfuscation.html, templates/case/asset_freeze.html</files>
  <read_first>
    - templates/case/monitor.html (export section - may be dynamically generated in JavaScript)
    - templates/case/obfuscation.html (export section)
    - templates/case/asset_freeze.html (export section)
  </read_first>
  <action>Add PDF button and exportPDF() function to all three templates. Button HTML: <button onclick="exportPDF()" class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">导出PDF</button>. Add after CSV button. JavaScript: tool_type values: 'monitor' for monitor.html, 'obfuscation' for obfuscation.html, 'asset_freeze' for asset_freeze.html. Alert: 'PDF导出失败' on error. Note: templates/case/monitor.html may generate export buttons dynamically via JavaScript - if so, add PDF button generation code to the JavaScript export button section. For other templates, follow standard pattern from Task 1.
  </action>
  <verify>
    <automated>grep -n "exportPDF" templates/case/monitor.html && grep -n "'tool_type': 'monitor'" templates/case/monitor.html && grep -n "exportPDF()" templates/case/obfuscation.html && grep -n "'tool_type': 'obfuscation'" templates/case/obfuscation.html && grep -n "exportPDF()" templates/case/asset_freeze.html && grep -n "'tool_type': 'asset_freeze'" templates/case/asset_freeze.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/case/monitor.html contains exportPDF (button and/or JavaScript function)
    - monitor.html uses tool_type 'monitor'
    - templates/case/obfuscation.html contains exportPDF() button and JavaScript
    - obfuscation.html uses tool_type 'obfuscation'
    - templates/case/asset_freeze.html contains exportPDF() button and JavaScript
    - asset_freeze.html uses tool_type 'asset_freeze'
  </acceptance_criteria>
  <done>PDF export button added to all case templates (monitor, obfuscation, asset_freeze).</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Browser JavaScript to /docs/api/export/pdf | JSON payload with analysis result |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-06-07 | Tampering | exportPDF() tool_type value | accept | tool_type is hardcoded in template, not user input |
| T-06-08 | Denial | PDF button rapid clicks | accept | Browser handles repeated clicks, no server-side rate limit needed for local tool |
</threat_model>

<verification>
1. All 8 templates contain exportPDF() function
2. All 8 templates contain bg-purple-500 button
3. Each template has correct tool_type value
4. Count: grep -l "exportPDF" templates/trace/*.html templates/cross/*.html templates/case/*.html should return 8 files
</verification>

<success_criteria>
- All 8 trace/cross/case templates have purple PDF export button
- All templates have exportPDF() JavaScript function
- Each template uses correct tool_type identifier
</success_criteria>

<output>
After completion, create `.planning/phases/06-documentation-export/06-03b-SUMMARY.md`
</output>