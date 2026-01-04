**Quick summary:** **`curl` is a command-line tool for transferring data over URLs;** learn its core flags (`-X`, `-H`, `-d`, `-F`, `-u`, `-b`, `-c`, `--cookie-jar`, `-v`) and combine them to set headers, auth, files, params, cookies, and sessions. The examples below take you from zero to advanced usage step by step.

---

### Basics
**What `curl` does**  
`curl` issues network requests (HTTP, HTTPS, FTP, etc.) from the terminal. It’s **installed by default on most Unix systems** and available for Windows.

**Simple GET request**
```bash
curl https://api.example.com/resource
```
**Show response headers and body**
```bash
curl -i https://api.example.com/resource
```

---

### HTTP methods and query parameters
**Change method**
```bash
curl -X POST https://api.example.com/items
```
**Add query params** (URL-encode or let shell expand)
```bash
curl "https://api.example.com/search?q=term&page=2"
```

---

### Headers and content types
**Set a header**
```bash
curl -H "Accept: application/json" -H "X-Trace: 123" https://api.example.com
```
**Common header use cases**: `Content-Type`, `Accept`, `Authorization`. You can pass multiple headers by repeating `-H`.  
**Inspect request and response headers** with `-v` or `--trace-ascii` for deeper debugging.
```bash
curl -v -H "Accept: application/json" https://api.example.com
```

---

### Authentication
**Basic auth**
```bash
curl -u username:password https://api.example.com/secure
```
**Bearer token**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/secure
```
**Client certificates**
```bash
curl --cert client.pem --key client.key https://secure.example.com
```

---

### Sending data and files
**Form-encoded POST**
```bash
curl -X POST -d "name=alice&age=30" -H "Content-Type: application/x-www-form-urlencoded" https://api.example.com/users
```
**JSON body**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' https://api.example.com/users
```
**Multipart file upload**
```bash
curl -F "file=@/path/to/photo.jpg" -F "desc=profile" https://api.example.com/upload
```

---

### Cookies sessions and persistence
**Send a cookie**
```bash
curl -b "sessionid=abc123" https://api.example.com
```
**Save cookies to a jar and reuse**
```bash
curl -c cookies.txt -d "user=me&pass=secret" https://site.example.com/login
curl -b cookies.txt https://site.example.com/dashboard
```
Use `--cookie-jar` to persist cookies across runs; this is how you maintain sessions programmatically.

---

### Advanced tips and debugging
- **Follow redirects**: `-L`.  
- **Silent mode**: `-s` (combine with `-S` to show errors).  
- **Output to file**: `-o filename` or `-O` to use remote name.  
- **Verbose trace**: `-v` or `--trace-ascii trace.txt` for full request/response details.  
- **Combine flags**: build scripts that export tokens and reuse them: `TOKEN=$(curl -s -X POST ... | jq -r .token)` then `curl -H "Authorization: Bearer $TOKEN" ...`.

---

### Final checklist to master `curl`
- **Know the core flags**: `-X`, `-H`, `-d`, `-F`, `-u`, `-b`, `-c`, `-L`, `-v`.  
- **Always set `Content-Type`** when sending bodies.  
- **Use cookie jars** to persist sessions.  
- **Use `-v` or `--trace`** to debug headers and TLS.  
- **Script safely**: avoid exposing secrets on command lines in shared environments.
