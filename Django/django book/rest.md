# REST - Representational State Transfer

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [REST কী?](#rest-কী)
3. [REST এর ইতিহাস](#rest-এর-ইতিহাস)
4. [REST Architectural Constraints](#rest-architectural-constraints)
5. [REST API কী?](#rest-api-কী)
6. [RESTful Design Principles](#restful-design-principles)
7. [REST vs SOAP vs GraphQL](#rest-vs-soap-vs-graphql)
8. [REST API Best Practices](#rest-api-best-practices)
9. [REST API Security](#rest-api-security)
10. [REST API Versioning](#rest-api-versioning)
11. [HATEOAS](#hateoas)
12. [Richardson Maturity Model](#richardson-maturity-model)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **REST কী?** - Basic understanding
2. ⭐⭐⭐ **REST API কী?** - Practical understanding
3. ⭐⭐⭐ **REST Architectural Constraints** - 6টি principles
4. ⭐⭐⭐ **RESTful Design Principles** - কীভাবে design করবেন
5. ⭐⭐⭐ **REST API Best Practices** - Professional APIs

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **REST vs SOAP vs GraphQL** - পার্থক্য
7. ⭐⭐ **REST API Security** - Authentication, Authorization
8. ⭐⭐ **REST API Versioning** - API evolution

### শেষে পড়ুন (Advanced):

9. ⭐ **HATEOAS** - Advanced REST concept
10. ⭐ **Richardson Maturity Model** - REST maturity levels

---

## পরিচিতি

REST হলো web services তৈরির একটি architectural style যা HTTP protocol ব্যবহার করে।

### সহজ উদাহরণ:

```
Traditional Web:
Browser → Server: "Give me the page"
Server → Browser: "Here's the HTML"

REST API:
Client → Server: "Give me user data (JSON)"
Server → Client: "Here's the JSON data"
```

---

## REST কী?

### Definition:

**REST (Representational State Transfer)** হলো একটি architectural style যা distributed systems (বিশেষত web services) design করার জন্য একটি set of constraints/principles প্রদান করে।

**সহজ ভাষায়:** REST হলো একটি guideline/rules যা বলে দেয় কীভাবে web services তৈরি করতে হবে যাতে সেগুলো scalable, maintainable এবং efficient হয়।

### Key Points:

- REST একটি **protocol নয়**, একটি **architectural style**
- HTTP protocol ব্যবহার করে (কিন্তু HTTP-only নয়)
- **Stateless** - প্রতিটি request independent
- **Resource-based** - সবকিছু resource হিসেবে treat করা হয়

### Real-World তুলনা:

```
REST = Building Architecture Guidelines

যেমন building তৈরির rules আছে:
- Foundation strong হতে হবে
- Proper ventilation লাগবে
- Fire exits থাকতে হবে

তেমনি REST এর rules:
- Stateless হতে হবে
- Client-Server separation থাকতে হবে
- Cacheable হতে হবে
```

---

## REST এর ইতিহাস

### Timeline:

**2000:** Roy Fielding তার PhD dissertation এ REST introduce করেন।

**Key Points:**
- Roy Fielding ছিলেন HTTP/1.1 specification এর co-author
- REST ছিল web এর existing architecture কে formalize করা
- Goal: Scalable, reliable, performant web services

**2000-2010:** REST popularity বাড়তে থাকে, SOAP এর alternative হিসেবে।

**2010-Present:** REST হয়ে যায় de facto standard for web APIs।

**2025-2026:** REST এখনো dominant, তবে GraphQL, gRPC ইত্যাদি specific use cases এর জন্য ব্যবহৃত হচ্ছে।

---

## REST Architectural Constraints

Roy Fielding ৬টি architectural constraints define করেছেন যা একটি system কে RESTful বানায়:

### 1. Client-Server Architecture ⭐⭐⭐

**Principle:** Client এবং Server আলাদা, independently evolve করতে পারবে।

**কাজ:**
- **Client:** User interface এবং user experience
- **Server:** Data storage এবং business logic

**সুবিধা:**
- Separation of concerns
- Independent development
- Scalability

**Example:**

```
Client (React App):
- UI rendering
- User interactions
- API calls

Server (Django REST API):
- Database operations
- Business logic
- Data validation

উভয়ে independently update করা যায়
```

### 2. Stateless ⭐⭐⭐

**Principle:** প্রতিটি request এ সব information থাকতে হবে, server কোনো client state store করবে না।

**কাজ:**
- প্রতিটি request self-contained
- Server previous requests মনে রাখে না
- Session state client এ থাকে

**সুবিধা:**
- Scalability (কোনো server যেকোনো request handle করতে পারে)
- Reliability (server crash হলেও session lost হয় না)
- Simple server logic

**Example:**

```http
# Bad - Stateful (Server remembers)
Request 1: POST /login → Server stores session
Request 2: GET /profile → Server checks stored session

# Good - Stateless (Each request has all info)
Request 1: POST /login → Returns token
Request 2: GET /profile
Authorization: Bearer token123 → Token এ সব info আছে
```

### 3. Cacheable ⭐⭐

**Principle:** Responses অবশ্যই cacheable বা non-cacheable হিসেবে define করতে হবে।

**কাজ:**
- Server response এ caching info দেয়
- Client/intermediaries cache করতে পারে
- Performance improve হয়

**সুবিধা:**
- Reduced server load
- Faster responses
- Better scalability

**Example:**

```http
Response:
HTTP/1.1 200 OK
Cache-Control: public, max-age=3600
ETag: "abc123"

{
  "data": "..."
}

# Client 1 hour পর্যন্ত cache করবে
# Server load কমবে
```

### 4. Uniform Interface ⭐⭐⭐ (Most Important!)

**Principle:** একটি uniform, consistent interface থাকতে হবে।

**৪টি Sub-Constraints:**

#### a) Resource Identification

প্রতিটি resource একটি unique URI দ্বারা identify হবে।

```
/users/123          → User with ID 123
/articles/456       → Article with ID 456
/users/123/orders   → Orders of user 123
```

#### b) Resource Manipulation Through Representations

Resources কে representations (JSON, XML) দিয়ে manipulate করা হবে।

```json
GET /users/123
{
  "id": 123,
  "name": "John",
  "email": "john@example.com"
}
```

#### c) Self-Descriptive Messages

প্রতিটি message এ যথেষ্ট information থাকবে।

```http
GET /users/123 HTTP/1.1
Host: api.example.com
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 58

{"id": 123, "name": "John"}
```

#### d) HATEOAS (Hypermedia As The Engine Of Application State)

Responses এ related resources এর links থাকবে।

```json
{
  "id": 123,
  "name": "John",
  "links": {
    "self": "/users/123",
    "orders": "/users/123/orders",
    "profile": "/users/123/profile"
  }
}
```

### 5. Layered System ⭐⭐

**Principle:** System multiple layers এ organize করা যাবে।

**কাজ:**
- Client জানে না কতগুলো layers আছে
- Intermediaries (proxies, load balancers) থাকতে পারে
- Each layer শুধু adjacent layer দেখে

**সুবিধা:**
- Security (firewalls, authentication layers)
- Load balancing
- Caching layers
- Scalability

**Example:**

```
Client
  ↓
Load Balancer
  ↓
API Gateway (Authentication, Rate Limiting)
  ↓
Application Server
  ↓
Database

Client শুধু API Gateway দেখে, বাকি layers জানে না
```

### 6. Code on Demand (Optional) ⭐

**Principle:** Server client কে executable code পাঠাতে পারে।

**কাজ:**
- Server JavaScript, applets পাঠায়
- Client execute করে

**Example:**

```html
<!-- Server পাঠায় -->
<script src="https://api.example.com/widget.js"></script>

<!-- Client execute করে -->
```

**Note:** এটি optional constraint, সবসময় ব্যবহার হয় না।

---

## REST API কী?

### Definition:

**REST API** হলো একটি API যা REST architectural constraints follow করে।

**সহজ ভাষায়:** REST API হলো একটি web service যা HTTP methods (GET, POST, PUT, DELETE) ব্যবহার করে resources এর সাথে interact করে।

### REST API এর Components:

#### 1. Resources

সবকিছু resource - users, articles, products ইত্যাদি।

```
Resources:
- Users
- Articles
- Products
- Orders
```

#### 2. URIs (Uniform Resource Identifiers)

প্রতিটি resource এর একটি unique URI।

```
/users              → All users
/users/123          → Specific user
/articles           → All articles
/articles/456       → Specific article
```

#### 3. HTTP Methods

Resources এর সাথে কী করবেন।

```
GET /users          → List users
POST /users         → Create user
GET /users/123      → Get user
PUT /users/123      → Update user
DELETE /users/123   → Delete user
```

#### 4. Representations

Resources কে JSON/XML format এ represent করা।

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```

#### 5. Status Codes

Operation এর result।

```
200 OK              → Success
201 Created         → Resource created
404 Not Found       → Resource not found
500 Server Error    → Server error
```

### REST API Example:

```
# List all users
GET /api/users
Response: 200 OK
[
  {"id": 1, "name": "John"},
  {"id": 2, "name": "Jane"}
]

# Get specific user
GET /api/users/1
Response: 200 OK
{"id": 1, "name": "John", "email": "john@example.com"}

# Create user
POST /api/users
Body: {"name": "Alice", "email": "alice@example.com"}
Response: 201 Created
{"id": 3, "name": "Alice", "email": "alice@example.com"}

# Update user
PUT /api/users/3
Body: {"name": "Alice Smith", "email": "alice@example.com"}
Response: 200 OK
{"id": 3, "name": "Alice Smith", "email": "alice@example.com"}

# Delete user
DELETE /api/users/3
Response: 204 No Content
```

---

## RESTful Design Principles

### 1. Use Nouns, Not Verbs ⭐⭐⭐

**Good:**

```
GET /users
POST /users
GET /users/123
PUT /users/123
DELETE /users/123
```

**Bad:**

```
GET /getUsers
POST /createUser
GET /getUserById/123
POST /updateUser/123
POST /deleteUser/123
```

### 2. Use Plural Nouns ⭐⭐

**Good:**

```
/users
/articles
/products
```

**Bad:**

```
/user
/article
/product
```

### 3. Use HTTP Methods Correctly ⭐⭐⭐

| Method | কাজ | Example |
|--------|-----|---------|
| GET | Retrieve | `GET /users` |
| POST | Create | `POST /users` |
| PUT | Replace | `PUT /users/123` |
| PATCH | Update | `PATCH /users/123` |
| DELETE | Delete | `DELETE /users/123` |

### 4. Use Hierarchical URIs ⭐⭐

**Good:**

```
/users/123/orders           → User's orders
/users/123/orders/456       → Specific order
/articles/789/comments      → Article's comments
```

**Bad:**

```
/getUserOrders?userId=123
/getOrderById?orderId=456&userId=123
```

### 5. Filter, Sort, Paginate ⭐⭐⭐

**Filtering:**

```
GET /users?role=admin
GET /articles?status=published&category=tech
```

**Sorting:**

```
GET /users?sort=name
GET /articles?sort=-created_at    # Descending
```

**Pagination:**

```
GET /users?page=2&limit=20
GET /articles?offset=40&limit=20
```

### 6. Use Proper Status Codes ⭐⭐⭐

```
200 OK              → Successful GET, PUT, PATCH
201 Created         → Successful POST
204 No Content      → Successful DELETE
400 Bad Request     → Validation error
401 Unauthorized    → Not authenticated
403 Forbidden       → Not authorized
404 Not Found       → Resource not found
500 Server Error    → Server error
```

### 7. Versioning ⭐⭐

**Good:**

```
/v1/users
/v2/users
```

**Alternative:**

```
Header: Accept: application/vnd.myapi.v1+json
```

### 8. Use JSON ⭐⭐⭐

**Standard format:**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2026-01-12T10:00:00Z"
}
```

### 9. Error Handling ⭐⭐

**Good:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Email is required"],
      "password": ["Password must be at least 8 characters"]
    }
  }
}
```

**Bad:**

```json
{
  "error": "Error occurred"
}
```

### 10. HATEOAS (Optional) ⭐

**Include links:**

```json
{
  "id": 123,
  "name": "John",
  "links": {
    "self": "/users/123",
    "orders": "/users/123/orders",
    "profile": "/users/123/profile"
  }
}
```

---

## RESTful vs Non-RESTful - পার্থক্য বুঝুন

**কেন গুরুত্বপূর্ণ?**

অনেকেই মনে করেন HTTP ব্যবহার করলেই REST API হয়ে যায়। কিন্তু এটা ভুল! REST এর specific principles আছে।

### RESTful API Example:

```python
# ✅ RESTful Design

# List users
GET /api/users
Response: 200 OK
[
  {"id": 1, "name": "John"},
  {"id": 2, "name": "Jane"}
]

# Get specific user
GET /api/users/1
Response: 200 OK
{"id": 1, "name": "John", "email": "john@example.com"}

# Create user
POST /api/users
Body: {"name": "Alice", "email": "alice@example.com"}
Response: 201 Created
{"id": 3, "name": "Alice"}

# Update user
PUT /api/users/3
Body: {"name": "Alice Smith", "email": "alice@example.com"}
Response: 200 OK

# Delete user
DELETE /api/users/3
Response: 204 No Content
```

**কেন RESTful?**
- ✅ Resource-based URLs (`/users`, `/users/1`)
- ✅ HTTP methods correctly used (GET, POST, PUT, DELETE)
- ✅ Proper status codes (200, 201, 204)
- ✅ Stateless (প্রতিটি request independent)
- ✅ JSON format
- ✅ Nouns, not verbs

### Non-RESTful API Example:

```python
# ❌ Non-RESTful Design

# List users (Verb in URL!)
GET /api/getUsers
Response: 200 OK
[
  {"id": 1, "name": "John"},
  {"id": 2, "name": "Jane"}
]

# Get specific user (Verb in URL!)
GET /api/getUserById?id=1
Response: 200 OK
{"id": 1, "name": "John"}

# Create user (Wrong method!)
GET /api/createUser?name=Alice&email=alice@example.com
Response: 200 OK
{"status": "success", "userId": 3}

# Update user (Wrong method!)
POST /api/updateUser
Body: {"id": 3, "name": "Alice Smith"}
Response: 200 OK
{"status": "updated"}

# Delete user (Wrong method!)
POST /api/deleteUser
Body: {"id": 3}
Response: 200 OK
{"status": "deleted"}
```

**কেন Non-RESTful?**
- ❌ Verbs in URLs (`/getUsers`, `/createUser`)
- ❌ Wrong HTTP methods (GET for create, POST for delete)
- ❌ Wrong status codes (সব 200 OK)
- ❌ Inconsistent response format
- ❌ Query parameters for resource identification

### Detailed Comparison:

| Feature | RESTful ✅ | Non-RESTful ❌ |
|---------|-----------|---------------|
| **URL Design** | `/users`, `/users/123` | `/getUsers`, `/getUserById` |
| **HTTP Methods** | GET, POST, PUT, DELETE | সব GET বা POST |
| **Status Codes** | 200, 201, 204, 404 | সব 200 |
| **Resource Focus** | Resources (nouns) | Actions (verbs) |
| **Stateless** | ✅ Yes | ❌ Often stateful |
| **Cacheable** | ✅ Yes | ❌ Difficult |
| **Scalable** | ✅ Easy | ❌ Hard |

### Real-World Examples:

#### Example 1: Blog API

**RESTful:**

```python
# Articles
GET    /api/articles          # List all articles
GET    /api/articles/5        # Get article 5
POST   /api/articles          # Create article
PUT    /api/articles/5        # Update article 5
DELETE /api/articles/5        # Delete article 5

# Comments
GET    /api/articles/5/comments      # Article 5's comments
POST   /api/articles/5/comments      # Add comment to article 5
DELETE /api/comments/10               # Delete comment 10
```

**Non-RESTful:**

```python
# Articles (Verbs everywhere!)
GET  /api/getAllArticles
GET  /api/getArticleById?id=5
POST /api/createArticle
POST /api/updateArticle
POST /api/deleteArticle

# Comments
GET  /api/getCommentsForArticle?articleId=5
POST /api/addComment
POST /api/removeComment
```

#### Example 2: E-commerce API

**RESTful:**

```python
# Products
GET    /api/products                    # List products
GET    /api/products?category=electronics  # Filter
GET    /api/products/123                # Get product
POST   /api/products                    # Create product
PUT    /api/products/123                # Update product
DELETE /api/products/123                # Delete product

# Orders
GET    /api/users/5/orders              # User's orders
POST   /api/users/5/orders              # Create order
GET    /api/orders/789                  # Get order
PUT    /api/orders/789/status           # Update order status
```

**Non-RESTful:**

```python
# Products
GET  /api/listProducts
GET  /api/searchProducts?category=electronics
GET  /api/getProduct?id=123
POST /api/addProduct
POST /api/editProduct
POST /api/removeProduct

# Orders
GET  /api/getUserOrders?userId=5
POST /api/placeOrder
GET  /api/getOrderDetails?orderId=789
POST /api/changeOrderStatus
```

### কেন RESTful Better?

#### 1. Predictable (অনুমান করা সহজ):

```python
# RESTful - Pattern বুঝলেই সব বুঝা যায়
GET    /api/products      # Obviously lists products
POST   /api/products      # Obviously creates product
GET    /api/products/5    # Obviously gets product 5
DELETE /api/products/5    # Obviously deletes product 5

# Non-RESTful - প্রতিটা endpoint মনে রাখতে হয়
GET  /api/getAllProducts
POST /api/createNewProduct
GET  /api/fetchProductDetails?id=5
POST /api/removeProductFromSystem
```

#### 2. Cacheable:

```python
# RESTful - GET requests cache করা যায়
GET /api/articles
Cache-Control: max-age=3600
→ 1 hour cache, server load কম

# Non-RESTful - POST দিয়ে read করলে cache করা যায় না
POST /api/getArticles
→ Can't cache POST requests
→ Higher server load
```

#### 3. Scalable:

```python
# RESTful - Stateless, যেকোনো server handle করতে পারে
Request 1: GET /api/users/5 → Server A
Request 2: GET /api/users/5 → Server B (same result!)

# Non-RESTful - Often stateful, specific server লাগে
Request 1: POST /api/login → Server A stores session
Request 2: POST /api/getProfile → Must go to Server A!
```

#### 4. Standard Tools:

```python
# RESTful - সব tools support করে
- Swagger/OpenAPI
- Postman
- Browser DevTools
- HTTP caching
- Load balancers

# Non-RESTful - Custom handling লাগে
- Custom documentation
- Custom caching logic
- Complex load balancing
```

### Common Mistakes (এড়িয়ে চলুন):

#### Mistake 1: Verbs in URLs

```python
# ❌ Wrong
GET /api/getUsers
POST /api/createUser
POST /api/updateUser
POST /api/deleteUser

# ✅ Correct
GET    /api/users
POST   /api/users
PUT    /api/users/123
DELETE /api/users/123
```

#### Mistake 2: Wrong HTTP Methods

```python
# ❌ Wrong - GET দিয়ে create করা
GET /api/createUser?name=John&email=john@example.com

# ✅ Correct - POST দিয়ে create
POST /api/users
Body: {"name": "John", "email": "john@example.com"}
```

#### Mistake 3: All 200 OK

```python
# ❌ Wrong - সব success 200
POST /api/users → 200 OK (should be 201!)
DELETE /api/users/5 → 200 OK (should be 204!)
GET /api/users/999 → 200 OK {"error": "Not found"} (should be 404!)

# ✅ Correct - proper status codes
POST /api/users → 201 Created
DELETE /api/users/5 → 204 No Content
GET /api/users/999 → 404 Not Found
```

#### Mistake 4: Inconsistent Responses

```python
# ❌ Wrong - different formats
GET /api/users/1 → {"user": {...}}
GET /api/products/1 → {"data": {...}}
GET /api/orders/1 → {"result": {...}}

# ✅ Correct - consistent format
GET /api/users/1 → {"id": 1, "name": "John"}
GET /api/products/1 → {"id": 1, "title": "Product"}
GET /api/orders/1 → {"id": 1, "total": 100}
```

### Migration Guide: Non-RESTful → RESTful

যদি আপনার existing non-RESTful API থাকে:

```python
# Old (Non-RESTful)
GET /api/getAllUsers
GET /api/getUserById?id=5
POST /api/createUser
POST /api/updateUser
POST /api/deleteUser

# New (RESTful) - Version 2
GET    /api/v2/users
GET    /api/v2/users/5
POST   /api/v2/users
PUT    /api/v2/users/5
DELETE /api/v2/users/5

# Keep old API for backward compatibility
# Deprecate gradually
```

---

## REST vs SOAP vs GraphQL

### Comparison Table:

| Feature | REST | SOAP | GraphQL |
|---------|------|------|---------|
| **Type** | Architectural style | Protocol | Query language |
| **Format** | JSON, XML | XML only | JSON |
| **Transport** | HTTP | HTTP, SMTP, etc | HTTP |
| **Complexity** | Simple | Complex | Medium |
| **Learning Curve** | Easy | Steep | Medium |
| **Performance** | Good | Slower | Excellent |
| **Caching** | Built-in | Manual | Complex |
| **Versioning** | URL/Header | Namespace | Schema evolution |
| **Use Case** | General APIs | Enterprise, Banking | Complex queries |

### When to Use What:

#### REST ⭐⭐⭐ (Most Common)

**Use When:**
- General-purpose APIs
- CRUD operations
- Public APIs
- Mobile apps
- Simple to medium complexity

**Examples:**
- Social media APIs
- E-commerce APIs
- Blog APIs

#### SOAP

**Use When:**
- Enterprise applications
- Banking/Financial systems
- High security requirements
- ACID transactions needed

**Examples:**
- Payment gateways
- Legacy systems

#### GraphQL

**Use When:**
- Complex data requirements
- Multiple resources in one request
- Mobile apps (reduce requests)
- Flexible data fetching

**Examples:**
- Facebook, GitHub APIs
- Complex dashboards
- Real-time applications

---

## REST API Best Practices

### 1. API-First Design ⭐⭐⭐

**Design API before coding:**

```yaml
# OpenAPI Specification
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
```

### 2. Consistent Naming ⭐⭐⭐

**Good:**

```
/users
/user-profiles
/order-items
```

**Bad:**

```
/users
/UserProfiles
/order_items
```

### 3. Use Sub-Resources ⭐⭐

```
GET /users/123/orders           → User's orders
GET /articles/456/comments      → Article's comments
POST /users/123/orders          → Create order for user
```

### 4. Pagination ⭐⭐⭐

**Always paginate collections:**

```
GET /users?page=1&limit=20

Response:
{
  "count": 100,
  "next": "/users?page=2&limit=20",
  "previous": null,
  "results": [...]
}
```

### 5. Rate Limiting ⭐⭐

**Protect your API:**

```http
Response Headers:
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1641984000
```

### 6. Documentation ⭐⭐⭐

**Use tools:**
- Swagger/OpenAPI
- Postman
- API Blueprint

### 7. Compression ⭐⭐

**Enable gzip:**

```http
Request:
Accept-Encoding: gzip

Response:
Content-Encoding: gzip
```

### 8. CORS ⭐⭐

**Enable cross-origin requests:**

```http
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## REST API Security

### 1. HTTPS Only ⭐⭐⭐

```
❌ http://api.example.com
✅ https://api.example.com
```

### 2. Authentication ⭐⭐⭐

**JWT (Recommended 2025/2026):**

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**OAuth 2.0:**

```http
Authorization: Bearer access_token_here
```

**API Keys:**

```http
X-API-Key: your-api-key-here
```

### 3. Authorization ⭐⭐⭐

**Role-based:**

```python
# User can only access their own data
if request.user.id != resource.owner_id:
    return 403 Forbidden
```

### 4. Input Validation ⭐⭐⭐

**Never trust client input:**

```python
# Validate all inputs
if not email_is_valid(data['email']):
    return 400 Bad Request
```

### 5. Rate Limiting ⭐⭐

**Prevent abuse:**

```
100 requests per hour per user
1000 requests per hour per IP
```

### 6. Security Headers ⭐⭐

```http
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

---

## REST API Versioning

### Method 1: URI Versioning ⭐⭐⭐ (Most Common)

```
/v1/users
/v2/users
```

**Pros:**
- Clear and visible
- Easy to implement
- Easy to test

**Cons:**
- URL changes

### Method 2: Header Versioning

```http
GET /users
Accept: application/vnd.myapi.v1+json
```

**Pros:**
- Clean URLs
- RESTful

**Cons:**
- Less visible
- Harder to test

### Method 3: Query Parameter

```
/users?version=1
/users?version=2
```

**Pros:**
- Simple

**Cons:**
- Not RESTful
- Can be ignored

### Best Practice:

**Use URI versioning for major changes:**

```
/v1/users  → Old version
/v2/users  → New version (breaking changes)
```

**Maintain backward compatibility when possible.**

---

## HATEOAS

**HATEOAS = Hypermedia As The Engine Of Application State**

### Concept:

Client শুধু entry point জানবে, বাকি সব links response এ পাবে।

### Example:

```json
GET /users/123

{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": {
      "href": "/users/123"
    },
    "orders": {
      "href": "/users/123/orders"
    },
    "profile": {
      "href": "/users/123/profile"
    },
    "update": {
      "href": "/users/123",
      "method": "PUT"
    },
    "delete": {
      "href": "/users/123",
      "method": "DELETE"
    }
  }
}
```

### Benefits:

- Self-documenting API
- Discoverability
- Loose coupling
- Evolvability

### Drawbacks:

- Increased payload size
- Complex implementation
- Not widely adopted

---

## Richardson Maturity Model

REST APIs এর maturity level measure করার একটি model।

### Level 0: The Swamp of POX (Plain Old XML)

**Single endpoint, single method:**

```
POST /api
<request>
  <action>getUser</action>
  <userId>123</userId>
</request>
```

**Not RESTful at all!**

### Level 1: Resources

**Multiple endpoints, single method:**

```
POST /users/123
POST /articles/456
```

**Better, but still not RESTful.**

### Level 2: HTTP Verbs ⭐⭐⭐ (Most Common)

**Multiple endpoints, multiple methods:**

```
GET /users/123
POST /users
PUT /users/123
DELETE /users/123
```

**This is what most people call REST!**

### Level 3: Hypermedia Controls (HATEOAS)

**Level 2 + Links:**

```json
{
  "id": 123,
  "name": "John",
  "_links": {
    "self": "/users/123",
    "orders": "/users/123/orders"
  }
}
```

**True REST according to Roy Fielding!**

### Reality:

**Most APIs are Level 2, which is good enough for most use cases.**

---

## অতিরিক্ত Resources

### Official Documentation
- Roy Fielding's Dissertation: https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- RESTful API Design: https://restfulapi.net/

### Tools
- Postman - API testing
- Swagger/OpenAPI - API documentation
- Insomnia - API client

### সম্পর্কিত বিষয়
- HTTP (http.md)
- Status Codes (status-codes.md)
- Authentication (authentication.md)

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
