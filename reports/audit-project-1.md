================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:     Flask 3.1.1
Dependencies:  flask, flask-cors
Domain:        E-commerce API
Architecture:  Monolith with partially organized layers
Source files:  15 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================

================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   15 analyzed | ~500 lines of code

## Summary
CRITICAL: 1 | HIGH: 1 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] Raw SQL queries in data layer
- **File:** database.py:12-65
- **Description:** Direct use of sqlite3.cursor.execute with raw SQL strings.
- **Impact:** Vulnerable to SQL Injection; lacks connection management.
- **Recommendation:** Implement ORM (SQLAlchemy) and connection pooling.

### [HIGH] Monolithic routing in app.py
- **File:** app.py:1-40
- **Description:** Business logic mixed with route definitions in a single file.
- **Impact:** Poor maintainability and scalability.
- **Recommendation:** Use Flask Blueprints to separate route handling into controllers.

### [MEDIUM] Duplicated validation logic
- **File:** controllers/produto_controller.py:23-53,88-100
- **Description:** Input validation logic is repeated across POST and PUT methods.
- **Impact:** Risk of inconsistent behavior; hard to update.
- **Recommendation:** Extract validation into a dedicated schema validator class.

### [MEDIUM] No centralized error handling
- **File:** controllers/produto_controller.py:5-10
- **Description:** Each route handler uses try/except blocks returning JSON error responses manually.
- **Impact:** Repetitive code; inconsistent error format.
- **Recommendation:** Implement a global error handler middleware.

### [LOW] Hardcoded error messages
- **File:** controllers/produto_controller.py:34-45
- **Description:** Error messages are hardcoded strings in controllers.
- **Impact:** Hard to localize or maintain consistent messages.
- **Recommendation:** Use a centralized constants file or configuration for messages.

### [LOW] Missing docstrings
- **File:** controllers/usuario_controller.py, models/produto.py
- **Description:** Functions and classes lack docstrings.
- **Impact:** Low maintainability/readability.
- **Recommendation:** Add docstrings to all public methods/classes.

================================
Total: 6 findings
================================
