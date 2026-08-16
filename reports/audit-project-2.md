================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   20 analyzed | ~600 lines of code

## Summary
CRITICAL: 1 | HIGH: 1 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] Falsa Criptografia
- **File:** utils/utils.js:functions
- **Description:** `badCrypto` uses Base64 encoding for passwords.
- **Impact:** Reversible, critical security failure.
- **Recommendation:** Use `bcrypt` with salt.

### [HIGH] Callback Hell
- **File:** controllers/checkoutController.js:various
- **Description:** Deeply nested `db.all` callbacks.
- **Impact:** Maintenance nightmare.
- **Recommendation:** Refactor to `async/await`.

### [MEDIUM] Hardcoded Gateway Keys
- **File:** config/config.js
- **Description:** Keys in plain text.
- **Impact:** Security risk.
- **Recommendation:** Use `dotenv`.

### [MEDIUM] Query N+1 Problem
- **File:** controllers/reportController.js:20-40
- **Description:** Querying per-user in loop.
- **Impact:** Performance degradation.
- **Recommendation:** Use JOIN or `IN` clause.

### [LOW] Poor Naming Conventions
- **File:** controllers/checkoutController.js
- **Description:** `u`, `e`, `p` variables.
- **Impact:** Hard to read.
- **Recommendation:** Use descriptive names.

### [LOW] Unused Dependencies
- **File:** package.json
- **Description:** Several unused packages listed.
- **Impact:** Increased attack surface/bloat.
- **Recommendation:** Cleanup dependencies.
