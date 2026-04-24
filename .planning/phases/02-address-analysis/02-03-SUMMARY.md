---
phase: 02-address-analysis
plan: 03
subsystem: eth-frontend
tags: [etherscan, stargate, ui-frontend, api-key-input]
requires: [ADDR-04, ADDR-05]
provides:
  - ETH transaction query user interface
  - API key input field with helpful placeholder
  - Card-based transaction display
  - Stargate bridge events visualization
affects:
  - modules/eth/routes.py (page route /eth/transaction-query)
tech_stack:
  added:
    - ETH transaction query HTML template
    - Stargate events card section with blue styling
  patterns:
    - API key per-request pattern (no localStorage)
    - Card-based UI layout matching TRON suspicious analyzer
key_files:
  created:
    - templates/eth/transaction_query.html
  modified: []
decisions:
  - D-07: ETH UI matches TRON suspicious analyzer layout
  - D-08: ETH results use card-based format
  - ADDR-05: API key sent per-request only, never stored
  - T-02-03-01: No localStorage for API key (mitigated)
metrics:
  duration: 3 minutes
  completed_date: 2026-04-24
  task_count: 1
  file_count: 1
commits:
  - hash: 00656f7
    message: feat(02-03): add ETH transaction query frontend with API key input and Stargate detection
    task: 1
---

# Phase 02 Plan 03: ETH Transaction Query Frontend Summary

**One-liner:** ETH transaction query frontend with API key input (per-request only), card-based transaction display, and Stargate cross-chain bridge events visualization.

## Completed Tasks

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Create transaction_query.html with API key input and results layout | 00656f7 | templates/eth/transaction_query.html |

## Implementation Details

### Task 1: ETH Transaction Query Frontend

Created `templates/eth/transaction_query.html` following D-07 and D-08 UI patterns:

**Header Section:**
- Title: "ETH交易查询"
- Description: "查询以太坊交易历史，识别Stargate跨链桥事件"

**Input Section (ADDR-05 compliance):**
- ETH address input field (`id="address-input"`)
  - Placeholder: "例如：0x1234567890abcdef1234567890abcdef12345678"
- API key input field (`id="api-key-input"`)
  - Placeholder: "从 etherscan.io 获取免费API密钥" (per Pitfall 1 in RESEARCH.md)
- "开始查询" button triggers `queryTransactions()`
- No sample button - API key required per query

**Results Layout:**
- Basic info card: address, total transaction count, ETH transfers count, ERC20 transfers count
- Normal transactions table: hash (with Etherscan link), timestamp, from, to, value (ETH)
- ERC20 transfers table: hash, timestamp, token symbol, from, to, value
- Stargate events card (blue styling `bg-blue-50 border-l-4 border-blue-500`):
  - Bridge icon SVG header
  - Event cards showing: contract_type, tx_hash, timestamp, addresses, value
  - Explanatory text about cross-chain transfers

**Export Buttons:**
- JSON export: calls `/eth/api/export/json`
- CSV export: calls `/eth/api/export/csv`

**JavaScript Functions:**
- `queryTransactions()`: fetch POST to `/eth/api/query` with `{ address, api_key }` in body
- `displayResults()`: populates all result cards
- `displayTransactions()`: renders normal ETH transfers table
- `displayERC20Transfers()`: renders ERC20 token transfers table
- `displayStargateEvents()`: renders bridge events in blue card section
- `exportJSON()` / `exportCSV()`: trigger file download

## Deviations from Plan

None - plan executed exactly as written.

## Threat Model Mitigations

| Threat ID | Category | Mitigation | Status |
|-----------|----------|------------|--------|
| T-02-03-01 | Information Disclosure | No localStorage/sessionStorage for API key, only per-request POST body | Implemented |
| T-02-03-02 | Tampering | Backend validates address with regex, XSS handled by Jinja2 auto-escape | Implemented |

## Verification Results

- File exists: templates/eth/transaction_query.html (408 lines)
- Contains `{% extends "base.html" %}`
- Contains `{% block title %}ETH交易查询{% endblock %}`
- Contains address input field with id
- Contains API key input field with etherscan.io placeholder
- Contains `queryTransactions()` function
- Contains fetch to `/eth/api/query` with address and api_key in body
- Contains `stargate-events` section
- Contains export buttons (JSON/CSV)
- No localStorage usage confirmed

## Known Stubs

None - all functionality is fully implemented.

## Threat Flags

No new threat surfaces beyond those documented in plan's threat model.

## Next Steps

1. Register eth_bp in app.py if not already done
2. Add ETH tool link to homepage sidebar (already in base.html navigation)
3. Test full integration with Flask app running

## Self-Check: PASSED

- templates/eth/transaction_query.html exists
- File has 408 lines (>= 200 requirement)
- Contains extends "base.html"
- Contains api_key input with etherscan.io placeholder
- Contains stargate-events section
- No localStorage usage found
- Commit 00656f7 exists in git log