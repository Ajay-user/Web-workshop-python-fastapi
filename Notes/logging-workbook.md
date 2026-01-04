**Setting up Python logging**

I’m detailing Python logging in stages, from basics like importing to advanced techniques such as structured logging and exception handling, ensuring clear, engaging, and practical guidance throughout.
# A Gentle Journey Through Python’s Logging Module

Welcome to your step-by-step guide on mastering Python logging. We’ll start with the absolute basics—replacing `print()` with log calls—and steadily build up to advanced configurations, structured logging, and best practices you can adopt in real‐world projects.

---

## 1. Why Use Logging Instead of print()

Logging gives you control, context, and flexibility beyond what `print()` can offer:

- Control over what messages appear (by severity level)  
- Automatic metadata (timestamps, module names, line numbers)  
- Multiple destinations (console, files, remote systems)  
- Ability to disable or reconfigure output without touching business logic  

---

## 2. Basic Setup: import, basicConfig, and log levels

Every logging session begins the same way:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)s :: %(message)s"
)

logger = logging.getLogger(__name__)

logger.debug("This is a DEBUG message")    # Won’t show at INFO level
logger.info("Starting calculation")       # Shows up
logger.warning("This is a WARNING")      # Shows up
logger.error("An ERROR occurred")        # Shows up
logger.critical("CRITICAL failure!")      # Shows up
```

- `level` sets the minimum severity to output  
- `format` defines each log line’s layout  

---

## 3. Named Loggers and Hierarchy

Avoid the root logger for better control. Instead, in each module use:

```python
# in my_module.py

import logging
logger = logging.getLogger(__name__)

def greet(name):
    logger.info("Greeting %s", name)
```

Naming by `__name__` gives you a hierarchy reflecting your package structure. You can fine-tune each module’s verbosity independently.

---

## 4. Handlers and Formatters

Handlers decide *where* logs go. Formatters decide *how* they look.

```python
import logging

# Create your logger
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))

# File handler
fh = logging.FileHandler("app.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

# Attach handlers
logger.addHandler(ch)
logger.addHandler(fh)

logger.debug("Debug goes only to file")
logger.info("Info goes to both console and file")
```

- Use `StreamHandler` for console  
- Use `FileHandler` (or `RotatingFileHandler`) for files  
- Each handler can have its own level and format  






---

## 5. Log Rotation to Manage File Size

```
By default, the file grows indefinitely. 
You can specify particular values of maxBytes and backupCount to allow the file to rollover at a predetermined size.

Rollover occurs whenever the current log file is nearly maxBytes in length. 
If backupCount is >= 1, the system will successively create new files with the same pathname as the base file, but with extensions ".1", ".2" etc. appended to it.
For example, with a backupCount of 5 and a base file name of "app.log", you would get "app.log", "app.log.1", "app.log.2", ... through to "app.log.5". 
The file being written to is always "app.log" - when it gets filled up, it is closed and renamed to "app.log.1", 
and if files "app.log.1", "app.log.2" etc. exist, then they are renamed to "app.log.2", "app.log.3" etc. respectively.

If maxBytes is zero, rollover never occurs.
```

Prevent logs from growing unbounded:

```python
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("rotator")
logger.setLevel(logging.INFO)

rotating_handler = RotatingFileHandler(
    "rotating.log",
    maxBytes=5_000_000,    # rotate after 5 MB
    backupCount=3          # keep last 3 files
)
rotating_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)
logger.addHandler(rotating_handler)

for i in range(10_000):
    logger.info("Line %d", i)
```

---

## 6. Advanced Configuration with dictConfig

For complex setups, centralize your config in a dictionary:

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "full.log",
            "level": "DEBUG"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info("Logging configured via dictConfig")
```

**Setting "disable_existing_loggers"**: 
- False in your logging configuration ensures that any loggers already created before this configuration is applied will continue to work. 
🧠 Summary
- "disable_existing_loggers": False preserves logging from libraries like requests.
- "disable_existing_loggers": True silences them unless you explicitly reconfigure their loggers.



✅ Why Set propagate: False
In your config, you're configuring the root logger ("") with two handlers: console and file. By setting propagate: False, you're saying:
- Don't pass messages up to any higher-level loggers (which in the case of the root logger, would be the default global logger).
- This avoids duplicate logging, where the same message could be handled multiple times by different handlers.
- It gives you full control over which handlers process the log messages.
🧠 Summary
You're using "propagate": False to:
- Prevent duplicate log entries.
- Ensure only the specified handlers (console and file) process the logs.
- Keep your logging clean and predictable.





```python

import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "full.log",
            "level": "DEBUG"
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "myapp.module": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False  # try changing this to True later
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("myapp.module")
logger.info("This is a test message from myapp.module")
```


- With propagate: False on "myapp.module":
    - The message is handled only by the console handler attached to "myapp.module".
    - It does not bubble up to the root logger, so it won't be written to full.log.
    - If you change "propagate": True on "myapp.module":
    - The message is handled by "myapp.module"'s console handler and by the root logger's handlers.
    - So you'll see the message printed to the console twice (once by each handler) and also written to full.log.





---

## 7. Structured Logging (JSON)

Structured logs let machines parse your logs easily:

```python
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        return json.dumps(entry)

logger = logging.getLogger("structured")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User login", extra={"user_id": 42, "ip": "192.168.0.1"})
```

---

## 8. Exception Logging

Capture stack traces without manual `traceback` calls:

```python
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Division by zero encountered")
```

`logger.exception()` logs at `ERROR` level and appends the full traceback.

---

## 9. Filters and Contextual Data

Filters let you screen or augment records:

```python
class RequestFilter(logging.Filter):
    def filter(self, record):
        record.request_id = "abc123"   # add custom field
        return True

handler.addFilter(RequestFilter())
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s [%(request_id)s] %(message)s"
))
```

You can also pass `extra` dicts to individual log calls for per-message context.

---

## 10. Thread- and Process-Safe Logging

Use a `QueueHandler` + `QueueListener` for concurrent apps:

```python
import logging
import multiprocessing
from logging.handlers import QueueHandler, QueueListener
from queue import SimpleQueue

def setup_logging():
    log_queue = SimpleQueue()
    qh = QueueHandler(log_queue)
    root = logging.getLogger()
    root.addHandler(qh)
    listener = QueueListener(log_queue, logging.StreamHandler())
    listener.start()
    root.setLevel(logging.DEBUG)
    return listener

listener = setup_logging()
logger = logging.getLogger("worker")

def worker():
    logger.info("Running in process")

procs = [multiprocessing.Process(target=worker) for _ in range(4)]
for p in procs: p.start()
for p in procs: p.join()
listener.stop()
```



This code is about **safe logging in a multi-process environment**, like when you're using `multiprocessing`.

---

### 🧠 Why This Is Needed

In Python, each process has its own memory space. So if multiple processes try to write to the same log file or stream at the same time, you can get:
- **Garbled logs**
- **Race conditions**
- **File corruption**

To avoid this, we use a **logging queue**: each process sends its log messages to a shared queue, and a single listener thread handles writing them out.

---

### 🧩 What Each Part Does

#### 1. **`SimpleQueue()`**
Creates a thread- and process-safe queue for log messages.

#### 2. **`QueueHandler(log_queue)`**
This handler sends log records into the queue instead of writing them directly.

#### 3. **`QueueListener(log_queue, StreamHandler())`**
This listener pulls log records from the queue and sends them to the `StreamHandler` (which prints to console). You could also use a `FileHandler` here to write to a file.

#### 4. **`setup_logging()`**
Sets up the root logger to use the `QueueHandler`, starts the listener, and sets the log level.

#### 5. **`worker()`**
This is the function that each process runs. It logs a message using the logger named `"worker"`.

#### 6. **`multiprocessing.Process(...)`**
Spawns 4 separate processes, each running `worker()`.

---

### 🖨️ What Happens When You Run It

Each process logs `"Running in process"` using the `"worker"` logger. Instead of writing directly to stdout or a file, the message is sent to the queue. The `QueueListener` running in the main process picks up each message and prints it.

So your output might look like:

```
INFO:worker:Running in process
INFO:worker:Running in process
INFO:worker:Running in process
INFO:worker:Running in process
```

Each line is safely handled by the listener, avoiding any concurrency issues.

---


---

## 11. Best Practices Recap

- Always get loggers via `logging.getLogger(__name__)`  
- Configure logging once at application startup  
- Use appropriate levels (DEBUG vs INFO vs WARNING…)  
- Keep log messages structured and contextual  
- Rotate files in production to avoid disk bloat  
- Capture exceptions with `logger.exception()`  
- Centralize complex configs via `dictConfig` or external files  
- Consider structured (JSON) output for log aggregation  

---

## 12. Next Steps and Related Topics

As you grow more comfortable, explore:

- Integrating with monitoring systems (ELK, Splunk, CloudWatch)  
- Using libraries like `structlog` for richer event-driven logs  
- Configuring logging in web frameworks (Django, Flask, FastAPI)  
- Correlating logs with distributed tracing (OpenTelemetry)  
- Redacting or masking sensitive data automatically  

Dive into these areas next to turn basic log calls into a full observability stack. Happy logging!











**when to use `multiprocessing.Process`, `ProcessPoolExecutor`, or `asyncio.run_in_executor`**, with examples 

---

## 🧠 The Big Picture

| Method                     | Type         | Best For                        | Parallelism | Blocking? |
|---------------------------|--------------|----------------------------------|-------------|-----------|
| `multiprocessing.Process` | Manual setup | Full control over processes      | ✅ Yes       | ✅ Yes     |
| `ProcessPoolExecutor`     | High-level   | CPU-bound tasks, parallel loops | ✅ Yes       | ❌ No      |
| `asyncio.run_in_executor` | Async I/O    | I/O-bound tasks in async code   | ❌ No        | ❌ No      |

---

## 🔧 1. `multiprocessing.Process`: Manual, Low-Level Control

Use this when you need **fine-grained control** over each process.

```python
from multiprocessing import Process

def task(name):
    print(f"Hello from {name}")

p1 = Process(target=task, args=("Process 1",))
p2 = Process(target=task, args=("Process 2",))

p1.start()
p2.start()

p1.join()
p2.join()
```

✅ Great for:
- Custom process behavior
- Logging, IPC, or shared memory
- Teaching or debugging concurrency

---

## 🚀 2. `ProcessPoolExecutor`: High-Level, Parallel Execution

Use this for **CPU-bound tasks** like data crunching or image processing.

```python
from concurrent.futures import ProcessPoolExecutor

def square(n):
    return n * n

with ProcessPoolExecutor() as executor:
    results = executor.map(square, [1, 2, 3, 4])
    print(list(results))  # [1, 4, 9, 16]
```

✅ Great for:
- Parallelizing loops
- Clean syntax
- Automatic process management

---

## 🌐 3. `asyncio.run_in_executor`: Async-Friendly for I/O Tasks

Use this when you're in an `asyncio` app and need to run **blocking code** (like file I/O or network calls) without freezing the event loop.

```python
import asyncio
import time

def blocking_task():
    time.sleep(2)
    return "Done"

async def main():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, blocking_task)
    print(result)

asyncio.run(main())
```

✅ Great for:
- Mixing async and sync code
- Avoiding thread/process overhead for lightweight tasks

---

## 🧩 Which Should You Use?

- **Need raw control?** → `multiprocessing.Process`
- **Need parallelism for CPU-heavy work?** → `ProcessPoolExecutor`
- **Need async compatibility for blocking I/O?** → `run_in_executor`

---

