---
phase: 01-core-framework
plan: 06
subsystem: core-infrastructure
tags: [startup, deployment, dependencies]
requires: [01-03-PLAN.md, 01-04-PLAN.md]
provides:
  - Zero-config local startup capability
  - Automated dependency installation
  - Cross-platform startup scripts
affects:
  - User onboarding experience
  - Local deployment workflow
tech-stack:
  added:
    - Python requirements.txt
    - Windows batch script (run.bat)
    - Linux/Mac shell script (run.sh)
  patterns:
    - Dependency auto-installation
    - Browser auto-launch on Windows
key-files:
  created:
    - requirements.txt
    - run.bat
    - run.sh
decisions:
  - Flask exact version 3.1.3 for stability
  - Browser auto-open on Windows (start command)
  - No browser auto-open on Linux/Mac (system differences)
  - pip show for dependency check
metrics:
  duration: 120s
  tasks: 3
  files: 3
  completed: 2026-04-23
---

# Phase 1 Plan 06: Startup Scripts Summary

## One-Liner

Created zero-config startup scripts (run.bat, run.sh) and requirements.txt enabling one-click local Flask application launch with automated dependency installation.

## What Was Built

### 1. requirements.txt
Python dependency file for the Crypto Investigation Toolkit:
- Flask==3.1.3 - Web framework (exact version for stability)
- requests>=2.32.0 - HTTP client for Tronscan API (already installed)
- pandas>=3.0.0 - Data handling for future tools (already installed)

### 2. run.bat (Windows)
Windows startup script with:
- Flask installation check via `pip show Flask`
- Auto-install dependencies if missing
- Directory change to script location (`%~dp0`)
- Browser auto-open after 2-second delay
- Chinese user guidance messages

### 3. run.sh (Linux/Mac)
Linux/Mac startup script with:
- Bash shebang for execution
- Flask installation check via `pip show Flask`
- Auto-install dependencies if missing
- Directory change to script location (`$(dirname "$0")`)
- Python3 execution for Unix compatibility
- Chinese user guidance messages

## Files Created

| File | Purpose | Lines |
|------|---------|-------|
| requirements.txt | Python dependencies | 9 |
| run.bat | Windows startup | 29 |
| run.sh | Linux/Mac startup | 23 |

## How to Use

**Windows:**
1. Double-click `run.bat`
2. Browser opens automatically to http://127.0.0.1:5000

**Linux/Mac:**
1. `chmod +x run.sh` (first time only)
2. `./run.sh`
3. Open browser to http://127.0.0.1:5000

## Deviations from Plan

None - plan executed exactly as written.

## Verification Results

| Criteria | Status | Evidence |
|----------|--------|----------|
| requirements.txt exists | PASS | File created, 9 lines |
| Flask==3.1.3 specified | PASS | grep confirmed |
| run.bat exists | PASS | File created, 29 lines |
| python app.py in run.bat | PASS | grep confirmed |
| Browser opening | PASS | start http://127.0.0.1:5000 |
| run.sh exists | PASS | File created, 23 lines |
| python3 app.py in run.sh | PASS | grep confirmed |
| Dependency auto-install | PASS | pip install in both scripts |

## Commits

| Hash | Message |
|------|---------|
| f215292 | feat(01-06): add requirements.txt with Flask and dependencies |
| a2c8651 | feat(01-06): add run.bat Windows startup script |
| c58d057 | feat(01-06): add run.sh Linux/Mac startup script |

## Self-Check: PASSED

- [x] All files created exist
- [x] All commits exist in git log
- [x] No unexpected deletions

## Threat Flags

No new threat surfaces introduced. Scripts run with user permissions, no privilege escalation.

## Known Stubs

None - all functionality complete.

## Next Steps

Plan 01-06 completes the Core Framework phase startup infrastructure. User can now:
1. Double-click `run.bat` (Windows) or run `./run.sh` (Linux/Mac)
2. Flask server starts with automatic dependency installation
3. Browser opens to toolkit homepage (Windows only)

---
*Created: 2026-04-23*