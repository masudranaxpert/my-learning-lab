# DRF Auth Kit + Django Allauth - Complete Setup Guide

## 📋 Table of Contents
1. [Installation](#installation)
2. [Settings Configuration](#settings-configuration)
3. [Custom Registration Serializer](#custom-registration-serializer)
4. [Problems Faced & Solutions](#problems-faced--solutions)
5. [Final Working Configuration](#final-working-configuration)

---

## Installation

```bash
# Install DRF Auth Kit with all features
pip install drf-auth-kit[all]

# This automatically installs:
# - django-allauth
# - djangorestframework
# - djangorestframework-simplejwt
# - drf-spectacular
```

---

## Settings Configuration

### 1. INSTALLED_APPS (Order Important!)

```python
INSTALLED_APPS = [
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django Allauth (MUST be before auth_kit)
    'allauth',
    'allauth.account',
    
    # DRF Auth Kit
    'auth_kit',

    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',  # For logout blacklisting
    'drf_spectacular',
    'phonenumber_field',

    # Local apps
    'authentication',
]
```

### 2. MIDDLEWARE

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Required for Allauth
]
```

### 3. REST_FRAMEWORK

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_kit.authentication.JWTCookieAuthentication',
    ),
}
```

### 4. SIMPLE_JWT (Token Lifetimes)

**⚠️ IMPORTANT:** Token lifetime configure করতে হয় `SIMPLE_JWT` এ, `AUTH_KIT` এ নয়!

```python
SIMPLE_JWT = {
    # Token lifetimes
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    
    # Token rotation and blacklisting
    'ROTATE_REFRESH_TOKENS': True,      # Generate new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,   # Blacklist old refresh token (logout security)
    'UPDATE_LAST_LOGIN': True,
    
    # Algorithm
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    
    # Headers
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    # User fields
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### 5. AUTH_KIT

```python
AUTH_KIT = {
    # Authentication type
    'AUTH_TYPE': 'jwt',
    
    # Cookie-based authentication
    'USE_AUTH_COOKIE': False,  # False = tokens in response body, True = tokens in cookies
    
    # Cookie settings
    # CRITICAL: When USE_AUTH_COOKIE=False, set AUTH_COOKIE_HTTPONLY=False
    # Otherwise refresh token will be empty in response!
    'AUTH_COOKIE_HTTPONLY': False,  # Must match USE_AUTH_COOKIE
    'AUTH_COOKIE_SECURE': False,    # True in production (HTTPS)
    'AUTH_COOKIE_SAMESITE': 'Lax',
    
    # JWT Cookie names
    'AUTH_JWT_COOKIE_NAME': 'auth-jwt',
    'AUTH_JWT_REFRESH_COOKIE_NAME': 'auth-refresh-jwt',
    
    # MFA
    'USE_MFA': False,
    
    # Custom serializers
    'REGISTER_SERIALIZER': 'authentication.serializers.CustomRegisterSerializer',
}
```

### 6. Django Allauth

```python
# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings (Use NEW settings, not deprecated ones!)
ACCOUNT_LOGIN_METHODS = {'email'}  # NEW in 65.4.0 (replaces ACCOUNT_AUTHENTICATION_METHOD)
ACCOUNT_SIGNUP_FIELDS = ['username', 'email*', 'password1*', 'password2*']  # NEW in 65.5.0
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # or 'optional' or 'none'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_PREVENT_ENUMERATION = True  # Security
ACCOUNT_LOGOUT_ON_GET = False  # Security
```

### 7. CORS

```python
CORS_ALLOW_ALL_ORIGINS = True  # Development only
CORS_ALLOW_CREDENTIALS = True  # For cookie authentication
```

### 8. DRF Spectacular

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Ecommerce API',
    'DESCRIPTION': 'Complete Ecommerce API with DRF Auth Kit authentication',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'TAGS': [
        {'name': 'Authentication', 'description': 'User authentication endpoints'},
    ],
    'COMPONENT_SPLIT_REQUEST': True,
}
```

---

## Custom Registration Serializer

**Problem:** DRF Auth Kit removes `username` field when `USERNAME_FIELD='email'`

**Solution:** Override `__init__` to force username field

### File: `authentication/serializers.py`

```python
from auth_kit.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer with username field.
    
    DRF Auth Kit removes username when USERNAME_FIELD='email'.
    This serializer forces username to be present.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Force username field to be present
        if 'username' not in self.fields:
            self.fields['username'] = serializers.CharField(
                required=True,
                max_length=150,
                write_only=True,
            )

    def validate_username(self, value):
        """Validate username uniqueness"""
        username = get_adapter().clean_username(value)
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return username

    def get_cleaned_data(self):
        """Include username in cleaned data"""
        data = super().get_cleaned_data()
        if 'username' not in data or not data['username']:
            data['username'] = self.validated_data.get('username', '')
        return data

    def save(self, request):
        """Save user with username"""
        user = super().save(request)
        username = self.validated_data.get('username')
        if username:
            user.username = username
            user.save(update_fields=['username'])
        return user
```

---

## Problems Faced & Solutions

### Problem 1: `ACCESS_TOKEN_LIFETIME` not working in AUTH_KIT

**Error:** Token lifetime settings in `AUTH_KIT` ignored

**Reason:** DRF Auth Kit uses `djangorestframework-simplejwt` internally

**Solution:**
```python
# ❌ Wrong
AUTH_KIT = {
    'ACCESS_TOKEN_LIFETIME': 900,  # Doesn't exist!
}

# ✅ Correct
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
}
```

---

### Problem 2: Wrong cookie setting names

**Error:** Cookie settings not working

**Reason:** Wrong key names used

**Solution:**
```python
# ❌ Wrong
AUTH_KIT = {
    'COOKIE_HTTPONLY': True,  # Wrong key!
    'COOKIE_SECURE': False,
    'COOKIE_SAMESITE': 'Lax',
}

# ✅ Correct
AUTH_KIT = {
    'AUTH_COOKIE_HTTPONLY': True,  # Correct prefix!
    'AUTH_COOKIE_SECURE': False,
    'AUTH_COOKIE_SAMESITE': 'Lax',
}
```

---

### Problem 3: Deprecated Allauth settings warning

**Error:** `ACCOUNT_EMAIL_REQUIRED` is deprecated

**Reason:** Django Allauth 65.5.0 introduced new settings

**Solution:**
```python
# ❌ Deprecated (Old)
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Deprecated in 65.4.0
ACCOUNT_EMAIL_REQUIRED = True  # Deprecated in 65.5.0
ACCOUNT_USERNAME_REQUIRED = False  # Deprecated in 65.5.0

# ✅ New (Modern)
ACCOUNT_LOGIN_METHODS = {'email'}  # New in 65.4.0
ACCOUNT_SIGNUP_FIELDS = ['username', 'email*', 'password1*', 'password2*']  # New in 65.5.0
```

---

### Problem 4: Username field not showing in registration schema

**Error:** Registration endpoint doesn't have `username` field

**Reason:** DRF Auth Kit removes username when `USERNAME_FIELD='email'`

**Solution:** Custom serializer with `__init__` override (see above)

**Code flow:**
1. Parent `__init__` runs → removes username
2. Our `__init__` runs → adds username back
3. Result: username field present!

---

### Problem 5: Refresh token empty in response

**Error:** 
```json
{
  "access": "eyJ...",
  "refresh": "",  // ❌ Empty!
}
```

**Reason:** `AUTH_COOKIE_HTTPONLY = True` causes DRF Auth Kit to remove refresh token from response (assumes it's in cookie)

**Solution:**
```python
# When USE_AUTH_COOKIE=False, must set AUTH_COOKIE_HTTPONLY=False
AUTH_KIT = {
    'USE_AUTH_COOKIE': False,
    'AUTH_COOKIE_HTTPONLY': False,  # ✅ Must be False!
}
```

**DRF Auth Kit code that causes this:**
```python
# In RefreshViewWithCookieSupport.finalize_response()
if auth_kit_settings.AUTH_COOKIE_HTTPONLY:
    response.data["refresh"] = ""  # Removes refresh token!
```

---

### Problem 6: Logout doesn't blacklist token

**Error:** After logout, refresh token still works

**Reason:** `rest_framework_simplejwt.token_blacklist` not installed

**Solution:**
```python
INSTALLED_APPS = [
    # ...
    'rest_framework_simplejwt.token_blacklist',  # Add this!
]

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,  # Requires token_blacklist app
}
```

Then migrate:
```bash
python manage.py migrate
```

---

## Final Working Configuration

### Registration Schema

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password1": "securepass123",
  "password2": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "detail": "Verification email sent."
}
```

---

### Login Response

**With `USE_AUTH_COOKIE = False`:**
```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "access_expiration": "2026-01-30T21:23:18Z",
  "refresh_expiration": "2026-02-14T21:08:18Z",
  "user": {
    "pk": 1,
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**With `USE_AUTH_COOKIE = True`:**
```json
{
  "access": "eyJ...",
  "refresh": "",  // In HTTP-only cookie
  "access_expiration": "2026-01-30T21:23:18Z",
  "refresh_expiration": "2026-02-14T21:08:18Z",
  "user": {...}
}
```

---

### Token Refresh

**Request:**
```json
{
  "refresh": "eyJ..."
}
```

**Response (with ROTATE_REFRESH_TOKENS=True):**
```json
{
  "access": "eyJ...",  // New access token
  "refresh": "eyJ..."  // New refresh token (old one blacklisted)
}
```

---

## Key Takeaways

### 1. Configuration Hierarchy
- `SIMPLE_JWT` → Token lifetimes, rotation, blacklisting
- `AUTH_KIT` → Cookie settings, custom serializers/views
- `ACCOUNT_*` → Django Allauth settings

### 2. Cookie vs Response Body

| Setting | USE_AUTH_COOKIE | AUTH_COOKIE_HTTPONLY | Refresh in Response |
|---------|----------------|---------------------|-------------------|
| Cookie (Secure) | True | True | ❌ No (in cookie) |
| Response Body | False | False | ✅ Yes |
| **Wrong Config** | False | True | ❌ Empty! |

### 3. Security Best Practices

**Development:**
```python
AUTH_KIT = {
    'USE_AUTH_COOKIE': False,  # Easy testing
    'AUTH_COOKIE_HTTPONLY': False,
    'AUTH_COOKIE_SECURE': False,
}
```

**Production:**
```python
AUTH_KIT = {
    'USE_AUTH_COOKIE': True,  # More secure
    'AUTH_COOKIE_HTTPONLY': True,  # XSS protection
    'AUTH_COOKIE_SECURE': True,  # HTTPS only
}
```

### 4. Common Mistakes

| Mistake | Correct |
|---------|---------|
| `ACCESS_TOKEN_LIFETIME` in `AUTH_KIT` | Put in `SIMPLE_JWT` |
| `COOKIE_HTTPONLY` | `AUTH_COOKIE_HTTPONLY` |
| `ACCOUNT_EMAIL_REQUIRED` | `ACCOUNT_SIGNUP_FIELDS` |
| `ACCOUNT_AUTHENTICATION_METHOD` | `ACCOUNT_LOGIN_METHODS` |
| Missing `token_blacklist` app | Add to `INSTALLED_APPS` |

---

## Testing

```bash
# Check configuration
python manage.py check

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Visit API docs
http://localhost:8000/api/docs/
```

---

## API Endpoints

```
POST /api/auth/register/           - Register new user
POST /api/auth/login/              - Login
POST /api/auth/logout/             - Logout (blacklist token)
POST /api/auth/token/refresh/      - Refresh access token
POST /api/auth/password/change/    - Change password
POST /api/auth/password/reset/     - Request password reset
GET  /api/auth/user/               - Get user profile
PUT  /api/auth/user/               - Update user profile
```

---

## Documentation References

- **DRF Auth Kit:** https://drf-auth-kit.readthedocs.io/
- **Django Allauth:** https://docs.allauth.org/
- **Simple JWT:** https://django-rest-framework-simplejwt.readthedocs.io/
- **DRF Spectacular:** https://drf-spectacular.readthedocs.io/

---

**Setup Complete! 🎉**
