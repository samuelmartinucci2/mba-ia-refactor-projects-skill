================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~500 lines of code

## Summary
CRITICAL: 1 | HIGH: 1 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] SQL Injection
- **File:** models/pedido.py:various
- **Description:** Raw SQL built via f-strings.
- **Impact:** SQL Injection vulnerability.
- **Recommendation:** Use parameterized queries.

### [HIGH] God Class
- **File:** models/pedido.py:1-150
- **Description:** Single file handles order creation, items, inventory, reports, status.
- **Impact:** Violates SRP, impossible to test.
- **Recommendation:** Refactor into specialized services.

### [MEDIUM] Hardcoded Secret Key
- **File:** app.py:8
- **Description:** `SECRET_KEY` hardcoded as string literal.
- **Impact:** Credential leakage risk.
- **Recommendation:** Use `os.getenv('SECRET_KEY')`.

### [MEDIUM] Lack of structured logging
- **File:** controllers/pedido_controller.py
- **Description:** Usage of `print()` for application flow events.
- **Impact:** No traceability in production.
- **Recommendation:** Use standard library `logging`.

### [LOW] Magic Numbers
- **File:** models/pedido.py:120-130
- **Description:** Hardcoded discount thresholds (1000, 5000).
- **Impact:** Fragile business logic.
- **Recommendation:** Use configuration constants.

### [LOW] Inconsistent Variable Naming
- **File:** controllers/usuario_controller.py
- **Description:** Mixed `snake_case` and `camelCase` for user data fields.
- **Impact:** Confusing API schema.
- **Recommendation:** Enforce `snake_case` globally.
