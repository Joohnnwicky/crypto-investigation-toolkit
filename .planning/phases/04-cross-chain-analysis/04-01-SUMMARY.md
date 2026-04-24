---
phase: 04-cross-chain-analysis
plan: 01
status: completed
completed: 2026-04-24
---

# SUMMARY: Address Clustering Backend Module

## Objective
Build address clustering backend module with chain detection and 4 clustering heuristics for multi-address association analysis across TRON, ETH, and BTC chains.

## Files Created

| File | Purpose |
|------|---------|
| modules/cross/__init__.py | Package initialization |
| modules/cross/chain_detector.py | Chain type detection (TRON/ETH/BTC) |
| modules/cross/cluster_analyzer.py | Address clustering with 4 heuristics |

## Key Functions Implemented

### chain_detector.py
- `detect_chain_type(address)` — Identifies TRON (T prefix), ETH (0x prefix), BTC (1/3/bc1 prefixes)
- `validate_address_format(address)` — Validates address against known patterns
- `get_chain_requirements(chain)` — Returns API key requirements per chain

### cluster_analyzer.py
- `cluster_addresses_web(addresses, api_keys)` — Main clustering function (max 10 addresses per D-01)
- `find_first_funding_source(address, chain, tx_data)` — D-05 heuristic
- `check_mutual_transfers(addr1, addr2, address_data)` — D-06 heuristic (threshold: 2+ transfers)
- `calculate_activity_window(address, tx_data)` — Activity time window calculation
- `calculate_time_overlap(window1, window2)` — D-07 heuristic (threshold: 70%+ overlap)
- `find_shared_deposit(addr1, addr2, address_data)` — D-08 heuristic

## Clustering Heuristics Implemented

| Heuristic | Code | Threshold | Detection |
|-----------|------|-----------|-----------|
| First funding source match | D-05 | Exact match | Same first incoming tx source |
| Frequent mutual transfers | D-06 | ≥2 transfers | Direct transfers between addresses |
| Time window overlap | D-07 | ≥70% overlap | Activity timing correlation |
| Shared deposit address | D-08 | Exact match | Same deposit address used |

## Result Structure (per D-09, D-10, D-11)

```python
{
    'success': True,
    'addresses': [...],
    'clusters': [
        {
            'cluster_id': 1,
            'addresses': ['Txxx...', '0x123...'],
            'chain_types': ['tron', 'eth'],
            'reasons': ['首次资金来源相同: Tabc123...', '频繁互转账: 3次'],
            'shared_source': 'Tabc123...',
            'mutual_transfers': [...],
            'time_window': {'overlap_pct': 85},
            'shared_deposit': 'Tdeposit123...',
            'stats': {'total_transactions': 50, 'total_volume': '...'}
        }
    ],
    'unassociated': ['Tzzz...']  # Addresses with no associations
}
```

## API Integration

- TRON: Uses existing `get_account_info`, `get_trc20_transfers` from `api_client.py`
- ETH: Uses existing `get_eth_transactions`, `get_erc20_transfers` from `api_client.py` (requires API key per D-03)
- BTC: Blockstream free API (no key required per RESEARCH.md recommendation)

## Deviations

None — all D-01 to D-11 requirements implemented as specified.

## Next Steps

Plan 04-03 will create Flask routes and frontend page for this module.