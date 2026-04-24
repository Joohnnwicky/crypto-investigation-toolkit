---
phase: 06-documentation-export
plan: 03a
type: execute
wave: 2
depends_on: [06-01]
files_modified:
  - templates/tron/suspicious_analyzer.html
  - templates/tron/behavior_analyzer.html
  - templates/eth/transaction_query.html
autonomous: true
requirements: [EXPORT-03]
user_setup: []

must_haves:
  truths:
    - "User sees PDF export button alongside JSON/CSV buttons on TRON tools"
    - "User sees PDF export button alongside JSON/CSV buttons on ETH tool"
    - "PDF button triggers /docs/api/export/pdf endpoint with correct tool_type"
  artifacts:
    - path: "templates/tron/suspicious_analyzer.html"
      provides: "PDF export button in export section"
      contains: "exportPDF()"
      min_lines: 1
    - path: "templates/tron/behavior_analyzer.html"
      provides: "PDF export button"
      contains: "exportPDF()"
    - path: "templates/eth/transaction_query.html"
      provides: "PDF export button"
      contains: "exportPDF()"
  key_links:
    - from: "exportPDF() JavaScript"
      to: "/docs/api/export/pdf"
      via: "fetch POST"
      pattern: "fetch('/docs/api/export/pdf'"
---

<objective>
Add PDF export button to TRON and ETH tool result pages.

Purpose: Enable PDF export for TRON suspicious/behavior analyzers and ETH transaction query (per D-02).
Output: 3 templates have purple PDF button in export section with exportPDF() JavaScript function.
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

From templates/tron/suspicious_analyzer.html (lines 226-254) - Export JavaScript pattern:
```javascript
function exportJSON() {
    if (!analysisResult) {
        alert('请先进行地址分析');
        return;
    }
    fetch('/tron/api/export/json', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ result: analysisResult })
    })
    .then(response => {
        const filename = response.headers.get('Content-Disposition').split('filename=')[1].replace(/"/g, '');
        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => alert('导出失败: ' + error.message));
}
```

<!-- tool_type values for each template: -->
1. tron/suspicious_analyzer.html -> tool_type: 'tron_suspicious'
2. tron/behavior_analyzer.html -> tool_type: 'tron_behavior'
3. eth/transaction_query.html -> tool_type: 'eth_query'
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Add PDF button to TRON templates</name>
  <files>templates/tron/suspicious_analyzer.html, templates/tron/behavior_analyzer.html</files>
  <read_first>
    - templates/tron/suspicious_analyzer.html (export section lines 83-96, JavaScript lines 226-284)
    - templates/tron/behavior_analyzer.html (export section and JavaScript)
  </read_first>
  <action>Add purple PDF button after the CSV button in export section of both templates. Button HTML: <button onclick="exportPDF()" class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">导出PDF</button>. Add exportPDF() JavaScript function after existing export functions. Function: check analysisResult exists, POST to /docs/api/export/pdf with JSON body {result: analysisResult, tool_type: 'tron_suspicious'} for suspicious_analyzer, {result: analysisResult, tool_type: 'tron_behavior'} for behavior_analyzer. Handle response same as existing export functions (extract filename from Content-Disposition, create blob download). Alert message: 'PDF导出失败' on error. Use exact pattern from suspicious_analyzer.html exportJSON function.
  </action>
  <verify>
    <automated>grep -n "exportPDF()" templates/tron/suspicious_analyzer.html && grep -n "bg-purple-500" templates/tron/suspicious_analyzer.html && grep -n "'/docs/api/export/pdf'" templates/tron/suspicious_analyzer.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/tron/suspicious_analyzer.html contains exportPDF() button with bg-purple-500 class
    - templates/tron/suspicious_analyzer.html contains exportPDF() JavaScript function
    - templates/tron/suspicious_analyzer.html JavaScript fetches /docs/api/export/pdf with tool_type 'tron_suspicious'
    - templates/tron/behavior_analyzer.html contains exportPDF() button with bg-purple-500 class
    - templates/tron/behavior_analyzer.html contains exportPDF() JavaScript function
    - templates/tron/behavior_analyzer.html JavaScript fetches /docs/api/export/pdf with tool_type 'tron_behavior'
  </acceptance_criteria>
  <done>PDF export button added to TRON suspicious_analyzer and behavior_analyzer templates.</done>
</task>

<task type="auto">
  <name>Task 2: Add PDF button to ETH template</name>
  <files>templates/eth/transaction_query.html</files>
  <read_first>
    - templates/eth/transaction_query.html (export section and JavaScript)
  </read_first>
  <action>Add PDF button and exportPDF() function to templates/eth/transaction_query.html following same pattern as Task 1. Button placement: after CSV button in export section. JavaScript: tool_type = 'eth_query'. Alert: 'PDF导出失败'.
  </action>
  <verify>
    <automated>grep -n "exportPDF()" templates/eth/transaction_query.html && grep -n "'tool_type': 'eth_query'" templates/eth/transaction_query.html</automated>
  </verify>
  <acceptance_criteria>
    - templates/eth/transaction_query.html contains exportPDF() button with bg-purple-500 class
    - templates/eth/transaction_query.html contains exportPDF() JavaScript function
    - JavaScript fetches /docs/api/export/pdf with tool_type 'eth_query'
  </acceptance_criteria>
  <done>PDF export button added to ETH transaction_query template.</done>
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
| T-06-05 | Tampering | exportPDF() tool_type value | accept | tool_type is hardcoded in template, not user input |
| T-06-06 | Denial | PDF button rapid clicks | accept | Browser handles repeated clicks, no server-side rate limit needed for local tool |
</threat_model>

<verification>
1. All 3 templates contain exportPDF() function
2. All 3 templates contain bg-purple-500 button
3. Each template has correct tool_type value
</verification>

<success_criteria>
- TRON suspicious_analyzer and behavior_analyzer have PDF export button
- ETH transaction_query has PDF export button
- All templates have exportPDF() JavaScript with correct tool_type
</success_criteria>

<output>
After completion, create `.planning/phases/06-documentation-export/06-03a-SUMMARY.md`
</output>