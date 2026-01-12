# HTTP - HyperText Transfer Protocol

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [HTTP কী?](#http-কী)
3. [HTTP কীভাবে কাজ করে](#http-কীভাবে-কাজ-করে)
4. [HTTP Request](#http-request)
5. [HTTP Response](#http-response)
6. [HTTP Methods](#http-methods)
7. [HTTP Headers](#http-headers)
8. [HTTP Status Codes](#http-status-codes)
9. [HTTP Versions](#http-versions)
10. [HTTPS - Secure HTTP](#https---secure-http)
11. [HTTP Cookies](#http-cookies)
12. [HTTP Caching](#http-caching)
13. [HTTP Authentication](#http-authentication)
14. [Best Practices](#best-practices)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **HTTP কী?** - Basic understanding
2. ⭐⭐⭐ **HTTP কীভাবে কাজ করে** - Request-Response cycle
3. ⭐⭐⭐ **HTTP Methods** - GET, POST, PUT, DELETE
4. ⭐⭐⭐ **HTTP Status Codes** - 200, 404, 500
5. ⭐⭐⭐ **HTTP Headers** - Common headers

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **HTTP Request Structure**
7. ⭐⭐ **HTTP Response Structure**
8. ⭐⭐ **HTTPS** - Security
9. ⭐⭐ **HTTP Cookies** - Session management
10. ⭐⭐ **HTTP Caching** - Performance

### শেষে পড়ুন (Advanced):

11. ⭐ **HTTP Versions** - HTTP/1.1, HTTP/2, HTTP/3
12. ⭐ **HTTP Authentication** - Basic, Bearer, Digest
13. ⭐ **Advanced Headers** - CORS, CSP

---

## পরিচিতি

HTTP হলো internet এর foundation - যেভাবে browsers এবং servers communicate করে।

### সহজ উদাহরণ:

```
আপনি: "আমাকে google.com দেখাও"
Browser: GET /index.html HTTP/1.1 (Request পাঠায়)
Server: 200 OK + HTML content (Response পাঠায়)
Browser: HTML render করে আপনাকে দেখায়
```

---

## HTTP কী?

### Definition:

**HTTP (HyperText Transfer Protocol)** হলো একটি protocol যা web browsers এবং web servers এর মধ্যে data transfer করে।

**সহজ ভাষায়:** HTTP হলো একটি language/rules যা browser এবং server একে অপরের সাথে কথা বলতে ব্যবহার করে।

### Real-World তুলনা:

```
HTTP = Postal System

আপনি চিঠি লিখেন (Request):
- প্রাপকের ঠিকানা (URL)
- আপনার ঠিকানা (Origin)
- চিঠির বিষয়বস্তু (Body)

পোস্ট অফিস পৌঁছে দেয় (Internet)

প্রাপক উত্তর পাঠায় (Response):
- উত্তরের বিষয়বস্তু (Body)
- স্ট্যাটাস (পেয়েছি/পাইনি)
```

### HTTP এর বৈশিষ্ট্য:

| বৈশিষ্ট্য | বর্ণনা |
|----------|--------|
| **Stateless** | প্রতিটি request independent, server previous request মনে রাখে না |
| **Text-based** | Human-readable format |
| **Request-Response** | Client request করে, server response দেয় |
| **Application Layer** | OSI model এর layer 7 |
| **Port 80** | Default HTTP port (HTTPS: 443) |

---

## HTTP কীভাবে কাজ করে

### Request-Response Cycle:

```
1. User: Browser এ URL type করে
   ↓
2. Browser: DNS lookup করে IP address খুঁজে
   ↓
3. Browser: Server এর সাথে TCP connection তৈরি করে
   ↓
4. Browser: HTTP Request পাঠায়
   ↓
5. Server: Request process করে
   ↓
6. Server: HTTP Response পাঠায়
   ↓
7. Browser: Response render করে
   ↓
8. User: Page দেখে
```

### বিস্তারিত Example:

```
User: https://example.com/articles টাইপ করে

1. DNS Lookup:
   example.com → 93.184.216.34

2. TCP Connection:
   Browser → Server (Port 443 for HTTPS)

3. HTTP Request:
   GET /articles HTTP/1.1
   Host: example.com
   User-Agent: Mozilla/5.0...
   Accept: text/html

4. Server Processing:
   - Route matching
   - Database query
   - HTML generation

5. HTTP Response:
   HTTP/1.1 200 OK
   Content-Type: text/html
   Content-Length: 1234
   
   <html>...</html>

6. Browser Rendering:
   - Parse HTML
   - Load CSS/JS
   - Display page
```

---

## HTTP Request

HTTP Request এর structure:

### Request Format:

```
[Method] [Path] [HTTP Version]
[Headers]

[Body]
```

### Example Request:

```http
POST /api/articles HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Length: 58

{
  "title": "My Article",
  "content": "Article content"
}
```

### Request Components:

#### 1. Request Line:

```http
GET /api/articles?page=1 HTTP/1.1
│   │                    │
│   │                    └─ HTTP Version
│   └────────────────────── Path + Query String
└────────────────────────── HTTP Method
```

#### 2. Request Headers:

```http
Host: api.example.com              # Server address
User-Agent: Mozilla/5.0...         # Client info
Accept: application/json           # Expected response format
Content-Type: application/json     # Request body format
Authorization: Bearer token123     # Authentication
Cookie: sessionid=abc123           # Session cookie
```

#### 3. Request Body (Optional):

```json
{
  "username": "john",
  "email": "john@example.com"
}
```

### Request Methods বিস্তারিত পরে আসবে।

---

## HTTP Response

HTTP Response এর structure:

### Response Format:

```
[HTTP Version] [Status Code] [Status Message]
[Headers]

[Body]
```

### Example Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 156
Cache-Control: max-age=3600
Set-Cookie: sessionid=xyz789; HttpOnly

{
  "id": 1,
  "title": "My Article",
  "content": "Article content",
  "created_at": "2026-01-12T10:00:00Z"
}
```

### Response Components:

#### 1. Status Line:

```http
HTTP/1.1 200 OK
│        │   │
│        │   └─ Status Message
│        └───── Status Code
└────────────── HTTP Version
```

#### 2. Response Headers:

```http
Content-Type: application/json        # Response format
Content-Length: 156                   # Body size in bytes
Cache-Control: max-age=3600          # Caching rules
Set-Cookie: sessionid=xyz; HttpOnly  # Set cookie
Access-Control-Allow-Origin: *       # CORS
```

#### 3. Response Body:

```json
{
  "data": "Response data here"
}
```

---

## HTTP Methods

HTTP Methods (বা HTTP Verbs) বলে দেয় কী action করতে হবে।

### Common Methods:

| Method | কাজ | Safe? | Idempotent? | Body? |
|--------|-----|-------|-------------|-------|
| **GET** | Data retrieve | ✅ | ✅ | ❌ |
| **POST** | Data create | ❌ | ❌ | ✅ |
| **PUT** | Data replace | ❌ | ✅ | ✅ |
| **PATCH** | Data update | ❌ | ❌ | ✅ |
| **DELETE** | Data delete | ❌ | ✅ | ❌ |
| **HEAD** | Headers only | ✅ | ✅ | ❌ |
| **OPTIONS** | Available methods | ✅ | ✅ | ❌ |

### 1. GET ⭐⭐⭐

**কাজ:** Data retrieve করা।

**বৈশিষ্ট্য:**
- Safe (server state change হয় না)
- Idempotent (একই result বারবার)
- No request body
- Cacheable

**Example:**

```http
GET /api/articles?page=1&limit=10 HTTP/1.1
Host: api.example.com

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{
  "results": [...]
}
```

**Use Cases:**
- List resources
- Retrieve single resource
- Search/filter

### 2. POST ⭐⭐⭐

**কাজ:** নতুন resource তৈরি করা।

**বৈশিষ্ট্য:**
- Not safe (server state change হয়)
- Not idempotent (বারবার call করলে multiple resources)
- Has request body
- Not cacheable

**Example:**

```http
POST /api/articles HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "title": "New Article",
  "content": "Content here"
}

Response:
HTTP/1.1 201 Created
Location: /api/articles/123

{
  "id": 123,
  "title": "New Article"
}
```

**Use Cases:**
- Create new resource
- Submit form data
- Upload file

### 3. PUT ⭐⭐

**কাজ:** Resource replace করা (পুরো resource)।

**বৈশিষ্ট্য:**
- Not safe
- Idempotent (একই result)
- Has request body
- Not cacheable

**Example:**

```http
PUT /api/articles/123 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}

Response:
HTTP/1.1 200 OK

{
  "id": 123,
  "title": "Updated Title",
  "content": "Updated content"
}
```

**PUT vs POST:**
- PUT: Idempotent, replace entire resource
- POST: Not idempotent, create new resource

### 4. PATCH ⭐⭐

**কাজ:** Resource এর partial update।

**বৈশিষ্ট্য:**
- Not safe
- Not idempotent (technically)
- Has request body
- Not cacheable

**Example:**

```http
PATCH /api/articles/123 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "title": "New Title"
}

Response:
HTTP/1.1 200 OK

{
  "id": 123,
  "title": "New Title",
  "content": "Old content remains"
}
```

**PATCH vs PUT:**
- PATCH: Partial update (শুধু changed fields)
- PUT: Full replacement (সব fields)

### 5. DELETE ⭐⭐

**কাজ:** Resource delete করা।

**বৈশিষ্ট্য:**
- Not safe
- Idempotent (একবার delete হলে আবার delete করলেও same result)
- No request body
- Not cacheable

**Example:**

```http
DELETE /api/articles/123 HTTP/1.1
Host: api.example.com

Response:
HTTP/1.1 204 No Content
```

### 6. HEAD

**কাজ:** GET এর মতো কিন্তু শুধু headers, body নেই।

**Use Cases:**
- Check if resource exists
- Get metadata
- Check last modified time

**Example:**

```http
HEAD /api/articles/123 HTTP/1.1
Host: api.example.com

Response:
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1234
Last-Modified: Sun, 12 Jan 2026 10:00:00 GMT

(No body)
```

### 7. OPTIONS

**কাজ:** Server কোন methods support করে জানা।

**Use Cases:**
- CORS preflight requests
- API discovery

**Example:**

```http
OPTIONS /api/articles HTTP/1.1
Host: api.example.com

Response:
HTTP/1.1 200 OK
Allow: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
```

### Safe Methods:

**Safe = Server state change হয় না**

**কী মানে?**

Safe methods হলো এমন HTTP methods যেগুলো server এর data modify করে না। শুধু data read করে।

**কেন গুরুত্বপূর্ণ?**
- Browser automatically prefetch করতে পারে
- Cache করা যায়
- Retry করা safe (কোনো side effect নেই)

**Safe Methods:**
- GET ✅
- HEAD ✅
- OPTIONS ✅

**Not Safe:**
- POST ❌
- PUT ❌
- PATCH ❌
- DELETE ❌

**Example:**

```python
# Safe Method (GET)
GET /api/articles/
→ শুধু data read করে
→ Database change হয় না
→ বারবার call করলেও কোনো সমস্যা নেই

# Not Safe Method (POST)
POST /api/articles/
→ নতুন article তৈরি করে
→ Database change হয়
→ বারবার call করলে multiple articles তৈরি হবে
```

**Real-World তুলনা:**

```
Safe = Library থেকে বই পড়া
- বই পড়লেন (GET)
- বই unchanged থাকলো
- আবার পড়তে পারবেন

Not Safe = বই কিনে নেওয়া
- বই কিনলেন (POST)
- Library এর inventory change হলো
- আবার কিনলে duplicate হবে
```

---

### Idempotent Methods:

**Idempotent = একই request বারবার করলে same result**

**কী মানে?**

Idempotent methods হলো এমন methods যেগুলো একবার বা একাধিকবার call করলে same final state হয়।

**কেন গুরুত্বপূর্ণ?**
- Network issues হলে safely retry করা যায়
- Duplicate requests handle করা সহজ
- Reliable systems তৈরি করা যায়

**Idempotent Methods:**
- GET ✅
- PUT ✅
- DELETE ✅
- HEAD ✅
- OPTIONS ✅

**Not Idempotent:**
- POST ❌ (বারবার call করলে multiple resources তৈরি হবে)
- PATCH ❌ (technically, depends on implementation)

**Examples:**

#### GET (Idempotent ✅):

```python
# First call
GET /api/articles/5/
→ Returns article 5

# Second call (same result!)
GET /api/articles/5/
→ Returns article 5 (same data)

# 100th call (still same!)
GET /api/articles/5/
→ Returns article 5
```

#### PUT (Idempotent ✅):

```python
# First call
PUT /api/articles/5/
Body: {"title": "Updated", "content": "New content"}
→ Article 5 updated

# Second call (same result!)
PUT /api/articles/5/
Body: {"title": "Updated", "content": "New content"}
→ Article 5 still has same data (no duplicate!)

# Final state: Article 5 = {"title": "Updated", "content": "New content"}
```

#### DELETE (Idempotent ✅):

```python
# First call
DELETE /api/articles/5/
→ Article 5 deleted
→ Response: 204 No Content

# Second call (same final state!)
DELETE /api/articles/5/
→ Article 5 already deleted
→ Response: 404 Not Found (but final state same: article doesn't exist)

# Final state: Article 5 doesn't exist
```

#### POST (Not Idempotent ❌):

```python
# First call
POST /api/articles/
Body: {"title": "New Article"}
→ Article created (ID: 10)

# Second call (different result!)
POST /api/articles/
Body: {"title": "New Article"}
→ Another article created (ID: 11)

# Third call (different again!)
POST /api/articles/
Body: {"title": "New Article"}
→ Yet another article created (ID: 12)

# Final state: 3 articles with same title!
```

**Real-World তুলনা:**

```
Idempotent = Light Switch
- Switch ON করলেন → Light ON
- আবার Switch ON করলেন → Still Light ON (same state!)
- 10 বার Switch ON করলেন → Still Light ON

Not Idempotent = Adding Money to Account
- ৳100 add করলেন → Balance: ৳100
- আবার ৳100 add করলেন → Balance: ৳200 (different!)
- 10 বার ৳100 add করলেন → Balance: ৳1000 (very different!)
```

**Practical Importance:**

```python
# Scenario: Network timeout during request

# With Idempotent Method (PUT):
PUT /api/articles/5/
→ Network timeout! Did it work?
→ Retry: PUT /api/articles/5/ (same data)
→ Safe! Final state will be same

# With Non-Idempotent Method (POST):
POST /api/articles/
→ Network timeout! Did it work?
→ Retry: POST /api/articles/
→ Problem! Might create duplicate article!
→ Need to check first or use idempotency keys
```

**Summary Table:**

| Method | Safe? | Idempotent? | কেন? |
|--------|-------|-------------|------|
| GET | ✅ | ✅ | শুধু read, কোনো change নেই |
| POST | ❌ | ❌ | নতুন resource তৈরি করে, বারবার করলে duplicate |
| PUT | ❌ | ✅ | Replace করে, বারবার করলেও same final state |
| PATCH | ❌ | ❌ | Partial update, implementation dependent |
| DELETE | ❌ | ✅ | Delete করে, বারবার করলেও final state same (doesn't exist) |
| HEAD | ✅ | ✅ | GET এর মতো, শুধু headers |
| OPTIONS | ✅ | ✅ | শুধু metadata, কোনো change নেই |

---

## HTTP Headers

Headers হলো metadata যা request/response এর সাথে পাঠানো হয়।

### Header Format:

```http
Header-Name: Header-Value
```

### Common Request Headers:

#### 1. Host ⭐⭐⭐ (Required!)

```http
Host: api.example.com
```

**কাজ:** কোন server এ request যাচ্ছে।

#### 2. User-Agent

```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0
```

**কাজ:** Client information (browser, OS)।

#### 3. Accept

```http
Accept: application/json
Accept: text/html, application/json
Accept: */*
```

**কাজ:** Client কোন format চায়।

#### 4. Content-Type

```http
Content-Type: application/json
Content-Type: application/x-www-form-urlencoded
Content-Type: multipart/form-data
```

**কাজ:** Request body এর format।

#### 5. Authorization

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Authorization: Token abc123xyz
```

**কাজ:** Authentication credentials।

#### 6. Cookie

```http
Cookie: sessionid=abc123; csrftoken=xyz789
```

**কাজ:** Session/state management।

#### 7. Referer

```http
Referer: https://example.com/page1
```

**কাজ:** কোন page থেকে request এসেছে।

#### 8. Cache-Control

```http
Cache-Control: no-cache
Cache-Control: max-age=3600
```

**কাজ:** Caching behavior।

### Common Response Headers:

#### 1. Content-Type ⭐⭐⭐

```http
Content-Type: application/json; charset=utf-8
Content-Type: text/html; charset=utf-8
Content-Type: image/png
```

**কাজ:** Response body এর format।

#### 2. Content-Length

```http
Content-Length: 1234
```

**কাজ:** Response body size (bytes)।

#### 3. Set-Cookie

```http
Set-Cookie: sessionid=abc123; HttpOnly; Secure; SameSite=Strict
```

**কাজ:** Client এ cookie set করা।

#### 4. Cache-Control

```http
Cache-Control: public, max-age=3600
Cache-Control: private, no-cache
Cache-Control: no-store
```

**কাজ:** Caching rules।

#### 5. Location

```http
Location: /api/articles/123
```

**কাজ:** Redirect URL (3xx codes) বা created resource URL (201)।

#### 6. Access-Control-Allow-Origin (CORS)

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Origin: https://example.com
```

**কাজ:** Cross-origin requests allow করা।

#### 7. ETag

```http
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

**কাজ:** Resource version (caching এর জন্য)।

#### 8. Last-Modified

```http
Last-Modified: Sun, 12 Jan 2026 10:00:00 GMT
```

**কাজ:** Resource কখন modify হয়েছে।

### Custom Headers:

```http
X-Request-ID: abc-123-xyz
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-API-Version: v2
```

**Note:** Custom headers সাধারণত `X-` দিয়ে শুরু হয় (deprecated কিন্তু এখনো common)।

---

## HTTP Status Codes

Status codes বলে দেয় request এর result কী।

### Categories:

| Range | Category | অর্থ |
|-------|----------|------|
| 1xx | Informational | Processing চলছে |
| 2xx | Success | Request successful |
| 3xx | Redirection | Redirect করতে হবে |
| 4xx | Client Error | Client এর ভুল |
| 5xx | Server Error | Server এর ভুল |

### Most Common Codes:

#### 2xx Success:

- **200 OK** - Request successful
- **201 Created** - Resource created
- **204 No Content** - Successful, no response body

#### 4xx Client Errors:

- **400 Bad Request** - Invalid request
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - No permission
- **404 Not Found** - Resource not found
- **429 Too Many Requests** - Rate limit exceeded

#### 5xx Server Errors:

- **500 Internal Server Error** - Server error
- **502 Bad Gateway** - Gateway error
- **503 Service Unavailable** - Server down

**বিস্তারিত:** `status-codes.md` দেখুন।

---

## HTTP Versions

### HTTP/0.9 (1991)

- শুধু GET method
- No headers
- শুধু HTML

### HTTP/1.0 (1996)

- Headers added
- POST, HEAD methods
- Status codes
- Content-Type

### HTTP/1.1 (1997) ⭐ (Most Common)

**Features:**
- Persistent connections (keep-alive)
- Pipelining
- Chunked transfer encoding
- Host header (required)
- More methods (PUT, DELETE, etc.)

**Example:**

```http
GET /index.html HTTP/1.1
Host: example.com
Connection: keep-alive
```

### HTTP/2 (2015) ⭐ (Modern)

**Improvements:**
- Binary protocol (not text)
- Multiplexing (multiple requests in one connection)
- Header compression
- Server push
- Faster!

**Benefits:**
- Faster page loads
- Better performance
- Less latency

### HTTP/3 (2022) ⭐ (Latest)

**Features:**
- Uses QUIC (UDP-based)
- Even faster
- Better mobile performance
- Improved security

**Adoption:** Growing, major sites using it.

---

## HTTPS - Secure HTTP

HTTPS = HTTP + SSL/TLS (Encryption)

### কেন HTTPS?

1. **Encryption** - Data encrypted, কেউ read করতে পারবে না
2. **Authentication** - Server verify করা
3. **Integrity** - Data tamper হয়নি verify করা

### HTTP vs HTTPS:

| Feature | HTTP | HTTPS |
|---------|------|-------|
| Port | 80 | 443 |
| Security | ❌ | ✅ |
| Encryption | ❌ | ✅ (SSL/TLS) |
| Certificate | ❌ | ✅ Required |
| Speed | Faster | Slightly slower |
| SEO | Lower rank | Higher rank |

### HTTPS Handshake:

```
1. Client: "Hello, I want secure connection"
2. Server: "Here's my certificate"
3. Client: Verifies certificate
4. Client: Generates session key, encrypts with server's public key
5. Server: Decrypts with private key
6. Both: Use session key for encryption
7. Secure communication starts!
```

### SSL/TLS Certificate:

```
Certificate contains:
- Domain name
- Organization info
- Public key
- Expiry date
- Certificate Authority signature
```

**Certificate Authorities (CA):**
- Let's Encrypt (Free!)
- DigiCert
- Comodo

---

## HTTP Cookies

Cookies হলো small data pieces যা browser এ store হয়।

### কেন Cookies?

HTTP stateless, তাই session maintain করতে cookies লাগে।

### Cookie Format:

```http
Set-Cookie: name=value; Domain=example.com; Path=/; Expires=Wed, 09 Jun 2026 10:18:14 GMT; HttpOnly; Secure; SameSite=Strict
```

### Cookie Attributes:

| Attribute | কাজ |
|-----------|-----|
| **Domain** | কোন domain এ valid |
| **Path** | কোন path এ valid |
| **Expires** | কখন expire হবে |
| **Max-Age** | কত সেকেন্ড valid |
| **HttpOnly** | JavaScript access করতে পারবে না (XSS protection) |
| **Secure** | শুধু HTTPS এ পাঠাবে |
| **SameSite** | CSRF protection |

### Example:

```http
Response:
Set-Cookie: sessionid=abc123; HttpOnly; Secure; SameSite=Strict

Subsequent Requests:
Cookie: sessionid=abc123
```

### Cookie Types:

#### 1. Session Cookies:

```http
Set-Cookie: sessionid=abc123
```

Browser close করলে delete হয়।

#### 2. Persistent Cookies:

```http
Set-Cookie: userid=123; Max-Age=2592000
```

Specific time পর্যন্ত থাকে।

---

## HTTP Caching

Caching হলো responses store করা যাতে বারবার server এ যেতে না হয়।

### Cache-Control Header:

```http
Cache-Control: public, max-age=3600
```

### Cache Directives:

| Directive | অর্থ |
|-----------|------|
| **public** | যেকোনো cache করতে পারবে |
| **private** | শুধু browser cache করবে |
| **no-cache** | Cache করবে কিন্তু revalidate করতে হবে |
| **no-store** | Cache করবে না |
| **max-age=3600** | 3600 seconds পর্যন্ত cache |
| **must-revalidate** | Expire হলে revalidate করতে হবে |

### Example:

```http
Response:
HTTP/1.1 200 OK
Cache-Control: public, max-age=3600
ETag: "abc123"

Next Request (within 1 hour):
Browser uses cached version

After 1 hour:
GET /api/articles HTTP/1.1
If-None-Match: "abc123"

Response:
HTTP/1.1 304 Not Modified
(Browser uses cached version)
```

---

## HTTP Authentication

### 1. Basic Authentication

```http
Request:
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Format:** `username:password` base64 encoded

**⚠️ Not Secure!** শুধু HTTPS এ ব্যবহার করুন।

### 2. Bearer Token (JWT)

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Modern approach!** API authentication এর জন্য।

### 3. Digest Authentication

```http
Authorization: Digest username="user", realm="api", nonce="..."
```

**More secure than Basic** কিন্তু complex।

---

## Best Practices

### 1. Always Use HTTPS

```
❌ http://api.example.com
✅ https://api.example.com
```

### 2. Use Appropriate Methods

```
❌ GET /api/articles/delete/123
✅ DELETE /api/articles/123
```

### 3. Set Correct Headers

```http
✅ Content-Type: application/json
✅ Cache-Control: public, max-age=3600
✅ Access-Control-Allow-Origin: https://example.com
```

### 4. Use Status Codes Correctly

```
✅ 200 for successful GET
✅ 201 for successful POST
✅ 204 for successful DELETE
✅ 400 for validation errors
✅ 401 for authentication errors
```

### 5. Enable Compression

```http
Accept-Encoding: gzip, deflate, br
Content-Encoding: gzip
```

### 6. Set Security Headers

```http
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

---

## অতিরিক্ত Resources

### Official Documentation
- HTTP Specification: https://httpwg.org/specs/
- MDN HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP

### Tools
- Postman - API testing
- curl - Command line HTTP client
- Browser DevTools - Network tab

### সম্পর্কিত বিষয়
- REST API (rest.md)
- Status Codes (status-codes.md)
- Authentication (authentication.md)

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
