================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~500 lines of code

## Summary
CRITICAL: 2 | HIGH: 1 | MEDIUM: 1 | LOW: 1

## Findings

### [CRITICAL] SQL Injection
- **File:** models/pedido.py:various
- **Description:** Raw SQL built via concatenation or f-strings (e.g., `f"SELECT * FROM ... WHERE id = {id}"`).
- **Impact:** Attacker can execute arbitrary SQL queries.
- **Recommendation:** Use parameterized queries (`?` placeholder) via `cursor.execute(sql, (param,))`.

### [CRITICAL] God Class
- **File:** models/pedido.py:1-150
- **Description:** Single file handles order creation, item insertion, inventory updates, report generation, and status management.
- **Impact:** Tight coupling, impossible to test components in isolation.
- **Recommendation:** Split into `OrderService`, `InventoryService`, `ReportService`.

### [HIGH] Hardcoded Secret Key
- **File:** app.py:8
- **Description:** `SECRET_KEY` hardcoded as string literal.
- **Impact:** Risk of credential leakage in VCS.
- **Recommendation:** Use `os.getenv('SECRET_KEY')` with `.env` file.

### [MEDIUM] Lack of structured logging
- **File:** controllers/pedido_controller.py
- **Description:** Usage of `print()` for critical application flow events.
- **Impact:** No traceability in production environments.
- **Recommendation:** Use standard library `logging` module with structured formatting.

### [LOW] Magic Numbers in Business Logic
- **File:** models/pedido.py:120-130
- **Description:** Hardcoded discount thresholds (1000, 5000, 10000).
- **Impact:** Fragile code; hard to change business rules.
- **Recommendation:** Define thresholds in configuration constants.
