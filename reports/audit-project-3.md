================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask
Files:   18 analyzed | ~550 lines of code

## Summary
CRITICAL: 1 | HIGH: 1 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] Hardcoded SMTP Credentials
- **File:** services/notification_service.py:8-9
- **Description:** Gmail password in plain text.
- **Impact:** Credential exposure.
- **Recommendation:** Use environment variables.

### [HIGH] Fat Controller
- **File:** routes/task_routes.py:10-100
- **Description:** Logic mixed with routing.
- **Impact:** Not testable.
- **Recommendation:** Move to `TaskService`.

### [MEDIUM] Bare Except Clause
- **File:** routes/task_routes.py:30-40
- **Description:** Swallows all errors.
- **Impact:** Debugging impossible.
- **Recommendation:** Capture specific exceptions.

### [MEDIUM] Hardcoded Secret Key
- **File:** app.py:14
- **Description:** `SECRET_KEY` hardcoded.
- **Impact:** Session compromise.
- **Recommendation:** Use `.env`.

### [LOW] Outdated API Usage
- **File:** routes/task_routes.py:50
- **Description:** `datetime.utcnow()` usage.
- **Impact:** Timezone inconsistency.
- **Recommendation:** Use `datetime.now(timezone.utc)`.

### [LOW] Missing Type Hints
- **File:** services/task_service.py
- **Description:** No type annotations.
- **Impact:** Low maintainability.
- **Recommendation:** Add type hints.
