# Phase 6: Documentation & Export - Research

**Researched:** 2026-04-24
**Domain:** PDF export (WeasyPrint), user documentation, API guides
**Confidence:** HIGH (verified from existing codebase and official docs)

## Summary

This phase implements PDF export functionality for all 11 tools and creates a comprehensive user documentation system. The PDF export extends the existing JSON/CSV export module in `modules/core/exporter.py` using WeasyPrint (HTML-to-PDF conversion). User documentation consists of 12 pages (homepage + 11 tool manuals) using the established card-based layout pattern from `templates/index.html`. API guide page provides registration instructions for Tronscan (free, no key), Etherscan (requires key), and Blockstream (free, no key).

**Primary recommendation:** Extend `exporter.py` with PDF export function; create `modules/docs/` Blueprint with routes for manuals and API guide; add PDF button to all 11 tool result sections using the existing export button trio pattern.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**PDF导出功能:**
- D-01: PDF导出使用WeasyPrint库（HTML直接转PDF，风格与现有页面一致）
- D-02: PDF导出按钮在所有11个工具结果页面统一出现（与JSON/CSV并列）

**用户手册组织:**
- D-03: 手册首页展示11个工具卡片，点击卡片进入详细说明书页面（需12个页面：首页+11详情）
- D-04: 每个工具说明书包含：操作步骤、结果解释、API密钥说明、案例演示

**API获取指南:**
- D-05: API密钥获取指南为独立页面（`/docs/api-guide`）
- D-06: API获取指南包含：注册流程、使用限制、安全说明、问题排查

### Claude's Discretion

- WeasyPrint安装脚本（Windows GTK依赖处理）
- PDF导出按钮具体样式设计
- 手册首页卡片布局细节
- 说明书页面模板设计
- API指南页面具体内容编写
- 侧边栏导航新增入口（手册、API指南）

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EXPORT-03 | User can export analysis results as PDF | WeasyPrint PDF export pattern, extend exporter.py |
| DOC-01 | User can read tool-specific user manuals (11 manuals) | 12 pages using index.html card pattern, base.html sidebar link |
| DOC-02 | User can follow API key registration guides (Tronscan, Etherscan, Blockchain) | API guide page with 3 sections, existing api_client.py for reference |

</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| PDF generation | Backend (Python) | — | WeasyPrint runs in Python, converts HTML to PDF |
| PDF download trigger | Frontend (JS) | — | Button onclick calls /api/export/pdf endpoint |
| Manual pages | Backend (Flask) + Frontend (HTML) | — | Flask routes serve templates, Jinja2 renders |
| API guide content | Backend (Flask) + Frontend (HTML) | — | Static content page, no dynamic data |
| Sidebar navigation | Frontend (base.html) | — | Template-level navigation links |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| WeasyPrint | 62.x (latest) | HTML-to-PDF conversion | Official docs recommend for visual PDF rendering [CITED: doc.courtbouillon.org] |
| Flask | 3.1.3 (existing) | PDF export route handler | Already in requirements.txt |
| Tailwind CSS | v4 CDN (existing) | PDF styling consistency | HTML source uses same styles, PDF matches web |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|------------|
| pydyf | bundled | PDF internal format | WeasyPrint dependency |
| pango | 1.44+ (via MSYS2) | Text rendering on Windows | Required for WeasyPrint on Windows |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| WeasyPrint | pdfkit (wkhtmltopdf) | Requires separate binary install, less integrated |
| WeasyPrint | ReportLab | Programmatic PDF, loses HTML styling |
| WeasyPrint | xhtml2pdf | Deprecated, poor CSS support |

**Installation:**

Primary (pip):
```bash
pip install weasyprint
```

Windows GTK dependency (MSYS2) — required before pip install:
```bash
# 1. Install MSYS2 from https://www.msys2.org/
# 2. In MSYS2 shell:
pacman -S mingw-w64-x86_64-pango

# 3. Set DLL directories in Windows CMD:
set WEASYPRINT_DLL_DIRECTORIES=C:\msys64\mingw64\bin

# 4. Verify:
python -m weasyprint --info
```

**Version verification:** [VERIFIED: WebFetch from doc.courtbouillon.org]
- WeasyPrint stable requires Python >= 3.10.0, Pango >= 1.44.0
- Windows executable available from GitHub releases (alternative to MSYS2)

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PDF Export Flow                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Tool Result Page ──► [PDF Button] ──► POST /api/export/pdf                │
│        │                                              │                      │
│        │                                              ▼                      │
│        │                                     exporter.py                     │
│        │                                     export_pdf()                   │
│        │                                              │                      │
│        │                                              ▼                      │
│        │                                     WeasyPrint HTML()              │
│        │                                     (result template)              │
│        │                                              │                      │
│        │                                              ▼                      │
│        │                                     PDF bytes ──► Download         │
│        │                                     (Content-Disposition)          │
│        │                                              │                      │
│        ▼                                              ▼                      │
│   analysisResult ─────────────────────────────► PDF filename               │
│   (JS variable)                                  {tool}_{addr}_{date}.pdf   │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                        Documentation Flow                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Sidebar ──► /docs/manuals ──► manuals.html (11 card grid)                 │
│      │              │                                                        │
│      │              ▼                                                        │
│      │         Click card ──► /docs/manual/{tool}                           │
│      │              │                                                        │
│      │              ▼                                                        │
│      │         manual_{tool}.html (4 sections: steps, results, API, demo)   │
│      │                                                                       │
│      ▼                                                                       │
│   /docs/api-guide ──► api_guide.html (3 sections: Tronscan, Etherscan, BTC) │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure

```
modules/
├── core/
│   └── exporter.py      # EXTEND: add export_pdf(), get_pdf_template()
├── docs/                # NEW module
│   ├── __init__.py
│   ├── routes.py        # Blueprint: /docs/manuals, /docs/manual/{tool}, /docs/api-guide
│   └── pdf_exporter.py  # PDF-specific template rendering
templates/
├── docs/                # NEW templates
│   ├── manuals.html     # Homepage: 11 tool cards
│   ├── manual_tron_suspicious.html
│   ├── manual_tron_behavior.html
│   ├── manual_eth_query.html
│   ├── manual_uniswap.html
│   ├── manual_mixer.html
│   ├── manual_btc.html
│   ├── manual_cluster.html
│   ├── manual_cross_border.html
│   ├── manual_monitor.html
│   ├── manual_obfuscation.html
│   ├── manual_asset_freeze.html
│   └── api_guide.html   # API key registration guide
├── base.html            # MODIFY: add /docs/api-guide sidebar link
└── {tool}/              # MODIFY: add PDF button to export sections
```

### Pattern 1: PDF Export Button Integration

**What:** Add PDF export button alongside existing JSON/CSV buttons
**When to use:** All 11 tool result pages
**Example:**

```html
<!-- Source: templates/tron/suspicious_analyzer.html (extended) -->
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
        <!-- NEW: PDF export button -->
        <button onclick="exportPDF()"
                class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition">
            导出PDF
        </button>
    </div>
</div>
```

```javascript
// NEW: PDF export function (add to each tool's JS)
function exportPDF() {
    if (!analysisResult) {
        alert('请先进行分析');
        return;
    }

    fetch('/docs/api/export/pdf', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            result: analysisResult,
            tool_type: 'tron_suspicious'  // Identifies which template to use
        })
    })
    .then(response => {
        const filename = response.headers.get('Content-Disposition')
            .split('filename=')[1].replace(/"/g, '');
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
    .catch(error => alert('PDF导出失败: ' + error.message));
}
```

### Pattern 2: Manual Homepage Card Grid

**What:** 11 tool cards in 4 category groups, reuse index.html pattern
**When to use:** `/docs/manuals` page
**Example:**

```html
<!-- Source: templates/index.html pattern -->
<div class="space-y-6">
    <!-- Category 1: Address Analysis -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">地址分析工具</h2>
        <div class="grid grid-cols-3 gap-4">
            <a href="/docs/manual/tron-suspicious" class="block p-4 bg-gray-50 rounded hover:bg-gray-100">
                <h3 class="font-bold text-gray-700">TRON可疑分析</h3>
                <p class="text-sm text-gray-500 mt-1">说明书与操作指南</p>
            </a>
            <!-- ... more cards -->
        </div>
    </div>
</div>
```

### Pattern 3: Tool Manual Page Structure

**What:** 4-section template for each tool manual
**When to use:** All 11 manual detail pages
**Example:**

```html
<!-- templates/docs/manual_tron_suspicious.html -->
{% extends "base.html" %}
{% block title %}TRON可疑分析 - 使用手册{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">TRON地址可疑特征分析</h1>
        <p class="text-gray-600">操作步骤、结果解释、API说明与案例演示</p>
    </div>

    <!-- Section 1: 操作步骤 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-lg font-bold text-gray-700 mb-4">操作步骤</h2>
        <ol class="list-decimal list-inside space-y-2">
            <li>输入TRON钱包地址（34位，以T开头）</li>
            <li>点击"加载样本"按钮查看示例地址格式</li>
            <li>点击"开始分析"按钮</li>
            <li>等待API返回数据，查看分析结果</li>
        </ol>
    </div>

    <!-- Section 2: 结果解释 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-lg font-bold text-gray-700 mb-4">结果解释</h2>
        <!-- ... -->
    </div>

    <!-- Section 3: API密钥说明 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-lg font-bold text-gray-700 mb-4">API密钥说明</h2>
        <p>本工具使用Tronscan API，无需API密钥。</p>
    </div>

    <!-- Section 4: 案例演示 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-lg font-bold text-gray-700 mb-4">案例演示</h2>
        <!-- ... -->
    </div>
</div>
{% endblock %}
```

### Anti-Patterns to Avoid

- **Don't create PDF from scratch:** Use HTML templates, let WeasyPrint convert
- **Don't style PDF separately:** PDF inherits styles from HTML, use same Tailwind classes
- **Don't hardcode PDF content:** Template renders analysisResult data dynamically
- **Don't ignore Windows users:** Provide GTK installation script or clear instructions

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| PDF generation | Custom PDF library code | WeasyPrint HTML() | Handles fonts, CSS, layout automatically |
| PDF styling | PDF-specific CSS | Same Tailwind classes | Consistency with web, simpler maintenance |
| Manual card layout | Custom grid CSS | index.html pattern | Established pattern, proven in Phase 1 |
| Export filename | Custom naming logic | get_export_filename() | Already in exporter.py, extend for PDF |
| API guide content | Guess API limits | Official docs + existing api_client.py | api_client.py shows actual endpoints used |

**Key insight:** WeasyPrint's HTML-to-PDF approach preserves visual consistency without extra work. The same HTML template that renders results on screen can be converted to PDF.

## Common Pitfalls

### Pitfall 1: Windows GTK Dependencies Missing

**What goes wrong:** `ImportError: cannot load library 'pango'` on Windows
**Why it happens:** WeasyPrint depends on GTK libraries (pango, cairo) not bundled in pip
**How to avoid:**
1. Provide installation script or clear MSYS2 instructions
2. Set `WEASYPRINT_DLL_DIRECTORIES=C:\msys64\mingw64\bin` environment variable
3. Verify with `python -m weasyprint --info` before use

**Warning signs:** ImportError at WeasyPrint import time

### Pitfall 2: PDF Filename Collision

**What goes wrong:** Multiple exports overwrite same filename
**Why it happens:** Filename doesn't include unique identifier (address, timestamp)
**How to avoid:** Follow existing pattern: `{tool}_{addr_short}_{date}.pdf`

**Warning signs:** Users report missing previous exports

### Pitfall 3: Sidebar Navigation Missing API Guide

**What goes wrong:** Users can't find API guide page
**Why it happens:** base.html sidebar only has `/docs/manuals` link (line 54)
**How to avoid:** Add `/docs/api-guide` link to sidebar after manuals link

**Warning signs:** Users ask how to get API keys

### Pitfall 4: PDF Button on All 11 Tools

**What goes wrong:** Some tools missing PDF export button
**Why it happens:** Manual addition to 11 templates, easy to miss one
**How to avoid:** Checklist verification: verify all 11 templates have PDF button

**Tool list:**
1. tron/suspicious_analyzer.html
2. tron/behavior_analyzer.html
3. eth/transaction_query.html
4. trace/uniswap.html
5. trace/mixer.html
6. trace/btc.html
7. cross/cluster.html
8. cross/cross_border.html
9. case/monitor.html
10. case/obfuscation.html
11. case/asset_freeze.html

## Code Examples

### PDF Export Function (extend exporter.py)

```python
# modules/core/exporter.py (add this function)

from weasyprint import HTML, CSS
from flask import render_template_string

def export_pdf(data: Dict[str, Any], tool_type: str) -> bytes:
    """Convert analysis result to PDF bytes using WeasyPrint.

    Args:
        data: Analysis result dict
        tool_type: Tool identifier for template selection

    Returns:
        PDF bytes for download
    """
    # Render HTML template with data
    html_template = get_pdf_template(tool_type)
    html_content = render_template_string(html_template, result=data)

    # Convert to PDF
    pdf = HTML(string=html_content).write_pdf()
    return pdf

def get_pdf_filename(address: str, tool_type: str) -> str:
    """Generate PDF filename following existing pattern.

    Args:
        address: Wallet address
        tool_type: Tool identifier

    Returns:
        Filename like "tron_suspicious_TUtP...NNw_20240115.pdf"
    """
    from datetime import datetime
    date_str = datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    return f"{tool_type}_{addr_short}_{date_str}.pdf"
```

### PDF Export Route (docs/routes.py)

```python
# modules/docs/routes.py

from flask import Blueprint, request, Response, jsonify
from modules.core.exporter import export_pdf, get_pdf_filename

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

@docs_bp.route('/api/export/pdf', methods=['POST'])
def export_pdf_endpoint():
    """Export analysis result as PDF file download.

    Request JSON body: {"result": data, "tool_type": str}
    Response: PDF file download
    """
    data = request.get_json()
    if not data or 'result' not in data or 'tool_type' not in data:
        return jsonify({'error': 'Missing result or tool_type'}), 400

    result = data['result']
    tool_type = data['tool_type']
    address = result.get('address', 'unknown')

    pdf_bytes = export_pdf(result, tool_type)
    filename = get_pdf_filename(address, tool_type)

    response = Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response
```

### Sidebar Navigation Update (base.html)

```html
<!-- templates/base.html (add after line 54) -->
<!-- Documentation -->
<a href="/docs/manuals" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/manuals' %} bg-gray-700{% endif %}">使用手册</a>
<a href="/docs/api-guide" class="block py-2 px-4 rounded hover:bg-gray-700 transition{% if request.path == '/docs/api-guide' %} bg-gray-700{% endif %}">API获取指南</a>
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Programmatic PDF (ReportLab) | HTML-to-PDF (WeasyPrint) | 2020s | Preserves styling, simpler code |
| Static PDF templates | Dynamic Jinja2 templates | This project | Data-driven PDFs, matches web UI |
| PDFkit + wkhtmltopdf binary | WeasyPrint pure Python | 2023+ | Fewer external dependencies |

**Deprecated/outdated:**
- xhtml2pdf: Poor CSS support, deprecated
- pdfkit: Requires wkhtmltopdf binary install

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | WeasyPrint works with Tailwind CSS CDN classes | Standard Stack | PDF styling may differ from web |
| A2 | All 11 tools use same result data structure | Architecture | PDF template may need per-tool customization |
| A3 | Tronscan API remains free without key requirement | API Guide | Documentation may need update |

**If this table is empty:** All claims in this research were verified or cited — no user confirmation needed.

## Open Questions (RESOLVED)

1. **PDF Template Per-Tool Customization** [RESOLVED: Single template approach adopted]
   - What we know: Different tools have different result structures (alerts vs behaviors vs transactions)
   - What's unclear: Single template handles all, or per-tool templates?
   - Resolution: Implementation uses single generic template in export_pdf() function (modules/core/exporter.py) that renders result data with standard sections (basic_info, alerts). This approach is simpler and maintains consistency across all tools. Per-tool customization deferred until runtime testing reveals specific needs.

2. **WeasyPrint Windows Bundled Installer** [RESOLVED: Documentation-only approach]
   - What we know: GTK dependencies require MSYS2 installation
   - What's unclear: Should project provide bundled installer script?
   - Resolution: Provide clear documentation in README and installation guide. Windows executable from WeasyPrint GitHub releases is simpler alternative for users who prefer not to install MSYS2. The MSYS2 instructions in Standard Stack section above provide the recommended path. No bundled installer script needed.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| WeasyPrint | PDF export | Install needed | 62.x | — |
| GTK/Pango | WeasyPrint on Windows | Install needed (MSYS2) | 1.44+ | Use WSL |
| Flask | Routes | Available | 3.1.3 | — |
| Tailwind CSS CDN | PDF styling | Available | v4 | — |

**Missing dependencies with no fallback:**
- WeasyPrint must be installed (pip install weasyprint)
- GTK/Pango on Windows: MSYS2 installation or WSL

**Missing dependencies with fallback:**
- Windows users can use WSL if MSYS2 installation fails

## Security Domain

> Security enforcement enabled (nyquist_validation=false but docs touch API keys)

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Single-user local tool |
| V3 Session Management | no | No sessions |
| V4 Access Control | no | No authorization |
| V5 Input Validation | yes | Flask request validation |
| V6 Cryptography | no | No encryption needed |

### Known Threat Patterns for Flask + PDF

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| XSS in PDF content | Tampering | Jinja2 autoescape enabled |
| Path traversal in filename | Tampering | sanitize filename characters |
| Large PDF generation DoS | Denial | Limit result data size |

**API Key Security:**
- API guide should emphasize: never share keys, use separate keys per project
- Etherscan key stored only in user input (per ADDR-05), not persisted

## Sources

### Primary (HIGH confidence)

- doc.courtbouillon.org/weasyprint/stable/first_steps.html — Windows installation with MSYS2
- modules/core/exporter.py — Existing export pattern to extend
- templates/tron/suspicious_analyzer.html — Export button pattern to extend
- templates/index.html — Card grid pattern for manuals homepage
- modules/core/api_client.py — API endpoints used (Tronscan, Etherscan)
- modules/trace/btc_analyzer.py — Blockstream API usage (free, no key)

### Secondary (MEDIUM confidence)

- templates/base.html — Sidebar navigation structure
- app.py — Blueprint registration pattern

### Tertiary (LOW confidence)

- [ASSUMED] WeasyPrint Tailwind CSS compatibility — needs runtime verification

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — WeasyPrint official docs verified, existing exporter.py read
- Architecture: HIGH — Existing patterns from index.html, suspicious_analyzer.html, routes.py
- Pitfalls: HIGH — Windows GTK installation documented, common issues known

**Research date:** 2026-04-24
**Valid until:** 30 days (stable libraries, but WeasyPrint versions may change)