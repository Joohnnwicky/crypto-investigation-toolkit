---
phase: 04-cross-chain-analysis
plan: 03
status: completed
completed: 2026-04-24
---

# SUMMARY: Cluster Frontend Page

## Objective
Build address clustering frontend page with multi-line input, API key handling, cluster cards display, and export functionality.

## Files Created

| File | Purpose |
|------|---------|
| modules/cross/routes.py | Flask Blueprint with cluster endpoints |
| templates/cross/cluster.html | Frontend UI for address clustering |

## Endpoints Implemented

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /cross/api/cluster/query | POST | Address clustering API |
| /cross/cluster | GET | Cluster tool page |
| /cross/api/cluster/sample | GET | Sample addresses for demo |
| /cross/api/cluster/export/json | POST | JSON export |
| /cross/api/cluster/export/csv | POST | CSV export |

## Frontend Features (per D-01 to D-12)

### Input Section (D-01, D-03, D-04)
- Textarea for multi-address input (max 10 addresses per D-01)
- ETH API key input (shows when ETH addresses detected, per D-03)
- Sample fill button (per D-04)

### Results Display (D-09, D-10, D-11)
- Cluster cards with addresses, chain types, and reasons
- Unassociated addresses section (marked "无关联")
- Transaction statistics per cluster

### Export Functionality (D-12, D-20)
- JSON export button
- CSV export button
- "导出到跨境协查" button — stores result in sessionStorage and redirects

## Session Caching

- Cache key: `cit_cluster_result`
- Cache key for cross-border: `cit_cluster_export`
- Result restored on page load

## JavaScript Functions

| Function | Purpose |
|----------|---------|
| fillSample() | Fetch sample addresses from API |
| checkEthAddresses() | Show/hide ETH API key input |
| analyzeCluster() | POST addresses to cluster API |
| displayResults(data) | Render cluster cards |
| displayClusterCard(cluster) | Generate single cluster HTML |
| exportJSON() | Download JSON file |
| exportCSV() | Download CSV file |
| exportToCrossBorder() | Store in sessionStorage + redirect |

## Deviations

None — all D-01 to D-12 and D-20 requirements implemented.

## Next Steps

Plan 04-05 will register cross_bp blueprint in app.py for full integration.