---
phase: 05-case-handling
plan: 02
subsystem: case
tags: [attack-detection, eth, dex, sandwich, flash-loan, dusting]

requires:
  - phase: 05-case-handling-plan-01
    provides: routes.py structure, case_bp Blueprint
provides:
  - Obfuscation attack detection tool with 4 attack type heuristics
  - ETH-only attack pattern analysis with HIGH/MEDIUM/LOW confidence
  - Tool interconnection exports via sessionStorage
affects: [05-03]

tech-stack:
  added: []
  patterns: [confidence-scoring, attack-heuristics]

key-files:
  created:
    - modules/case/obfuscation_detector.py
    - templates/case/obfuscation.html
  modified:
    - modules/case/routes.py

key-decisions:
  - "ETH-only scope per D-24 (DEX attacks on Uniswap/Sushiswap)"
  - "Rule-based heuristics with confidence scoring pattern from mixer_tracker.py"
  - "Session cache key: cit_obfuscation_result"

patterns-established:
  - "Pattern: Confidence colors HIGH=red, MEDIUM=yellow, LOW=blue"
  - "Pattern: Attack detection returns attack_cards sorted by confidence"

requirements-completed: [CASE-02]

duration: 12min
completed: 2026-04-24
---

# Phase 5 Plan 02: Obfuscation Attack Detector Summary

**ETH obfuscation attack detection tool with rule-based heuristics for Sandwich, Flash Loan, Dusting, and Protocol vulnerability attacks, confidence scoring following mixer_tracker pattern**

## Performance

- **Duration:** 12 min
- **Started:** 2026-04-24T16:45:00Z
- **Completed:** 2026-04-24T16:57:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- 4 attack type detectors with rule-based heuristics (Sandwich, Flash Loan, Dusting, Protocol vulnerability)
- Confidence scoring pattern reused from mixer_tracker.py (HIGH/MEDIUM/LOW)
- ETH-only scope validation (per D-24)
- Attack cards display with colored confidence badges
- Tool interconnection exports to ETH query and asset freeze

## Files Created/Modified
- `modules/case/obfuscation_detector.py` - Attack detection heuristics with detect_attacks_web, detect_sandwich_attack, detect_flash_loan_attack, detect_dusting_attack, detect_protocol_vulnerability
- `modules/case/routes.py` - Added obfuscation routes under case_bp
- `templates/case/obfuscation.html` - Attack detection UI with ETH address input, attack cards, export buttons

## Decisions Made
- DEX_ROUTERS dict includes Uniswap V2/V3, Sushiswap addresses from RESEARCH.md
- DUST_THRESHOLD = 0.001 ETH per D-21 for dusting detection
- High value threshold = 100 ETH for flash loan detection (HIGH confidence)
- 10+ unique recipients for dusting MEDIUM confidence, 50+ for HIGH
- Failed tx with >10 ETH value triggers LOW confidence protocol vulnerability

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None - all acceptance criteria verified successfully.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Plan 05-02 complete, routes.py ready for 05-03 asset freeze routes addition
- Sequential execution required due to files_modified overlap on routes.py

---
*Phase: 05-case-handling*
*Completed: 2026-04-24*