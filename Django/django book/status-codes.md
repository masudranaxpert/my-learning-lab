# Django REST Framework - HTTP Status Codes

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Status Code কী এবং কেন?](#status-code-কী-এবং-কেন)
3. [Status Code Categories](#status-code-categories)
4. [2xx Success Codes](#2xx-success-codes)
5. [3xx Redirection Codes](#3xx-redirection-codes)
6. [4xx Client Error Codes](#4xx-client-error-codes)
7. [5xx Server Error Codes](#5xx-server-error-codes)
8. [DRF এ Status Codes ব্যবহার](#drf-এ-status-codes-ব্যবহার)
9. [Best Practices](#best-practices)
10. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **Status Code কী এবং কেন?**
2. ⭐⭐⭐ **2xx Success Codes** - 200, 201, 204
3. ⭐⭐⭐ **4xx Client Error Codes** - 400, 401, 403, 404
4. ⭐⭐⭐ **DRF এ Status Codes ব্যবহার**

### এরপর পড়ুন (গুরুত্বপূর্ণ):

5. ⭐⭐ **5xx Server Error Codes** - 500, 503
6. ⭐⭐ **Best Practices** - কখন কোনটি ব্যবহার করবেন
7. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ**

### শেষে পড়ুন (Advanced):

8. ⭐ **3xx Redirection Codes**
9. ⭐ **Custom Status Codes**

---

## পরিচিতি

HTTP Status Codes হলো server থেকে client কে বলা যে request টি কী হয়েছে - success, error, redirect ইত্যাদি।

### সহজ উদাহরণ:

```python
# Success
GET /api/articles/
→ 200 OK

# Created
POST /api/articles/
→ 201 Created

# Not Found
GET /api/articles/999/
→ 404 Not Found

# Unauthorized
GET /api/articles/
→ 401 Unauthorized
```

---

## Status Code কী এবং কেন?

### Status Code কী?

**সহজ ভাষায়:** HTTP Status Code হলো একটি ৩-digit number যা server response এর status বলে দেয়।

**Format:** `XXX Status Message`

**উদাহরণ:**
- `200 OK`
- `404 Not Found`
- `500 Internal Server Error`

### কেন Status Code প্রয়োজন?

1. **Client কে জানানো** - Request success হয়েছে কিনা
2. **Error Handling** - কী ধরনের error হয়েছে
3. **Standard Communication** - সবাই একই language বুঝে
4. **Debugging** - সমস্যা খুঁজে বের করা সহজ

### Real-World তুলনা:

```
Traffic Signal এর মতো:
- 🟢 Green (2xx) = Success, এগিয়ে যান
- 🟡 Yellow (3xx) = Redirect, অন্য পথে যান
- 🔴 Red (4xx) = Client Error, আপনার ভুল
- ⚫ Black (5xx) = Server Error, আমাদের ভুল
```

---

## Status Code Categories

HTTP Status Codes পাঁচটি categories তে ভাগ:

| Range | Category | অর্থ | উদাহরণ |
|-------|----------|------|---------|
| **1xx** | Informational | Processing চলছে | 100 Continue |
| **2xx** | Success | Request successful | 200 OK, 201 Created |
| **3xx** | Redirection | Redirect করতে হবে | 301 Moved Permanently |
| **4xx** | Client Error | Client এর ভুল | 400 Bad Request, 404 Not Found |
| **5xx** | Server Error | Server এর ভুল | 500 Internal Server Error |

### কোনটা কখন:

```python
# 2xx - সব ঠিক আছে
return Response(data, status=200)

# 4xx - Client ভুল করেছে
return Response(errors, status=400)

# 5xx - Server এ সমস্যা
return Response({'error': 'Server error'}, status=500)
```

---

## 2xx Success Codes

Request successful হলে 2xx codes ব্যবহার হয়।

### 200 OK ⭐⭐⭐ (সবচেয়ে Common!)

**কখন:** Request successful এবং response আছে।

**ব্যবহার:**
- GET requests (list, retrieve)
- PUT/PATCH requests (update)
- Any successful operation with response

```python
# GET - List
GET /api/articles/
→ 200 OK
{
    "count": 10,
    "results": [...]
}

# GET - Retrieve
GET /api/articles/5/
→ 200 OK
{
    "id": 5,
    "title": "My Article"
}

# PUT - Update
PUT /api/articles/5/
→ 200 OK
{
    "id": 5,
    "title": "Updated Title"
}

# DRF Code:
from rest_framework import status
from rest_framework.response import Response

class ArticleView(APIView):
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # অথবা শুধু: return Response(serializer.data)
```

### 201 Created ⭐⭐⭐

**কখন:** নতুন resource তৈরি হয়েছে।

**ব্যবহার:**
- POST requests (create)

```python
# POST - Create
POST /api/articles/
{
    "title": "New Article",
    "content": "Content here"
}

→ 201 Created
{
    "id": 11,
    "title": "New Article",
    "content": "Content here",
    "created_at": "2026-01-12T10:00:00Z"
}

# DRF Code:
class ArticleView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 204 No Content ⭐⭐

**কখন:** Request successful কিন্তু response body নেই।

**ব্যবহার:**
- DELETE requests
- Update যেখানে response data দরকার নেই

```python
# DELETE
DELETE /api/articles/5/
→ 204 No Content
(Empty response body)

# DRF Code:
class ArticleView(APIView):
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### 202 Accepted

**কখন:** Request accepted কিন্তু processing এখনো complete হয়নি।

**ব্যবহার:**
- Async operations
- Background tasks
- Long-running processes

```python
# POST - Async task
POST /api/reports/generate/
→ 202 Accepted
{
    "message": "Report generation started",
    "task_id": "abc123",
    "status_url": "/api/tasks/abc123/"
}

# DRF Code:
from celery import shared_task

class ReportView(APIView):
    def post(self, request):
        task = generate_report.delay(request.data)
        return Response({
            'task_id': task.id,
            'status_url': f'/api/tasks/{task.id}/'
        }, status=status.HTTP_202_ACCEPTED)
```

---

## 3xx Redirection Codes

Client কে অন্য URL এ redirect করতে হবে।

### 301 Moved Permanently

**কখন:** Resource permanently নতুন URL এ move হয়েছে।

```python
# Old URL
GET /api/v1/articles/
→ 301 Moved Permanently
Location: /api/v2/articles/
```

### 302 Found (Temporary Redirect)

**কখন:** Resource temporarily অন্য URL এ আছে।

### 304 Not Modified

**কখন:** Resource modify হয়নি (caching এর জন্য)।

**Note:** REST APIs তে 3xx codes কম ব্যবহার হয়।

---

## 4xx Client Error Codes

Client এর ভুলের জন্য 4xx codes।

### 400 Bad Request ⭐⭐⭐

**কখন:** Request invalid বা malformed।

**ব্যবহার:**
- Validation errors
- Invalid JSON
- Missing required fields

```python
# Invalid data
POST /api/articles/
{
    "title": "",  # Empty title
    "content": "abc"  # Too short
}

→ 400 Bad Request
{
    "title": ["This field may not be blank."],
    "content": ["Ensure this field has at least 100 characters."]
}

# DRF Code:
class ArticleView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 401 Unauthorized ⭐⭐⭐

**কখন:** Authentication required কিন্তু credentials নেই বা invalid।

**ব্যবহার:**
- No authentication token
- Invalid token
- Expired token

```python
# No token
GET /api/articles/
→ 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}

# Invalid token
GET /api/articles/
Authorization: Token invalid123
→ 401 Unauthorized
{
    "detail": "Invalid token."
}

# DRF Code:
# Automatically handled by authentication classes
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 403 Forbidden ⭐⭐⭐

**কখন:** Authenticated কিন্তু permission নেই।

**ব্যবহার:**
- User authenticated কিন্তু access denied
- Not the owner
- Insufficient permissions

```python
# Authenticated but not the author
DELETE /api/articles/5/
Authorization: Token abc123
→ 403 Forbidden
{
    "detail": "You do not have permission to perform this action."
}

# DRF Code:
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class ArticleView(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        self.check_object_permissions(request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### 404 Not Found ⭐⭐⭐

**কখন:** Resource খুঁজে পাওয়া যায়নি।

**ব্যবহার:**
- Invalid ID
- Deleted resource
- Wrong URL

```python
# Resource doesn't exist
GET /api/articles/999/
→ 404 Not Found
{
    "detail": "Not found."
}

# DRF Code:
from django.shortcuts import get_object_or_404

class ArticleView(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
```

### 405 Method Not Allowed

**কখন:** HTTP method allowed নয়।

```python
# DELETE not allowed
DELETE /api/articles/
→ 405 Method Not Allowed
{
    "detail": "Method \"DELETE\" not allowed."
}

# DRF Code:
class ArticleListView(APIView):
    def get(self, request):
        # GET allowed
        pass
    
    def post(self, request):
        # POST allowed
        pass
    
    # DELETE not implemented, so 405
```

### 409 Conflict

**কখন:** Request conflicts with current state।

**ব্যবহার:**
- Duplicate resource
- Version conflict

```python
# Duplicate email
POST /api/users/
{
    "email": "john@example.com"  # Already exists
}

→ 409 Conflict
{
    "detail": "User with this email already exists."
}
```

### 422 Unprocessable Entity

**কখন:** Request valid কিন্তু semantic errors আছে।

**ব্যবহার:**
- Business logic validation errors

```python
# End date before start date
POST /api/events/
{
    "start_date": "2026-01-15",
    "end_date": "2026-01-10"  # Before start!
}

→ 422 Unprocessable Entity
{
    "detail": "End date must be after start date."
}
```

### 429 Too Many Requests

**কখন:** Rate limit exceed করেছে।

```python
# Too many requests
GET /api/articles/
→ 429 Too Many Requests
{
    "detail": "Request was throttled. Expected available in 60 seconds."
}

# DRF Code:
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/hour'
    }
}
```

---

## 5xx Server Error Codes

Server এর ভুলের জন্য 5xx codes।

### 500 Internal Server Error ⭐⭐

**কখন:** Server এ unexpected error।

**ব্যবহার:**
- Unhandled exceptions
- Code bugs
- Database errors

```python
# Server error
GET /api/articles/
→ 500 Internal Server Error
{
    "detail": "Internal server error."
}

# DRF Code:
# Automatically handled by Django
# But you can customize:
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        # Unhandled exception
        return Response({
            'detail': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler'
}
```

### 503 Service Unavailable

**কখন:** Server temporarily unavailable।

**ব্যবহার:**
- Maintenance mode
- Overloaded server
- Database down

```python
# Maintenance
GET /api/articles/
→ 503 Service Unavailable
{
    "detail": "Service temporarily unavailable. Please try again later."
}
```

---

## DRF এ Status Codes ব্যবহার

### Method 1: status Module (Recommended!)

```python
from rest_framework import status
from rest_framework.response import Response

class ArticleView(APIView):
    def get(self, request, pk):
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response(data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**সুবিধা:**
- Readable: `status.HTTP_200_OK` vs `200`
- Autocomplete support
- Less error-prone

### Method 2: Integer (Not Recommended)

```python
# Bad - Hard to remember
return Response(data, status=201)

# Good - Clear and readable
return Response(data, status=status.HTTP_201_CREATED)
```

### Common Status Codes in DRF:

```python
from rest_framework import status

# Success
status.HTTP_200_OK                    # 200
status.HTTP_201_CREATED               # 201
status.HTTP_204_NO_CONTENT            # 204

# Client Errors
status.HTTP_400_BAD_REQUEST           # 400
status.HTTP_401_UNAUTHORIZED          # 401
status.HTTP_403_FORBIDDEN             # 403
status.HTTP_404_NOT_FOUND             # 404
status.HTTP_405_METHOD_NOT_ALLOWED    # 405
status.HTTP_409_CONFLICT              # 409
status.HTTP_429_TOO_MANY_REQUESTS     # 429

# Server Errors
status.HTTP_500_INTERNAL_SERVER_ERROR # 500
status.HTTP_503_SERVICE_UNAVAILABLE   # 503
```

### ViewSet এ Default Status Codes:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    # DRF automatically uses:
    # list() → 200 OK
    # create() → 201 Created
    # retrieve() → 200 OK
    # update() → 200 OK
    # partial_update() → 200 OK
    # destroy() → 204 No Content
```

### Custom Status Codes:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response with 201
        return Response({
            'message': 'Article created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
```

---

## Best Practices

### 1. সঠিক Status Code ব্যবহার করুন

```python
# Good - Correct status codes
class ArticleView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Bad - Wrong status codes
class ArticleView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Should be 201!
        return Response(serializer.errors, status=status.HTTP_200_OK)  # Should be 400!
```

### 2. Consistent Error Responses

```python
# Good - Consistent format
{
    "detail": "Error message",
    "errors": {
        "field": ["Error 1", "Error 2"]
    }
}

# Bad - Inconsistent
# Sometimes: {"error": "..."}
# Sometimes: {"message": "..."}
# Sometimes: {"detail": "..."}
```

### 3. Use status Module

```python
# Good
from rest_framework import status
return Response(data, status=status.HTTP_200_OK)

# Bad
return Response(data, status=200)
```

### 4. DELETE Returns 204

```python
# Good
def delete(self, request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Bad
def delete(self, request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)
```

### 5. POST Returns 201 with Created Resource

```python
# Good
def post(self, request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Bad
def post(self, request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Created'}, status=status.HTTP_200_OK)
```

### 6. 401 vs 403

```python
# 401 - Not authenticated
# No token or invalid token
→ 401 Unauthorized

# 403 - Authenticated but no permission
# Valid token but not allowed
→ 403 Forbidden
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: CRUD Operations

```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class ArticleListView(APIView):
    def get(self, request):
        """List all articles - 200 OK"""
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create article - 201 Created or 400 Bad Request"""
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(APIView):
    def get(self, request, pk):
        """Retrieve article - 200 OK or 404 Not Found"""
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """Update article - 200 OK, 400 Bad Request, or 404 Not Found"""
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Delete article - 204 No Content or 404 Not Found"""
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### উদাহরণ 2: Authentication & Permissions

```python
class ArticleView(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    
    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            # 404 - Resource not found
            return Response(
                {'detail': 'Article not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check permissions
        if article.author != request.user:
            # 403 - Authenticated but not allowed
            return Response(
                {'detail': 'You are not the author'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        article.delete()
        # 204 - Deleted successfully
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### উদাহরণ 3: Custom Actions

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish article"""
        article = self.get_object()
        
        if article.is_published:
            # 409 - Already published
            return Response(
                {'detail': 'Article already published'},
                status=status.HTTP_409_CONFLICT
            )
        
        article.is_published = True
        article.save()
        
        # 200 - Updated successfully
        return Response(
            {'detail': 'Article published'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics"""
        stats = {
            'total': Article.objects.count(),
            'published': Article.objects.filter(is_published=True).count(),
        }
        # 200 - Success
        return Response(stats, status=status.HTTP_200_OK)
```

### উদাহরণ 4: Error Handling

```python
from rest_framework.exceptions import ValidationError, PermissionDenied

class ArticleView(APIView):
    def post(self, request):
        try:
            serializer = ArticleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # 201 - Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            # 400 - Validation error
            return Response(
                {'errors': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except PermissionDenied:
            # 403 - Permission denied
            return Response(
                {'detail': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        except Exception as e:
            # 500 - Server error
            return Response(
                {'detail': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

---

## Quick Reference Table

| Status Code | কখন ব্যবহার করবেন | DRF Constant |
|------------|-------------------|--------------|
| **200** | GET, PUT, PATCH success | `HTTP_200_OK` |
| **201** | POST success (created) | `HTTP_201_CREATED` |
| **204** | DELETE success | `HTTP_204_NO_CONTENT` |
| **400** | Validation error | `HTTP_400_BAD_REQUEST` |
| **401** | Not authenticated | `HTTP_401_UNAUTHORIZED` |
| **403** | No permission | `HTTP_403_FORBIDDEN` |
| **404** | Not found | `HTTP_404_NOT_FOUND` |
| **405** | Method not allowed | `HTTP_405_METHOD_NOT_ALLOWED` |
| **409** | Conflict | `HTTP_409_CONFLICT` |
| **429** | Too many requests | `HTTP_429_TOO_MANY_REQUESTS` |
| **500** | Server error | `HTTP_500_INTERNAL_SERVER_ERROR` |

---

## অতিরিক্ত Resources

### Official Documentation
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- DRF Status Codes: https://www.django-rest-framework.org/api-guide/status-codes/

### সম্পর্কিত বিষয়
- Error Handling
- Exception Handling
- Response Format

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
