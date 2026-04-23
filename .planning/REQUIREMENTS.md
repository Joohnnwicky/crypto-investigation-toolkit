# REQUIREMENTS: Crypto Investigation Toolkit

**Project:** CIT
**Updated:** 2026-04-23
**Milestone:** v1 - Core Framework

---

## v1 Requirements

### Core Framework

- [ ] **CORE-01**: User can start Flask application via run.bat (Windows) or run.sh (Linux/Mac)
- [ ] **CORE-02**: User sees homepage with tool overview and 4 group categories
- [ ] **CORE-03**: User can navigate between tools via sidebar
- [ ] **CORE-04**: Application loads sample data to help users understand input format
- [ ] **CORE-05**: Application displays legal compliance disclaimer on all pages

### Address Analysis Tools

- [ ] **ADDR-01**: User can analyze TRON address for suspicious features (red/yellow/green alerts)
- [ ] **ADDR-02**: User receives risk score (0-100) for TRON address analysis
- [ ] **ADDR-03**: User can analyze TRON address behavior patterns
- [ ] **ADDR-04**: User can query ETH address transactions with cross-chain bridge detection
- [ ] **ADDR-05**: User inputs API key manually (not stored by application)

### Transaction Tracking Tools

- [ ] **TRACE-01**: User can trace Uniswap DEX trading paths
- [ ] **TRACE-02**: User can trace mixer (混币器) laundering paths
- [ ] **TRACE-03**: User can analyze BTC transaction flow

### Cross-Chain Analysis Tools

- [ ] **CROSS-01**: User can cluster multiple addresses for association analysis
- [ ] **CROSS-02**: User can generate cross-border investigation coordination templates

### Case Handling Tools

- [ ] **CASE-01**: User can monitor addresses across multiple chains in real-time
- [ ] **CASE-02**: User can identify obfuscation attack techniques
- [ ] **CASE-03**: User can generate asset freeze request templates

### Export & Documentation

- [ ] **EXPORT-01**: User can export analysis results as JSON
- [ ] **EXPORT-02**: User can export analysis results as CSV
- [ ] **EXPORT-03**: User can export analysis results as PDF
- [ ] **DOC-01**: User can read tool-specific user manuals (11 manuals)
- [ ] **DOC-02**: User can follow API key registration guides (Tronscan, Etherscan, Blockchain)

---

## v2 Requirements (Deferred)

- Real-time address monitoring alerts
- Batch address analysis
- Historical data caching
- Multi-language support (English)
- Dark mode theme

---

## Out of Scope

- User authentication system — single-user local tool
- Data persistence/storage — confidentiality requirement
- Cloud deployment — local-only requirement
- Training scenario stories — tool documentation only
- Built-in API keys — users must obtain their own

---

## Traceability

| Phase | Requirements | Status |
|-------|--------------|--------|
| 1 | CORE-01 to CORE-05, ADDR-01 to ADDR-03, EXPORT-01, EXPORT-02 | Pending |
| 2 | ADDR-04, ADDR-05 | Pending |
| 3 | TRACE-01, TRACE-02, TRACE-03 | Pending |
| 4 | CROSS-01, CROSS-02 | Pending |
| 5 | CASE-01, CASE-02, CASE-03 | Pending |
| 6 | DOC-01, DOC-02, EXPORT-03 | Pending |

---
*Updated: 2026-04-23*