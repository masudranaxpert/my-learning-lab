# Django REST Framework - Authentication

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Authentication কী এবং কেন?](#authentication-কী-এবং-কেন)
3. [Authentication vs Authorization](#authentication-vs-authorization)
4. [Authentication কীভাবে কাজ করে](#authentication-কীভাবে-কাজ-করে)
5. [Built-in Authentication Classes](#built-in-authentication-classes)
   - [SessionAuthentication](#sessionauthentication)
   - [TokenAuthentication](#tokenauthentication)
   - [BasicAuthentication](#basicauthentication)
6. [Modern Authentication (2025/2026)](#modern-authentication-20252026)
   - [JWT Authentication](#jwt-authentication)
   - [Django REST Knox](#django-rest-knox)
   - [OAuth2](#oauth2)
7. [Setup এবং Configuration](#setup-এবং-configuration)
8. [Custom Authentication](#custom-authentication)
9. [Best Practices](#best-practices)
10. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **Authentication কী এবং কেন?**
2. ⭐⭐⭐ **Authentication vs Authorization** - পার্থক্য বোঝা
3. ⭐⭐⭐ **TokenAuthentication** - সবচেয়ে common
4. ⭐⭐⭐ **JWT Authentication** - Modern standard (2025/2026)
5. ⭐⭐⭐ **Setup এবং Configuration**

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **SessionAuthentication** - Web apps এর জন্য
7. ⭐⭐ **Django REST Knox** - Better than TokenAuthentication
8. ⭐⭐ **Best Practices** - Security এবং production tips
9. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ**

### শেষে পড়ুন (Advanced):

10. ⭐ **BasicAuthentication** - Rarely used
11. ⭐ **OAuth2** - Third-party login
12. ⭐ **Custom Authentication** - নিজের authentication তৈরি করা

---

## পরিচিতি

API তৈরি করার সময় দুটি মূল প্রশ্ন:

1. **এই request কে পাঠিয়েছে?** (Authentication)
2. **এই user কী করতে পারবে?** (Authorization/Permissions)

এই documentation শুধুমাত্র **Authentication** নিয়ে। Permissions আলাদা documentation এ আছে।

### সহজ উদাহরণ:

```python
# Without Authentication
GET /api/articles/
# কে request করেছে? জানা নেই!

# With Authentication
GET /api/articles/
Authorization: Token abc123xyz
# এখন জানি: User "John" request করেছে
```

---

## Authentication কী এবং কেন?

### Authentication কী?

**সহজ ভাষায়:** Authentication হলো verify করা যে user কে বলছে সে সেই ব্যক্তি কিনা।

**Real-world উদাহরণ:**
- Airport এ passport দেখানো
- ATM এ PIN দেওয়া
- Website এ login করা

**API তে:**
```
Client: "আমি John, আমাকে data দাও"
Server: "প্রমাণ করো তুমি John"
Client: "এই নাও আমার token: abc123"
Server: "ঠিক আছে, তুমি John। এই নাও data"
```

### কেন Authentication প্রয়োজন?

1. **Security** - শুধু authorized users access পাবে
2. **Personalization** - User-specific data দেখানো
3. **Tracking** - কে কী করছে track করা
4. **Rate Limiting** - Per-user limits apply করা

### Authentication এর Components:

| Component | কাজ | উদাহরণ |
|-----------|-----|---------|
| **Credentials** | User identity proof | Username + Password, Token |
| **Authentication Scheme** | কীভাবে verify করবে | Token, JWT, Session |
| **request.user** | Authenticated user object | User instance |
| **request.auth** | Authentication details | Token instance |

---

## Authentication vs Authorization

অনেকে এই দুটি confuse করে। পার্থক্য বুঝুন:

### Authentication (Who are you?)

**প্রশ্ন:** তুমি কে?

**উদাহরণ:**
- Username + Password দিয়ে login
- Token পাঠানো
- Fingerprint scan

**DRF তে:**
```python
# Authentication
request.user  # <User: john>
request.auth  # <Token: abc123>
```

### Authorization (What can you do?)

**প্রশ্ন:** তুমি কী করতে পারবে?

**উদাহরণ:**
- Admin panel access
- Delete করার permission
- Own posts edit করা

**DRF তে:**
```python
# Authorization (Permissions)
permission_classes = [IsAuthenticated, IsAuthor]
```

### তুলনা Table:

| Feature | Authentication | Authorization |
|---------|---------------|---------------|
| প্রশ্ন | Who are you? | What can you do? |
| কখন হয় | Request এর শুরুতে | Permission check এ |
| Result | request.user, request.auth | Allow/Deny access |
| Example | Login, Token | IsAuthenticated, IsAdmin |
| DRF Class | Authentication classes | Permission classes |

### একসাথে কীভাবে কাজ করে:

```python
# 1. Authentication (Who?)
class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]  # Token দিয়ে identify
    
    # 2. Authorization (What?)
    permission_classes = [IsAuthenticated, IsAuthor]  # কী করতে পারবে
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**Flow:**
```
1. Client পাঠায়: Authorization: Token abc123
2. Authentication: Token verify করে → request.user = John
3. Permission: John কি এই article edit করতে পারবে?
4. যদি হ্যাঁ → Allow, না হলে → 403 Forbidden
```

---

## Authentication কীভাবে কাজ করে

### Request Flow:

```
1. Client Request পাঠায়
   ↓
2. Authentication Class চেক করে credentials
   ↓
3. Valid হলে: request.user এবং request.auth set করে
   ↓
4. Invalid হলে: 401 Unauthorized
   ↓
5. Permission Check
   ↓
6. View Code Execute
```

### Code Example:

```python
# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Client Request:
GET /api/articles/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# DRF Internally:
# 1. TokenAuthentication.authenticate() called
# 2. Token verified
# 3. request.user = User object
# 4. request.auth = Token object
# 5. IsAuthenticated.has_permission() → True
# 6. View executes
```

### request.user এবং request.auth:

```python
class MyView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        # request.user - Django User instance
        print(request.user)  # <User: john>
        print(request.user.username)  # 'john'
        print(request.user.email)  # 'john@example.com'
        
        # request.auth - Token instance
        print(request.auth)  # <Token: 9944b09...>
        print(request.auth.key)  # '9944b09...'
        
        return Response({'message': f'Hello {request.user.username}'})
```

---

## Built-in Authentication Classes

DRF চারটি built-in authentication classes প্রদান করে:

### 1. SessionAuthentication

**কাজ:** Django এর session framework ব্যবহার করে।

**কখন ব্যবহার করবেন:**
- Traditional web applications
- Frontend এবং backend same domain এ
- Browser-based clients

**সুবিধা:**
- Built-in CSRF protection
- Django এর সাথে integrate
- Session management automatic

**অসুবিধা:**
- Stateful (server এ session store করতে হয়)
- Mobile apps এর জন্য ভালো না
- Scalability issues (large user base এ)

**Setup:**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

**ব্যবহার:**

```python
# Client (Browser)
# 1. Login করুন Django admin বা login view দিয়ে
# 2. Session cookie automatically set হবে
# 3. পরবর্তী requests এ cookie automatically পাঠাবে

# API Request (Browser automatically পাঠায়)
GET /api/articles/
Cookie: sessionid=abc123xyz
```

**কখন ব্যবহার করবেন:**
- ✅ Web apps (React, Vue frontend + Django backend same domain)
- ✅ Django templates সহ traditional apps
- ❌ Mobile apps
- ❌ Third-party clients
- ❌ Microservices

---

### 2. TokenAuthentication ⭐

**কাজ:** প্রতিটি user এর জন্য একটি unique token তৈরি করে।

**কখন ব্যবহার করবেন:**
- Mobile applications
- Desktop clients
- SPAs (Single Page Applications)
- Simple token-based auth চাইলে

**Setup:**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',  # Add this!
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Run migrations
python manage.py migrate
```

**Token তৈরি করা:**

**Method 1: Manually**

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='john')
token = Token.objects.create(user=user)
print(token.key)  # '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

**Method 2: Signal (Automatic)**

```python
# signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

**Method 3: Login View**

```python
# views.py
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

# Client Request:
POST /api/login/
{
    "username": "john",
    "password": "secret123"
}

# Response:
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "john"
}
```

**Token ব্যবহার করা:**

```python
# Client পাঠাবে:
GET /api/articles/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Logout (Token Delete):**

```python
@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out'})
```

**সুবিধা:**
- Simple এবং straightforward
- Stateless
- Mobile apps এর জন্য perfect

**অসুবিধা:**
- প্রতি user এ শুধু একটি token
- Token expire হয় না (security risk!)
- Token rotation নেই

**⚠️ Production Warning:**
- HTTPS ছাড়া ব্যবহার করবেন না!
- Token database এ plain text এ থাকে
- Better alternatives: JWT, Knox

---

### 3. BasicAuthentication

**কাজ:** প্রতিটি request এ username এবং password পাঠাতে হয়।

**⚠️ Warning:** Production এ ব্যবহার করবেন না! শুধু testing এর জন্য।

**Setup:**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}
```

**ব্যবহার:**

```bash
# Username: john, Password: secret123
# Base64 encode: am9objpzZWNyZXQxMjM=

GET /api/articles/
Authorization: Basic am9objpzZWNyZXQxMjM=
```

**কেন ব্যবহার করবেন না:**
- প্রতিটি request এ password পাঠাতে হয়
- Security risk
- No logout mechanism

**কখন ব্যবহার করবেন:**
- ✅ Development/Testing
- ✅ curl commands দিয়ে quick testing
- ❌ Production
- ❌ Real applications

---

## Modern Authentication (2025/2026)

2025/2026 এ recommended authentication methods:

### 1. JWT Authentication ⭐⭐⭐ (Most Recommended!)

**কাজ:** JSON Web Tokens - stateless, secure, modern standard।

**কেন JWT?**
- ✅ Stateless (server এ কিছু store করতে হয় না)
- ✅ Scalable (microservices এর জন্য perfect)
- ✅ Token expiry built-in
- ✅ Refresh tokens support
- ✅ Industry standard

**Package:** `djangorestframework-simplejwt`

**Installation:**

```bash
pip install djangorestframework-simplejwt
```

**Setup:**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Short-lived
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Long-lived
    'ROTATE_REFRESH_TOKENS': True,                   # Security!
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**ব্যবহার:**

```bash
# 1. Login - Get tokens
POST /api/token/
{
    "username": "john",
    "password": "secret123"
}

# Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  # 15 minutes
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  # 7 days
}

# 2. Use access token
GET /api/articles/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

# 3. Access token expired? Refresh it
POST /api/token/refresh/
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  # New access token
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  # New refresh token (if rotation enabled)
}
```

**Custom Claims:**

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

**Best Practices:**
- ✅ Short-lived access tokens (5-15 minutes)
- ✅ Longer refresh tokens (7 days)
- ✅ Token rotation enabled
- ✅ HTTPS only
- ✅ Store tokens in HTTP-only cookies (web) or secure storage (mobile)
- ❌ Never store in localStorage (XSS risk!)

---

### 2. Django REST Knox ⭐⭐

**কাজ:** Better alternative to DRF's TokenAuthentication।

**সুবিধা:**
- ✅ Multiple tokens per user
- ✅ Token expiry
- ✅ Token rotation
- ✅ Secure token storage (hashed)
- ✅ Per-device tokens

**Installation:**

```bash
pip install django-rest-knox
```

**Setup:**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'knox',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ],
}

# Run migrations
python manage.py migrate
```

**ব্যবহার:**

```python
# urls.py
from knox import views as knox_views
from . import views

urlpatterns = [
    path('api/login/', views.LoginView.as_view(), name='knox_login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

# views.py
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
```

**কখন ব্যবহার করবেন:**
- Mobile apps (multiple devices)
- SPAs
- যখন JWT এর complexity চান না

---

### 3. OAuth2

**কাজ:** Third-party authentication (Google, Facebook, GitHub)।

**Package:** `django-oauth-toolkit`

**কখন ব্যবহার করবেন:**
- Social login
- SSO (Single Sign-On)
- Third-party integrations

---

## Setup এবং Configuration

### Global Configuration:

```python
# settings.py
REST_FRAMEWORK = {
    # Default authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Default permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Per-View Configuration:

```python
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class ArticleView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Hello'})
```

### Per-ViewSet Configuration:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

### Multiple Authentication Classes:

```python
# Try JWT first, then Session
class ArticleView(APIView):
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
        TokenAuthentication,
    ]
    
    def get(self, request):
        # DRF will try each authentication class in order
        # First successful authentication wins
        return Response({'user': request.user.username})
```

---

## Custom Authentication

নিজের authentication class তৈরি করা:

```python
from rest_framework import authentication
from rest_framework import exceptions
from .models import CustomToken

class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get token from header
        token = request.META.get('HTTP_X_API_KEY')
        
        if not token:
            return None  # No authentication attempted
        
        try:
            # Verify token
            token_obj = CustomToken.objects.get(key=token, is_active=True)
        except CustomToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        # Return (user, auth)
        return (token_obj.user, token_obj)
    
    def authenticate_header(self, request):
        return 'X-API-Key'

# Usage:
class MyView(APIView):
    authentication_classes = [CustomTokenAuthentication]
```

---

## Best Practices

### 1. Always Use HTTPS

```python
# settings.py (Production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Use JWT for Modern Apps (2025/2026)

```python
# Recommended for 2025/2026
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### 3. Short-lived Access Tokens

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Short!
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### 4. Token Rotation

```python
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 5. Secure Token Storage

```python
# ❌ Bad - localStorage (XSS vulnerable)
localStorage.setItem('token', token)

# ✅ Good - HTTP-only cookie
# Server sets: Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict

# ✅ Good - Mobile secure storage
# iOS: Keychain
# Android: EncryptedSharedPreferences
```

### 6. Rate Limiting

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: JWT Authentication Complete Setup

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # Authentication already set globally
```

### উদাহরণ 2: Mixed Authentication (Web + Mobile)

```python
# Web users: Session
# Mobile users: JWT

class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        JWTAuthentication,        # Mobile
        SessionAuthentication,    # Web
    ]
    permission_classes = [IsAuthenticated]
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

### উদাহরণ 3: Public + Private Endpoints

```python
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        """Public endpoint - no authentication required"""
        articles = Article.objects.filter(is_published=True)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Authentication: https://www.django-rest-framework.org/api-guide/authentication/
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/
- Django REST Knox: https://james1345.github.io/django-rest-knox/

### সম্পর্কিত বিষয়
- Permissions (পরবর্তী documentation)
- Throttling
- Security

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
