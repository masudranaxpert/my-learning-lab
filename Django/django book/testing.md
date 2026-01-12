# Django REST Framework - Testing

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Testing কী এবং কেন?](#testing-কী-এবং-কেন)
3. [Testing Tools](#testing-tools)
4. [APITestCase](#apitestcase)
5. [APIClient](#apiclient)
6. [Test Types](#test-types)
7. [Code Coverage](#code-coverage)
8. [Pytest Integration](#pytest-integration)
9. [Best Practices](#best-practices)
10. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **Testing কী এবং কেন?**
2. ⭐⭐⭐ **APITestCase** - DRF testing এর base
3. ⭐⭐⭐ **APIClient** - Request করা
4. ⭐⭐⭐ **Test Types** - কী কী test করবেন
5. ⭐⭐⭐ **Code Coverage** - কতটুকু test হয়েছে

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **Pytest Integration** - Modern testing (2025/2026)
7. ⭐⭐ **Best Practices** - Professional testing
8. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ**

### শেষে পড়ুন (Advanced):

9. ⭐ **Mocking** - External services mock করা
10. ⭐ **Performance Testing** - Load testing

---

## পরিচিতি

Testing হলো code verify করা যে সেটা expected behavior দেখাচ্ছে কিনা।

### সহজ উদাহরণ:

```python
# API Endpoint
GET /api/articles/

# Test: এটা কাজ করছে কিনা?
def test_list_articles(self):
    response = self.client.get('/api/articles/')
    self.assertEqual(response.status_code, 200)
    self.assertIsInstance(response.data, list)
```

---

## Testing কী এবং কেন?

### Testing কী?

**সহজ ভাষায়:** Testing হলো automated code যা আপনার main code check করে।

**উদাহরণ:**

```python
# Your Code
def add(a, b):
    return a + b

# Test Code
def test_add():
    assert add(2, 3) == 5  # Pass!
    assert add(-1, 1) == 0  # Pass!
```

### কেন Testing প্রয়োজন?

1. **Bugs খুঁজে বের করা** - Deploy এর আগে
2. **Confidence** - Code change করলেও ভয় নেই
3. **Documentation** - Tests দেখে বুঝা যায় code কী করে
4. **Refactoring** - নিরাপদে code improve করা
5. **Team Collaboration** - অন্যরা code break করছে কিনা জানা

### Testing এর সুবিধা:

```python
# Without Tests:
# 1. Code লিখলাম
# 2. Manually test করলাম browser এ
# 3. Deploy করলাম
# 4. Production এ bug! 😱

# With Tests:
# 1. Code লিখলাম
# 2. Test লিখলাম
# 3. Test run করলাম → Failed
# 4. Bug fix করলাম
# 5. Test run করলাম → Passed
# 6. Deploy করলাম → Confident! 😊
```

### Real-World তুলনা:

```
Car Testing এর মতো:
- Unit Tests = Individual parts test (engine, brakes)
- Integration Tests = Parts একসাথে কাজ করছে কিনা
- End-to-End Tests = পুরো car drive করা
```

---

## Testing Tools

Django REST Framework testing এর জন্য tools:

### 1. Django's TestCase

```python
from django.test import TestCase

class MyTest(TestCase):
    def test_something(self):
        self.assertEqual(1 + 1, 2)
```

### 2. DRF's APITestCase ⭐⭐⭐ (Recommended!)

```python
from rest_framework.test import APITestCase

class ArticleTests(APITestCase):
    def test_list_articles(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
```

### 3. APIClient

```python
from rest_framework.test import APIClient

client = APIClient()
response = client.get('/api/articles/')
```

### 4. Pytest (Modern - 2025/2026) ⭐⭐⭐

```python
import pytest

def test_list_articles(api_client):
    response = api_client.get('/api/articles/')
    assert response.status_code == 200
```

---

## APITestCase

`APITestCase` হলো DRF এর main testing class।

### Basic Structure:

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Article

class ArticleTests(APITestCase):
    def setUp(self):
        """
        প্রতিটি test এর আগে run হয়
        """
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content',
            author=self.user
        )
    
    def tearDown(self):
        """
        প্রতিটি test এর পরে run হয়
        """
        # Cleanup if needed
        pass
    
    def test_list_articles(self):
        """Test article list endpoint"""
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_article(self):
        """Test article creation"""
        data = {
            'title': 'New Article',
            'content': 'New content'
        }
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
```

### setUp() এবং tearDown():

**কী এবং কেন?**

`setUp()` এবং `tearDown()` হলো special methods যা প্রতিটি test method এর আগে এবং পরে automatically call হয়।

**কেন প্রয়োজন?**
- প্রতিটি test এর জন্য fresh, clean environment তৈরি করা
- Test isolation নিশ্চিত করা (একটি test অন্যটিকে affect করবে না)
- Repeated code avoid করা

**কখন কী হয়:**

```
Test Class শুরু
  ↓
setUp() call হয় → test_method_1() run হয় → tearDown() call হয়
  ↓
setUp() call হয় → test_method_2() run হয় → tearDown() call হয়
  ↓
setUp() call হয় → test_method_3() run হয় → tearDown() call হয়
  ↓
Test Class শেষ
```

**Example:**

```python
class ArticleTests(APITestCase):
    def setUp(self):
        """
        কখন: প্রতিটি test method এর আগে
        কাজ: Test data তৈরি করা
        কেন: প্রতিটি test fresh data দিয়ে শুরু হবে
        """
        print("setUp called!")  # Debug করার জন্য
        
        # User তৈরি করা (প্রতিটি test এর জন্য)
        self.user = User.objects.create_user(username='test', password='pass')
        
        # Article তৈরি করা (প্রতিটি test এর জন্য)
        self.article = Article.objects.create(title='Test', author=self.user)
    
    def tearDown(self):
        """
        কখন: প্রতিটি test method এর পরে
        কাজ: Cleanup (যদি লাগে)
        কেন: Resources free করা, temporary files delete করা
        
        Note: Django automatically database rollback করে,
        তাই সাধারণত এখানে কিছু লিখতে হয় না
        """
        print("tearDown called!")  # Debug করার জন্য
        pass  # Django automatically rolls back database
    
    def test_article_exists(self):
        """Test 1: Article আছে কিনা"""
        # setUp() already called, self.article available
        self.assertEqual(Article.objects.count(), 1)
        # tearDown() will be called after this
    
    def test_article_title(self):
        """Test 2: Article title check"""
        # setUp() called again! Fresh data!
        self.assertEqual(self.article.title, 'Test')
        # tearDown() will be called after this
```

**Execution Flow:**

```
1. setUp() → test_article_exists() → tearDown()
   Database: User created, Article created → Test runs → Database rolled back
   
2. setUp() → test_article_title() → tearDown()
   Database: User created again, Article created again → Test runs → Database rolled back
```

**কেন প্রতিবার setUp() call হয়?**

```python
# যদি setUp() না থাকতো:
def test_delete_article(self):
    self.article.delete()  # Article deleted
    
def test_article_exists(self):
    # এখানে article নেই! Previous test delete করেছে!
    # Test fail হবে!

# setUp() থাকার কারণে:
def test_delete_article(self):
    self.article.delete()  # Article deleted
    # tearDown() → Database rollback
    
def test_article_exists(self):
    # setUp() আবার call হয়েছে
    # Fresh article আছে! Test pass হবে!
```

### setUpTestData() (Performance Optimization):

**কী এবং কেন?**

`setUpTestData()` হলো একটি class method যা **পুরো test class এর জন্য একবার** call হয়।

**setUp() vs setUpTestData():**

| Feature | setUp() | setUpTestData() |
|---------|---------|-----------------|
| কখন call হয় | প্রতিটি test এর আগে | পুরো class এ একবার |
| Performance | Slow (বারবার create) | Fast (একবার create) |
| Data modify করা যায় | ✅ হ্যাঁ | ❌ না (read-only) |
| Use case | Mutable data | Immutable/read-only data |

**কখন কী হয়:**

```
Test Class শুরু
  ↓
setUpTestData() call হয় (একবার!)
  ↓
setUp() → test_method_1() → tearDown()
  ↓
setUp() → test_method_2() → tearDown()
  ↓
setUp() → test_method_3() → tearDown()
  ↓
Test Class শেষ
```

**Example:**

```python
class ArticleTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        কখন: পুরো test class এর জন্য একবার
        কাজ: Common, read-only data তৈরি করা
        কেন: Performance improve করা (faster tests!)
        
        Warning: এখানে তৈরি data modify করবেন না!
        """
        print("setUpTestData called once!")
        
        # User তৈরি করা (একবার!)
        cls.user = User.objects.create_user(username='test', password='pass')
        
        # Article তৈরি করা (একবার!)
        cls.article = Article.objects.create(title='Test', author=cls.user)
    
    def setUp(self):
        """
        এখনো প্রতিটি test এর আগে call হবে
        কিন্তু শুধু mutable data এর জন্য
        """
        print("setUp called!")
        # setUpTestData এর data available: self.user, self.article
    
    def test_article_title(self):
        """Test 1: Read-only check"""
        # setUpTestData এর data ব্যবহার করা (read-only)
        self.assertEqual(self.article.title, 'Test')  # ✅ OK
    
    def test_article_count(self):
        """Test 2: Read-only check"""
        self.assertEqual(Article.objects.count(), 1)  # ✅ OK
    
    def test_modify_article(self):
        """Test 3: Modify করা (সাবধান!)"""
        # ❌ Bad: setUpTestData এর data modify করা
        # self.article.title = 'Modified'
        # self.article.save()
        # এটা অন্য tests affect করবে!
        
        # ✅ Good: নতুন data তৈরি করা
        new_article = Article.objects.create(
            title='New',
            author=self.user
        )
        self.assertEqual(Article.objects.count(), 2)
```

**Performance Comparison:**

```python
# Without setUpTestData (Slow):
# setUp() → test_1() → tearDown() → Database rollback
# setUp() → test_2() → tearDown() → Database rollback
# setUp() → test_3() → tearDown() → Database rollback
# Total: 3 user creations, 3 article creations

# With setUpTestData (Fast):
# setUpTestData() → 1 user, 1 article created
# setUp() → test_1() → tearDown()
# setUp() → test_2() → tearDown()
# setUp() → test_3() → tearDown()
# Total: 1 user creation, 1 article creation (3x faster!)
```

**কখন কোনটা ব্যবহার করবেন:**

```python
# setUp() ব্যবহার করুন যখন:
# - Data modify করবেন
# - Each test এর জন্য fresh data লাগবে

class ArticleTests(APITestCase):
    def setUp(self):
        # প্রতিবার fresh article
        self.article = Article.objects.create(title='Test')
    
    def test_delete(self):
        self.article.delete()  # ✅ OK, fresh article পাবেন next test এ

# setUpTestData() ব্যবহার করুন যখন:
# - Data শুধু read করবেন
# - Performance important

class ArticleTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # একবার তৈরি, সব tests read করবে
        cls.user = User.objects.create_user(username='test')
    
    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username='test').exists())
```

---

## APIClient

`APIClient` ব্যবহার করে HTTP requests simulate করা হয়।

### Basic Usage:

```python
from rest_framework.test import APIClient

class ArticleTests(APITestCase):
    def setUp(self):
        self.client = APIClient()  # Already available in APITestCase!
    
    def test_get_request(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_request(self):
        data = {'title': 'New Article', 'content': 'Content'}
        response = self.client.post('/api/articles/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_put_request(self):
        data = {'title': 'Updated Title'}
        response = self.client.put('/api/articles/1/', data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_request(self):
        response = self.client.delete('/api/articles/1/')
        self.assertEqual(response.status_code, 204)
```

### Authentication:

**কেন Authentication Test করতে হয়?**

বেশিরভাগ API endpoints এ authentication লাগে। Test করার সময় আমাদের simulate করতে হবে যে user logged in আছে।

**৩টি উপায় আছে:**

1. **force_authenticate()** - সবচেয়ে সহজ (Recommended!)
2. **credentials()** - Token/JWT authentication এর জন্য
3. **login()** - Session authentication এর জন্য

#### Method 1: force_authenticate() ⭐⭐⭐ (Most Common!)

**কী:**
এটা সরাসরি user কে authenticate করে দেয়, কোনো token বা password লাগে না।

**কখন ব্যবহার করবেন:**
- সব ধরনের tests এ (সবচেয়ে সহজ!)
- যখন authentication logic test করছেন না
- যখন শুধু authenticated user এর behavior test করছেন

**কেন ভালো:**
- সহজ এবং দ্রুত
- Token তৈরি করতে হয় না
- Password মনে রাখতে হয় না
- সব authentication types এর সাথে কাজ করে

```python
class ArticleTests(APITestCase):
    def setUp(self):
        # User তৈরি করা
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_authenticated_request(self):
        """
        কী হচ্ছে:
        1. force_authenticate() user কে directly authenticate করে দিচ্ছে
        2. এখন self.client এর সব requests authenticated হবে
        3. Test শেষে logout করা ভালো practice
        """
        
        # Force authentication (সবচেয়ে সহজ!)
        self.client.force_authenticate(user=self.user)
        
        # এখন authenticated user হিসেবে request করা যাবে
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        
        # Logout (optional কিন্তু recommended)
        self.client.force_authenticate(user=None)
    
    def test_unauthenticated_request(self):
        """
        কী হচ্ছে:
        force_authenticate() call করিনি, তাই unauthenticated
        """
        # No authentication
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 401)  # Unauthorized
```

**কখন কী হচ্ছে:**

```
Test শুরু
  ↓
setUp() → User তৈরি হলো
  ↓
test_authenticated_request() শুরু
  ↓
self.client.force_authenticate(user=self.user)
  → DRF internally: request.user = self.user set করে দিলো
  → কোনো token check করলো না, সরাসরি authenticated!
  ↓
self.client.get('/api/articles/')
  → Request পাঠালো
  → Server দেখলো: request.user = test user
  → Authentication passed!
  → Response: 200 OK
  ↓
self.client.force_authenticate(user=None)
  → Logout করলো
  ↓
Test শেষ
```

#### Method 2: credentials() (Token Authentication)

**কী:**
এটা HTTP headers set করে (যেমন Authorization header)।

**কখন ব্যবহার করবেন:**
- যখন Token/JWT authentication test করছেন
- যখন real-world scenario simulate করতে চান
- যখন authentication logic নিজেই test করছেন

**কেন ব্যবহার করবেন:**
- Production এর মতো exact behavior
- Token generation test করা যায়
- Headers test করা যায়

```python
from rest_framework.authtoken.models import Token

class ArticleTests(APITestCase):
    def setUp(self):
        # User তৈরি করা
        self.user = User.objects.create_user(username='test', password='pass')
        
        # Token তৈরি করা
        self.token = Token.objects.create(user=self.user)
    
    def test_token_authentication(self):
        """
        কী হচ্ছে:
        1. credentials() Authorization header set করছে
        2. এটা real client এর মতো token পাঠাচ্ছে
        3. Server token verify করবে
        """
        
        # Set token in header (Production এর মতো!)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # এখন request পাঠালে token সাথে যাবে
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        
        # Clear credentials (পরবর্তী tests এর জন্য)
        self.client.credentials()
    
    def test_invalid_token(self):
        """
        কী হচ্ছে:
        Invalid token দিয়ে test করছি
        """
        # Invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid123')
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 401)  # Unauthorized
```

**কখন কী হচ্ছে:**

```
Test শুরু
  ↓
setUp() → User তৈরি → Token তৈরি
  ↓
test_token_authentication() শুরু
  ↓
self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
  → Client এ header set হলো: Authorization: Token abc123...
  ↓
self.client.get('/api/articles/')
  → Request পাঠালো header সহ
  → Server TokenAuthentication class চালালো
  → Token verify করলো database এ
  → Token valid! → request.user = test user
  → Response: 200 OK
  ↓
self.client.credentials()
  → Headers clear করলো
  ↓
Test শেষ
```

**JWT এর জন্য:**

```python
class ArticleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        
        # JWT token তৈরি করা
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_jwt_authentication(self):
        """JWT token দিয়ে authentication"""
        # JWT token set করা
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
```

#### Method 3: login() (Session Authentication)

**কী:**
Django এর session authentication ব্যবহার করে (browser এর মতো)।

**কখন ব্যবহার করবেন:**
- যখন SessionAuthentication test করছেন
- যখন browser-based clients test করছেন
- যখন cookies test করছেন

**কেন কম ব্যবহার হয়:**
- API সাধারণত token-based হয়
- Session stateful (REST এর বিপরীত)
- force_authenticate() সহজ

```python
class ArticleTests(APITestCase):
    def setUp(self):
        # User তৈরি করা
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_session_authentication(self):
        """
        কী হচ্ছে:
        1. login() Django session তৈরি করছে
        2. Cookie set হচ্ছে
        3. Browser এর মতো behavior
        """
        
        # Login (username + password লাগবে!)
        logged_in = self.client.login(username='test', password='pass')
        self.assertTrue(logged_in)  # Login successful?
        
        # এখন session cookie সহ request যাবে
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        
        # Logout
        self.client.logout()
    
    def test_invalid_login(self):
        """Wrong password"""
        logged_in = self.client.login(username='test', password='wrong')
        self.assertFalse(logged_in)  # Login failed
```

**কখন কী হচ্ছে:**

```
Test শুরু
  ↓
setUp() → User তৈরি (password='pass')
  ↓
test_session_authentication() শুরু
  ↓
self.client.login(username='test', password='pass')
  → Django authenticate() call করলো
  → Password verify করলো
  → Session তৈরি করলো
  → Session cookie set করলো
  → Return: True (success)
  ↓
self.client.get('/api/articles/')
  → Request পাঠালো session cookie সহ
  → Server SessionAuthentication চালালো
  → Session verify করলো
  → request.user = test user
  → Response: 200 OK
  ↓
self.client.logout()
  → Session delete করলো
  ↓
Test শেষ
```

### কোনটা কখন ব্যবহার করবেন - Quick Guide:

```python
# 1. সাধারণ tests (90% cases):
# ✅ force_authenticate() ব্যবহার করুন
def test_create_article(self):
    self.client.force_authenticate(user=self.user)
    response = self.client.post('/api/articles/', data)

# 2. Token authentication logic test:
# ✅ credentials() ব্যবহার করুন
def test_token_authentication(self):
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    response = self.client.get('/api/articles/')

# 3. Session authentication test:
# ✅ login() ব্যবহার করুন
def test_session_authentication(self):
    self.client.login(username='test', password='pass')
    response = self.client.get('/api/articles/')

# 4. Unauthenticated test:
# ✅ কিছু call করবেন না
def test_unauthenticated(self):
    # No authentication
    response = self.client.get('/api/articles/')
    self.assertEqual(response.status_code, 401)
```

### Multiple Users Test:

```python
class ArticleTests(APITestCase):
    def setUp(self):
        # দুইজন user
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        
        # user1 এর article
        self.article = Article.objects.create(
            title='Test',
            author=self.user1
        )
    
    def test_author_can_delete(self):
        """Author নিজের article delete করতে পারবে"""
        # user1 authenticate করা
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, 204)  # Success
    
    def test_non_author_cannot_delete(self):
        """অন্য user delete করতে পারবে না"""
        # user2 authenticate করা (not the author!)
        self.client.force_authenticate(user=self.user2)
        
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, 403)  # Forbidden
```

### Request Formats:

```python
class ArticleTests(APITestCase):
    def test_json_format(self):
        data = {'title': 'Test'}
        response = self.client.post('/api/articles/', data, format='json')
    
    def test_multipart_format(self):
        # For file uploads
        data = {'title': 'Test', 'image': image_file}
        response = self.client.post('/api/articles/', data, format='multipart')
```

---

## Test Types

### 1. Model Tests

```python
from django.test import TestCase
from .models import Article

class ArticleModelTests(TestCase):
    def test_article_creation(self):
        """Test article model creation"""
        article = Article.objects.create(
            title='Test Article',
            content='Test content'
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertIsNotNone(article.created_at)
    
    def test_article_str(self):
        """Test article string representation"""
        article = Article.objects.create(title='Test')
        self.assertEqual(str(article), 'Test')
```

### 2. Serializer Tests

```python
from rest_framework.test import APITestCase
from .serializers import ArticleSerializer
from .models import Article

class ArticleSerializerTests(APITestCase):
    def test_serializer_with_valid_data(self):
        """Test serializer with valid data"""
        data = {
            'title': 'Test Article',
            'content': 'Test content'
        }
        serializer = ArticleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'Test Article')
    
    def test_serializer_with_invalid_data(self):
        """Test serializer with invalid data"""
        data = {'title': ''}  # Empty title
        serializer = ArticleSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
```

### 3. View/Endpoint Tests

```python
class ArticleViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.article = Article.objects.create(
            title='Test',
            content='Content',
            author=self.user
        )
    
    def test_list_articles(self):
        """Test GET /api/articles/"""
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_article(self):
        """Test GET /api/articles/{id}/"""
        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test')
    
    def test_create_article(self):
        """Test POST /api/articles/"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New', 'content': 'New content'}
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
    
    def test_update_article(self):
        """Test PUT /api/articles/{id}/"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated', 'content': 'Updated content'}
        response = self.client.put(f'/api/articles/{self.article.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated')
    
    def test_delete_article(self):
        """Test DELETE /api/articles/{id}/"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)
```

### 4. Permission Tests

```python
class ArticlePermissionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.article = Article.objects.create(
            title='Test',
            content='Content',
            author=self.user1
        )
    
    def test_unauthenticated_cannot_create(self):
        """Unauthenticated users cannot create articles"""
        data = {'title': 'New', 'content': 'Content'}
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_author_can_update(self):
        """Author can update their own article"""
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated', 'content': 'Content'}
        response = self.client.put(f'/api/articles/{self.article.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_author_cannot_update(self):
        """Non-author cannot update article"""
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Updated', 'content': 'Content'}
        response = self.client.put(f'/api/articles/{self.article.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### 5. Authentication Tests

```python
class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    def test_user_login(self):
        """Test user login"""
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

---

## Code Coverage

Code Coverage measure করে কতটুকু code tests দ্বারা covered হয়েছে।

### Installation:

```bash
pip install coverage
```

### Basic Usage:

```bash
# Run tests with coverage
coverage run --source='.' manage.py test

# View coverage report
coverage report

# Output:
# Name                      Stmts   Miss  Cover
# ---------------------------------------------
# myapp/models.py              20      2    90%
# myapp/views.py               30      5    83%
# myapp/serializers.py         15      0   100%
# ---------------------------------------------
# TOTAL                        65      7    89%
```

### HTML Report:

```bash
# Generate HTML report
coverage html

# Open htmlcov/index.html in browser
```

### Coverage Configuration:

```ini
# .coveragerc
[run]
source = .
omit =
    */migrations/*
    */tests/*
    */venv/*
    manage.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### Coverage Goals:

```
Excellent: 90%+
Good: 80-90%
Acceptable: 70-80%
Poor: <70%
```

### Coverage with pytest:

```bash
# Install
pip install pytest-cov

# Run
pytest --cov=myapp --cov-report=html

# View
open htmlcov/index.html
```

---

## Pytest Integration

Pytest হলো modern, powerful testing framework (2025/2026 recommended!)

### Installation:

```bash
pip install pytest pytest-django pytest-cov
```

### Configuration:

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
```

### Basic Pytest Test:

```python
# tests/test_articles.py
import pytest
from rest_framework import status
from myapp.models import Article

@pytest.mark.django_db
class TestArticleAPI:
    def test_list_articles(self, api_client):
        """Test article list endpoint"""
        response = api_client.get('/api/articles/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_article(self, api_client, user):
        """Test article creation"""
        api_client.force_authenticate(user=user)
        data = {'title': 'Test', 'content': 'Content'}
        response = api_client.post('/api/articles/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Article.objects.count() == 1
```

### Pytest Fixtures:

```python
# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from myapp.models import Article

@pytest.fixture
def api_client():
    """API client fixture"""
    return APIClient()

@pytest.fixture
def user(db):
    """User fixture"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def article(db, user):
    """Article fixture"""
    return Article.objects.create(
        title='Test Article',
        content='Test content',
        author=user
    )

# Usage in tests:
def test_something(api_client, user, article):
    api_client.force_authenticate(user=user)
    response = api_client.get(f'/api/articles/{article.id}/')
    assert response.status_code == 200
```

### Parametrized Tests:

```python
import pytest

@pytest.mark.parametrize('title,content,expected_status', [
    ('Valid Title', 'Valid content', 201),
    ('', 'Valid content', 400),  # Empty title
    ('Valid Title', '', 400),     # Empty content
])
def test_article_creation(api_client, user, title, content, expected_status):
    api_client.force_authenticate(user=user)
    data = {'title': title, 'content': content}
    response = api_client.post('/api/articles/', data)
    assert response.status_code == expected_status
```

### Running Pytest:

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_articles.py

# Run specific test
pytest tests/test_articles.py::TestArticleAPI::test_list_articles

# Run with coverage
pytest --cov=myapp --cov-report=html

# Run with verbose output
pytest -v

# Run failed tests only
pytest --lf
```

---

## Best Practices

### 1. Test Naming Convention

```python
# Good - Descriptive names
def test_authenticated_user_can_create_article(self):
    pass

def test_unauthenticated_user_cannot_create_article(self):
    pass

# Bad - Vague names
def test_create(self):
    pass

def test_1(self):
    pass
```

### 2. One Assertion Per Test (When Possible)

```python
# Good - Focused test
def test_article_creation_returns_201(self):
    response = self.client.post('/api/articles/', data)
    self.assertEqual(response.status_code, 201)

def test_article_creation_increases_count(self):
    self.client.post('/api/articles/', data)
    self.assertEqual(Article.objects.count(), 1)

# Acceptable - Related assertions
def test_article_creation(self):
    response = self.client.post('/api/articles/', data)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Article.objects.count(), 1)
    self.assertEqual(response.data['title'], data['title'])
```

### 3. Use setUp() for Common Data

```python
class ArticleTests(APITestCase):
    def setUp(self):
        # Common for all tests
        self.user = User.objects.create_user(username='test', password='pass')
        self.client.force_authenticate(user=self.user)
    
    def test_create_article(self):
        # No need to create user again
        response = self.client.post('/api/articles/', data)
```

### 4. Test Edge Cases

```python
class ArticleTests(APITestCase):
    def test_create_article_with_empty_title(self):
        """Edge case: empty title"""
        data = {'title': '', 'content': 'Content'}
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, 400)
    
    def test_create_article_with_very_long_title(self):
        """Edge case: very long title"""
        data = {'title': 'a' * 1000, 'content': 'Content'}
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, 400)
```

### 5. Aim for High Coverage

```python
# Target: 80%+ coverage
# Focus on:
# - All views/endpoints
# - All serializers
# - Critical business logic
# - Permission checks
```

### 6. Fast Tests

```python
# Good - Use setUpTestData for read-only data
@classmethod
def setUpTestData(cls):
    cls.user = User.objects.create_user(username='test', password='pass')

# Bad - Creating data in every test
def test_something(self):
    user = User.objects.create_user(username='test', password='pass')
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: Complete CRUD Tests

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Article

class ArticleCRUDTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create test user once for all tests"""
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def setUp(self):
        """Authenticate before each test"""
        self.client.force_authenticate(user=self.user)
        
        # Create test article
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content',
            author=self.user
        )
    
    def test_list_articles(self):
        """Test GET /api/articles/"""
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Article')
    
    def test_retrieve_article(self):
        """Test GET /api/articles/{id}/"""
        response = self.client.get(f'/api/articles/{self.article.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.article.id)
        self.assertEqual(response.data['title'], 'Test Article')
    
    def test_create_article(self):
        """Test POST /api/articles/"""
        data = {
            'title': 'New Article',
            'content': 'New content here'
        }
        response = self.client.post('/api/articles/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Article')
        
        # Verify in database
        article = Article.objects.get(id=response.data['id'])
        self.assertEqual(article.title, 'New Article')
        self.assertEqual(article.author, self.user)
    
    def test_update_article(self):
        """Test PUT /api/articles/{id}/"""
        data = {
            'title': 'Updated Title',
            'content': 'Updated content'
        }
        response = self.client.put(
            f'/api/articles/{self.article.id}/',
            data
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        
        # Verify in database
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')
    
    def test_partial_update_article(self):
        """Test PATCH /api/articles/{id}/"""
        data = {'title': 'Patched Title'}
        response = self.client.patch(
            f'/api/articles/{self.article.id}/',
            data
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Patched Title')
        
        # Content should remain unchanged
        self.article.refresh_from_db()
        self.assertEqual(self.article.content, 'Test content')
    
    def test_delete_article(self):
        """Test DELETE /api/articles/{id}/"""
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)
        
        # Verify article is deleted
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(id=self.article.id)
```

### উদাহরণ 2: Validation Tests

```python
class ArticleValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client.force_authenticate(user=self.user)
    
    def test_create_article_with_empty_title(self):
        """Title cannot be empty"""
        data = {'title': '', 'content': 'Content'}
        response = self.client.post('/api/articles/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_article_with_short_content(self):
        """Content must be at least 100 characters"""
        data = {'title': 'Title', 'content': 'Short'}
        response = self.client.post('/api/articles/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)
    
    def test_create_article_with_duplicate_title(self):
        """Title must be unique"""
        Article.objects.create(
            title='Unique Title',
            content='Content',
            author=self.user
        )
        
        data = {'title': 'Unique Title', 'content': 'Different content'}
        response = self.client.post('/api/articles/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

### উদাহরণ 3: Permission Tests

```python
class ArticlePermissionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        
        self.article = Article.objects.create(
            title='Test',
            content='Content',
            author=self.user1
        )
    
    def test_unauthenticated_cannot_create(self):
        """Unauthenticated users cannot create articles"""
        data = {'title': 'New', 'content': 'Content'}
        response = self.client.post('/api/articles/', data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_can_list(self):
        """Authenticated users can list articles"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_author_can_update_own_article(self):
        """Author can update their own article"""
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated', 'content': 'Content'}
        response = self.client.put(f'/api/articles/{self.article.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_author_cannot_update_article(self):
        """Non-author cannot update article"""
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Updated', 'content': 'Content'}
        response = self.client.put(f'/api/articles/{self.article.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_author_can_delete_own_article(self):
        """Author can delete their own article"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```

### উদাহরণ 4: Pytest Example

```python
# tests/test_articles.py
import pytest
from rest_framework import status
from myapp.models import Article

@pytest.mark.django_db
class TestArticleAPI:
    def test_list_articles(self, api_client, article):
        """Test article list"""
        response = api_client.get('/api/articles/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
    
    def test_create_article(self, api_client, user):
        """Test article creation"""
        api_client.force_authenticate(user=user)
        data = {'title': 'New', 'content': 'Content'}
        response = api_client.post('/api/articles/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Article.objects.count() == 1
        assert response.data['title'] == 'New'
    
    @pytest.mark.parametrize('title,expected_status', [
        ('Valid Title', 201),
        ('', 400),  # Empty title
    ])
    def test_article_title_validation(self, api_client, user, title, expected_status):
        """Test title validation"""
        api_client.force_authenticate(user=user)
        data = {'title': title, 'content': 'Content'}
        response = api_client.post('/api/articles/', data)
        
        assert response.status_code == expected_status

# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from myapp.models import Article

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='test', password='pass')

@pytest.fixture
def article(db, user):
    return Article.objects.create(
        title='Test',
        content='Content',
        author=user
    )
```

---

## Running Tests

### Django TestCase:

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test myapp

# Run specific test file
python manage.py test myapp.tests.test_articles

# Run specific test class
python manage.py test myapp.tests.test_articles.ArticleTests

# Run specific test method
python manage.py test myapp.tests.test_articles.ArticleTests.test_list_articles

# Run with verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

### Pytest:

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_articles.py

# Run specific test
pytest tests/test_articles.py::TestArticleAPI::test_list_articles

# Run with coverage
pytest --cov=myapp --cov-report=html

# Run verbose
pytest -v

# Run with print statements
pytest -s

# Run failed tests only
pytest --lf
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django Testing: https://docs.djangoproject.com/en/stable/topics/testing/
- DRF Testing: https://www.django-rest-framework.org/api-guide/testing/
- Pytest: https://docs.pytest.org/
- Coverage.py: https://coverage.readthedocs.io/

### সম্পর্কিত বিষয়
- Continuous Integration (CI/CD)
- Test-Driven Development (TDD)
- Mocking and Fixtures

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
