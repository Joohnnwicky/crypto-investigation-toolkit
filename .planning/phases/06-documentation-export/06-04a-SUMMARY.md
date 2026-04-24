---
phase: 06-documentation-export
plan: 04a
subsystem: docs
tags: [routes, api-guide, navigation, documentation]
requires: [06-01, 06-02]
provides: [manual-routes, api-guide-page, sidebar-link]
affects: [modules/docs/routes.py, templates/docs/api_guide.html, templates/base.html]
key_decisions:
  - D1: Added slug validation in manual route to prevent arbitrary template rendering
tech_stack:
  added: [Flask route patterns]
  patterns: [Blueprint routes, Jinja2 templates, active state highlighting]
key_files:
  created: [templates/docs/api_guide.html]
  modified: [modules/docs/routes.py, templates/base.html]
---

# Phase 6 Plan 04a: Documentation Page Routes & API Guide Summary

## One-Liner

Added documentation page routes to docs Blueprint and created API key registration guide with Tronscan, Etherscan, and Blockstream sections.

## Tasks Completed

| Task | Name | Commit | Files |
| ---- | ---- | ------ | ----- |
| 1 | Add manual page routes to docs Blueprint | ced6e9f | modules/docs/routes.py |
| 2 | Create API guide page | 93c251f | templates/docs/api_guide.html |
| 3 | Add API guide sidebar link | a217bd6 | templates/base.html |

## Implementation Details

### Task 1: Manual Page Routes

Added three route handlers to `modules/docs/routes.py`:
- `/docs/manuals` - Renders manuals index page
- `/docs/api-guide` - Renders API key guide page
- `/docs/manual/<tool>` - Dynamic route for 11 tool manual pages with slug validation

Security: Slug validation prevents arbitrary template path injection.

### Task 2: API Guide Page

Created `templates/docs/api_guide.html` with three service sections:
- **Tronscan API**: FREE, no key needed, direct access
- **Etherscan API**: Requires registration, 5 calls/sec free tier, key security warnings
- **Blockstream API**: FREE, no key needed, direct access

Each section includes 4 subsections per requirements:
- 注册流程 (Registration Process)
- 使用限制 (Usage Limits)
- 安全说明 (Security Notes)
- 问题排查 (Troubleshooting)

### Task 3: Sidebar Link

Added "API获取指南" link to sidebar navigation after "使用手册" with active state highlighting.

## Verification

All acceptance criteria verified:
- Routes registered: `/docs/manuals`, `/docs/api-guide`, `/docs/manual/<slug>`
- API guide contains Tronscan, Etherscan, Blockstream sections
- Each service section has 4 required subsections
- Etherscan section mentions 5 calls/sec rate limit
- Sidebar link has active state highlighting

## Deviations from Plan

None - plan executed exactly as written.

## Duration

~4 minutes (222 seconds)

## Self-Check: PASSED

- [x] templates/docs/api_guide.html exists
- [x] modules/docs/routes.py contains all three route decorators
- [x] templates/base.html contains API guide link
- [x] All commits verified in git log