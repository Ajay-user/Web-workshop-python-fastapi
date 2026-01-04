

# 🐍 Python Logging Training: From Basics to Pro

## 1. Logging Basics
- **Import and configure:**
```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.debug("Debugging info")
logging.info("General info")
logging.warning("Something might be wrong")
logging.error("An error occurred")
logging.critical("Critical issue!")
```
- **Log Levels:** `DEBUG < INFO < WARNING < ERROR < CRITICAL`

---

## 2. Loggers, Handlers, and Formatters
- **Logger:** Entry point (`logging.getLogger("myapp")`)
- **Handler:** Where logs go (console, file, HTTP, etc.)
- **Formatter:** How logs look

```python
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler("app.log")
fh.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

logger.info("This goes to console and file")
```

---

## 3. Advanced Filtering
Filters let you **control which logs are processed**.

### Example: Filter by module name
```python
class ModuleFilter(logging.Filter):
    def filter(self, record):
        return "module1" in record.name

logger.addFilter(ModuleFilter())
```

### Example: Add custom fields
```python
class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_id = "U123"
        return True

logger.addFilter(ContextFilter())
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(user_id)s | %(message)s")
```

---

## 4. Multiple Handlers with Different Levels
```python
error_handler = logging.FileHandler("errors.log")
error_handler.setLevel(logging.ERROR)

debug_handler = logging.FileHandler("debug.log")
debug_handler.setLevel(logging.DEBUG)

logger.addHandler(error_handler)
logger.addHandler(debug_handler)
```
- Errors go to `errors.log`
- Debug info goes to `debug.log`

---

## 5. Structured & JSON Logging
For modern apps, logs often need to be machine-readable:
```python
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        return json.dumps(log_record)

json_handler = logging.StreamHandler()
json_handler.setFormatter(JsonFormatter())
logger.addHandler(json_handler)

logger.info("User logged in")
```

---

## 6. Best Practices
- **Use `__name__` as logger name** → helps trace modules.
- **Never use `print()` for logs** → use `logging` instead.
- **Separate handlers for error/debug/info** → easier troubleshooting.
- **Add context with filters** → user IDs, request IDs.
- **Rotate logs** with `logging.handlers.RotatingFileHandler`.

---

## 📊 Comparison Table

| Feature                | Basic Logging | Advanced Logging |
|-------------------------|---------------|-----------------|
| Levels                 | Yes           | Yes             |
| Multiple Handlers       | No            | Yes             |
| Custom Formatters       | Limited       | Flexible        |
| Filters                 | No            | Yes (customizable) |
| Structured/JSON Logs    | No            | Yes             |
| Contextual Info         | No            | Yes (via filters) |

---
Perfect — let’s build a **logging mastery toolkit** with strong, practical examples. I’ll walk you through each advanced concept with code you can run and adapt. By the end, you’ll be able to design logging setups like a pro.  

---

## Examples 
---


## 1. Log Levels in Action
```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s: %(message)s")

logging.debug("Debugging details (dev only)")
logging.info("General info for users")
logging.warning("Something looks off")
logging.error("An error occurred")
logging.critical("System is down!")
```
👉 Use levels to control verbosity. In production, you might set `level=logging.WARNING` to suppress debug/info.

---

## 2. Custom Formatters
```python
import logging

logger = logging.getLogger("custom")
handler = logging.StreamHandler()

# Custom format with timestamp, logger name, and message
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info("Custom formatted log")
```
👉 Formatters let you design log output exactly how you want.

---

## 3. Filtering Logs
```python
class ErrorOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR

logger = logging.getLogger("filter_demo")
handler = logging.StreamHandler()
handler.addFilter(ErrorOnlyFilter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug("This won't show")
logger.error("This will show")
```
👉 Filters give fine-grained control beyond just log levels.

---

## 4. Structured (JSON) Logs
```python
import logging, json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

logger = logging.getLogger("json_demo")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User logged in")
```
👉 Structured logs are machine-readable, perfect for modern observability stacks (ELK, Splunk, etc.).

---

## 5. Adding Context with Filters
```python
class ContextFilter(logging.Filter):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def filter(self, record):
        record.user_id = self.user_id
        return True

logger = logging.getLogger("context_demo")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s | %(levelname)s | user=%(user_id)s | %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addFilter(ContextFilter(user_id="U123"))
logger.setLevel(logging.INFO)

logger.info("Action performed")
```
👉 Context filters inject extra fields (like user IDs, request IDs) into every log.

---

## 6. Adding Extra Info Dynamically
```python
logger = logging.getLogger("extra_demo")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(user)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User logged in", extra={"user": "Alice"})
logger.info("User logged out", extra={"user": "Bob"})
```
👉 `extra` lets you attach ad-hoc metadata per log call.

---

## 7. Multiple Handlers (Console + File)
```python
logger = logging.getLogger("multi_handler")
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler("debug.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

logger.debug("Debug goes to file only")
logger.error("Error goes to both console and file")
```
👉 Different handlers capture different levels for different destinations.

---

