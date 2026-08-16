================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask
Files:   18 analyzed | ~550 lines of code

## Summary
CRITICAL: 1 | HIGH: 2 | MEDIUM: 1 | LOW: 1

## Findings

### [CRITICAL] Hardcoded SMTP Credentials
- **File:** services/notification_service.py:8-9
- **Description:** Gmail password `senha123` hardcoded for SMTP connection.
- **Impact:** Complete exposure of email account credentials.
- **Recommendation:** Use environment variables for SMTP password.

### [HIGH] Fat Controller
- **File:** routes/task_routes.py:10-100
- **Description:** Route definitions contain heavy business logic (task status checks, date validation, email dispatching).
- **Impact:** Violates MVC; business logic not reusable or testable.
- **Recommendation:** Move business logic to dedicated `TaskService`.

### [HIGH] Hardcoded Secret Key
- **File:** app.py:14
- **Description:** `SECRET_KEY` hardcoded.
- **Impact:** Session vulnerability.
- **Recommendation:** Use `.env`.

### [MEDIUM] Bare Except Clause
- **File:** routes/task_routes.py:30-40
- **Description:** `try...except:` capturing all errors with no logging.
- **Impact:** Root cause of failures invisible.
- **Recommendation:** Capture specific exceptions and log stack traces.

### [LOW] Outdated API Usage
- **File:** routes/task_routes.py:50
- **Description:** Uses `datetime.utcnow()` (deprecated in Python 3.12).
- **Impact:** Potential timezone bugs.
- **Recommendation:** Use `datetime.now(timezone.utc)`.
