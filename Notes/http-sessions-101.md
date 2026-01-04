**Planning tutorial structure**

I’m thinking we need a well-organized tutorial covering both synchronous and asynchronous requests. I'll break it down into sections — we’ll start with an introduction to sessions. Then, I’ll explain how requests.Session works in sync, followed by how to use async sessions with httpx. I also want to include best practices and FastAPI examples. Finally, I'll touch on common mistakes and offer tips. I'll try to keep it clear, efficient, and concise, with a max of 6 sections for simplicity!
# Http sessions in Python: requests and httpx

You've got the right instinct: sessions make HTTP practical. They keep state and reuse connections, which saves time and reduces boilerplate. Let’s build this up step by step, then cement it with FastAPI sync and async examples.

---

## What an HTTP session is

- **Core idea:** A “session” stores state and resources across multiple requests to the same server.
- **State kept:** Cookies, headers, auth, proxies, and configuration (e.g., timeouts).
- **Performance:** Reuses TCP connections (connection pooling), reducing latency and CPU.
- **Ergonomics:** Central place to set defaults (headers, retries) instead of repeating per request.

---

## Synchronous sessions with requests.Session

### Why use requests.Session
- **Connection reuse:** Keep-alive reduces handshake overhead.
- **Shared config:** Set headers, cookies, auth, and timeouts once.
- **Better reliability:** Attach retry logic to the adapter; handle transient errors gracefully.

### Step-by-step usage

#### 1) Create a session and set defaults
```python
import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "my-app/1.0",
    "Accept": "application/json",
})
session.cookies.set("experiment", "A")  # example cookie
```

#### 2) Reuse the session for multiple requests
```python
# GET with query params
resp = session.get("https://httpbin.org/get", params={"q": "python"}, timeout=10)
print(resp.status_code, resp.json())

# POST with JSON
data = {"name": "Ada", "role": "engineer"}
resp = session.post("https://httpbin.org/post", json=data, timeout=10)
print(resp.status_code, resp.json())
```

#### 3) Add retry logic via adapters
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)

session.mount("http://", adapter)
session.mount("https://", adapter)
```

#### 4) Use context manager to ensure cleanup
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)

with requests.Session() as s:
    s.headers.update({"User-Agent": "my-app/1.0"})
    s.mount("https://", adapter)

    r1 = s.get("https://httpbin.org/get", timeout=10)
    r2 = s.post("https://httpbin.org/post", json={"hello": "world"}, timeout=10)

    print(r1.ok, r2.ok)
# Session closes automatically here
```

---

## Asynchronous sessions with httpx.AsyncClient

Requests is synchronous. For async, prefer httpx—it mirrors requests’ API but supports async, connection pooling, timeouts, and retries (via transport or custom logic).

### Why use httpx.AsyncClient
- **True concurrency:** Run many HTTP calls without blocking the event loop.
- **Efficient pooling:** Reuses connections across concurrent tasks.
- **Feature parity:** Headers, cookies, auth, streaming, HTTP/2.

### Step-by-step usage

#### 1) Create an AsyncClient with defaults
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient(
        headers={"User-Agent": "my-async-app/1.0", "Accept": "application/json"},
        timeout=httpx.Timeout(10.0, connect=5.0),
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
        follow_redirects=True,
        http2=True,
    ) as client:
        resp = await client.get("https://httpbin.org/get", params={"q": "async"})
        print(resp.status_code, resp.json())

asyncio.run(main())
```

#### 2) Concurrent requests with asyncio.gather
```python
import httpx
import asyncio

async def fetch(client, url):
    r = await client.get(url)
    return url, r.status_code

async def run():
    urls = [f"https://httpbin.org/delay/{i}" for i in [1,2,3]]
    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(*(fetch(client, u) for u in urls))
        print(dict(results))  # {'.../delay/1': 200, '.../delay/2': 200, ...}

asyncio.run(run())
```

#### 3) Simple retry strategy for transient errors
```python
import httpx
import asyncio
import random

async def get_with_retry(client, url, retries=3, backoff=0.5):
    for attempt in range(1, retries + 1):
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt == retries:
                raise
            await asyncio.sleep(backoff * attempt + random.uniform(0, 0.2))

async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await get_with_retry(client, "https://httpbin.org/status/503", retries=3)
        print(r.status_code)

# asyncio.run(main())
```

---

## FastAPI examples: sync and async

We’ll use sessions/clients as dependencies. Best practice: create them once, reuse via dependency injection, and close them on app shutdown.

### Sync FastAPI with requests.Session
```python
from fastapi import FastAPI, Depends
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = FastAPI()

def get_session():
    retry = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)

    s = requests.Session()
    s.headers.update({"User-Agent": "fastapi-sync/1.0"})
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

@app.get("/sync-external")
def sync_external(session: requests.Session = Depends(get_session)):
    r = session.get("https://httpbin.org/get", timeout=10)
    r.raise_for_status()
    data = r.json()
    return {"ok": True, "origin": data.get("origin"), "headers": data.get("headers")}
```

- **Note:** This dependency creates a session per request. For high throughput, create once and reuse globally. You can store a single session in app.state at startup and close at shutdown.

#### Reuse a single session with lifespan
```python
from fastapi import FastAPI

def create_session():
    s = requests.Session()
    s.headers.update({"User-Agent": "fastapi-sync/1.0"})
    return s

app = FastAPI()

@app.on_event("startup")
def startup():
    app.state.session = create_session()

@app.on_event("shutdown")
def shutdown():
    app.state.session.close()

@app.get("/sync-external-2")
def sync_external_2():
    r = app.state.session.get("https://httpbin.org/get", timeout=10)
    r.raise_for_status()
    return r.json()
```

### Async FastAPI with httpx.AsyncClient (best practices)

- **Create once, reuse:** Build AsyncClient at startup, close at shutdown.
- **Set timeouts and limits:** Prevent resource exhaustion.
- **Use dependency injection:** Provide client to route handlers.
- **Use HTTP/2 and keep-alive:** Better throughput for many small requests.
- **Add simple retries for transient errors.**

```python
from fastapi import FastAPI, Depends, HTTPException
import httpx
import asyncio

app = FastAPI()

async def create_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        headers={"User-Agent": "fastapi-async/1.0", "Accept": "application/json"},
        timeout=httpx.Timeout(10.0, connect=5.0),
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
        follow_redirects=True,
        http2=True,
    )

@app.on_event("startup")
async def startup():
    app.state.client = await create_async_client()

@app.on_event("shutdown")
async def shutdown():
    await app.state.client.aclose()

def get_client() -> httpx.AsyncClient:
    return app.state.client

async def get_with_retry(client: httpx.AsyncClient, url: str, retries: int = 3, backoff: float = 0.3):
    for attempt in range(1, retries + 1):
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp
        except (httpx.RequestError, httpx.HTTPStatusError):
            if attempt == retries:
                raise
            await asyncio.sleep(backoff * attempt)

@app.get("/async-external")
async def async_external(client: httpx.AsyncClient = Depends(get_client)):
    try:
        resp = await get_with_retry(client, "https://httpbin.org/get")
        data = resp.json()
        return {"ok": True, "origin": data.get("origin"), "headers": data.get("headers")}
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        # Map network/HTTP errors to a 502 response
        raise HTTPException(status_code=502, detail=str(e))
```

#### Concurrent calls inside a single request
```python
from fastapi import FastAPI, Depends
import httpx
import asyncio

app = FastAPI()

# ... reuse startup/shutdown and get_client from previous snippet ...

async def fetch(client: httpx.AsyncClient, url: str):
    r = await client.get(url)
    r.raise_for_status()
    return url, r.json()

@app.get("/fan-out")
async def fan_out(client: httpx.AsyncClient = Depends(get_client)):
    urls = [
        "https://httpbin.org/get?i=1",
        "https://httpbin.org/get?i=2",
        "https://httpbin.org/get?i=3",
    ]
    results = await asyncio.gather(*(fetch(client, u) for u in urls), return_exceptions=True)

    # Collect successes and errors
    successes = {u: data for (u, data) in [r for r in results if not isinstance(r, Exception)]}
    errors = [str(e) for e in results if isinstance(e, Exception)]

    return {"successes": successes, "errors": errors}
```

---

## Pitfalls and pro tips

- **Always set timeouts:** Default timeouts can be infinite; set sensible values.
  - **Requests:** `timeout=10`
  - **httpx:** `timeout=httpx.Timeout(10.0, connect=5.0)`
- **Retry only idempotent methods:** Be careful retrying POST unless your API is safe for retries.
- **Close clients:** Use context managers or app lifecycle hooks to avoid leaked sockets.
- **Limit concurrency:** Use semaphore or httpx limits to prevent exhausting file descriptors.
- **Share default headers:** Set a clear User-Agent; helps server operators and debugging.
- **Error mapping:** Convert transport errors to HTTP errors in FastAPI for consistent responses.

---

## Quick mental model

- **Session/Client = state + pooled connections.**
- **Sync (requests.Session) = simple, robust for scripts and small services.**
- **Async (httpx.AsyncClient) = scalable for high concurrency in FastAPI/async apps.**
- **In FastAPI: create once, inject everywhere, and close cleanly.**

If you want, tell me your real API target and constraints (throughput, latency, auth), and I’ll tailor the setup—timeouts, retries, and concurrency—to your use case.
