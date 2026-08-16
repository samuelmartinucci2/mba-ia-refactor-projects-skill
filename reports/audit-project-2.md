================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   20 analyzed | ~600 lines of code

## Summary
CRITICAL: 2 | HIGH: 1 | MEDIUM: 1 | LOW: 1

## Findings

### [CRITICAL] Falsa Criptografia
- **File:** utils/utils.js:functions
- **Description:** `badCrypto` uses recursive Base64 encoding for password hashing.
- **Impact:** Base64 is reversible encoding, not hashing. Exposure of user credentials.
- **Recommendation:** Use `bcrypt` with salt for secure password hashing.

### [CRITICAL] Callback Hell
- **File:** controllers/checkoutController.js:various
- **Description:** Deeply nested `db.all(..., function(err, row) { db.all(...) ... })`.
- **Impact:** "Pyramid of Doom". Extremely hard to maintain, test, and handle errors.
- **Recommendation:** Refactor to Promises using `util.promisify` or `sqlite3` promise-based wrappers.

### [HIGH] Hardcoded Gateway Keys
- **File:** config/config.js
- **Description:** `paymentGatewayKey` and DB credentials in plain text.
- **Impact:** High risk of credential compromise.
- **Recommendation:** Load via `dotenv` (process.env).

### [MEDIUM] Query N+1 Problem
- **File:** controllers/reportController.js:20-40
- **Description:** Iterating through enrollment list, executing DB query for each user.
- **Impact:** Poor performance; database overload under load.
- **Recommendation:** Refactor to a single SQL query with JOIN or `IN` clause.

### [LOW] Poor Naming Conventions
- **File:** controllers/checkoutController.js
- **Description:** Variables named `u`, `e`, `p` throughout checkout flow.
- **Impact:** Low maintainability, hard to read.
- **Recommendation:** Use descriptive names (e.g., `user`, `email`, `paymentDetails`).
