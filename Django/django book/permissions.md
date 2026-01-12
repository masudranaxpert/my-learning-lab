# Django REST Framework - Permissions

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Permission কী এবং কেন?](#permission-কী-এবং-কেন)
3. [Authentication vs Permissions](#authentication-vs-permissions)
4. [Permission কীভাবে কাজ করে](#permission-কীভাবে-কাজ-করে)
5. [Built-in Permission Classes](#built-in-permission-classes)
6. [Custom Permissions](#custom-permissions)
7. [Object-Level Permissions](#object-level-permissions)
8. [Combining Permissions](#combining-permissions)
9. [Best Practices](#best-practices)
10. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **Permission কী এবং কেন?**
2. ⭐⭐⭐ **Authentication vs Permissions** - পার্থক্য
3. ⭐⭐⭐ **Built-in Permission Classes** - IsAuthenticated, AllowAny ইত্যাদি
4. ⭐⭐⭐ **Custom Permissions** - নিজের permission তৈরি করা
5. ⭐⭐⭐ **Object-Level Permissions** - User শুধু নিজের data edit করতে পারবে

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **Combining Permissions** - একাধিক permissions একসাথে
7. ⭐⭐ **Best Practices** - Security এবং organization
8. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ**

### শেষে পড়ুন (Advanced):

9. ⭐ **DjangoModelPermissions** - Django এর built-in permissions
10. ⭐ **DjangoObjectPermissions** - Per-object permissions

---

## পরিচিতি

Authentication বলে **কে** আপনি, Permissions বলে **কী** করতে পারবেন।

### সহজ উদাহরণ:

```python
# Authentication: তুমি John
request.user  # <User: john>

# Permissions: John কী করতে পারবে?
# - সব articles দেখতে পারবে? ✅
# - নতুন article তৈরি করতে পারবে? ✅ (যদি authenticated)
# - অন্যের article delete করতে পারবে? ❌ (শুধু নিজের)
```

---

## Permission কী এবং কেন?

### Permission কী?

**সহজ ভাষায়:** Permission হলো access control - কে কী করতে পারবে সেটা নির্ধারণ করা।

**Real-world উদাহরণ:**
- Office এ: Manager সবার data দেখতে পারে, Employee শুধু নিজের
- Social Media: আপনি শুধু নিজের posts edit/delete করতে পারেন
- E-commerce: Admin products add করতে পারে, customers শুধু buy করতে পারে

### কেন Permission প্রয়োজন?

1. **Security** - Unauthorized access prevent করা
2. **Data Protection** - Users শুধু নিজের data access করবে
3. **Role-Based Access** - Admin, User, Guest - different access levels
4. **Business Logic** - Paid users extra features পাবে

### Permission Types:

| Type | Level | Example |
|------|-------|---------|
| **View-Level** | Entire endpoint | শুধু authenticated users access পাবে |
| **Object-Level** | Specific object | User শুধু নিজের article edit করতে পারবে |
| **Action-Based** | Specific action | Create করতে পারবে কিন্তু delete না |

---

## Authentication vs Permissions

এই দুটি একসাথে কাজ করে কিন্তু আলাদা:

### তুলনা:

| Feature | Authentication | Permissions |
|---------|---------------|-------------|
| প্রশ্ন | Who are you? | What can you do? |
| কাজ | Identity verify করা | Access control করা |
| কখন চেক হয় | প্রথমে | Authentication এর পরে |
| Result | request.user set হয় | Allow/Deny access |
| Example | TokenAuthentication | IsAuthenticated |
| Status Code | 401 Unauthorized | 403 Forbidden |

### একসাথে কীভাবে কাজ করে:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    # Step 1: Authentication - কে তুমি?
    authentication_classes = [TokenAuthentication]
    
    # Step 2: Permissions - কী করতে পারবে?
    permission_classes = [IsAuthenticated, IsAuthor]
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**Flow:**

```
1. Request আসে: GET /api/articles/5/
2. Authentication: Token verify → request.user = John
3. Permission Check:
   - IsAuthenticated? ✅ (John logged in)
   - IsAuthor? ✅ (John is the author)
4. Access Granted → Return article
```

**Error Codes:**

```python
# No authentication credentials
→ 401 Unauthorized

# Authenticated but no permission
→ 403 Forbidden
```

---

## Permission কীভাবে কাজ করে

### Permission Check Flow:

```
1. Request আসে
   ↓
2. Authentication (request.user set হয়)
   ↓
3. Permission Classes চেক হয়
   ↓
4. has_permission() call হয় (view-level)
   ↓
5. যদি object-specific হয়: has_object_permission() call হয়
   ↓
6. সব permissions pass করলে: View execute হয়
   ↓
7. কোনো permission fail করলে: 403 Forbidden
```

### Detailed Step-by-Step Example:

```python
# View
class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Custom Permission
class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        # View-level check
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Object-level check
        return obj.author == request.user
```

**কখন কী হচ্ছে:**

```
Client Request:
DELETE /api/articles/5/
Authorization: Token abc123

↓

Step 1: Request Received
- Method: DELETE
- URL: /api/articles/5/
- Headers: Authorization: Token abc123

↓

Step 2: Authentication
- TokenAuthentication.authenticate() called
- Token verified: abc123 → User "John"
- request.user = John
- request.auth = Token object

↓

Step 3: View-Level Permission Check (has_permission)

  Permission 1: IsAuthenticated
  - has_permission(request, view) called
  - Check: request.user.is_authenticated?
  - Result: ✅ True (John is logged in)
  
  Permission 2: IsAuthor
  - has_permission(request, view) called
  - Check: request.user.is_authenticated?
  - Result: ✅ True
  
  All view-level permissions passed!

↓

Step 4: Get Object
- Article.objects.get(pk=5)
- Article 5 found
- Article.author = "Jane" (not John!)

↓

Step 5: Object-Level Permission Check (has_object_permission)

  Permission 1: IsAuthenticated
  - No has_object_permission method
  - Skip ✅
  
  Permission 2: IsAuthor
  - has_object_permission(request, view, obj) called
  - Check: obj.author == request.user?
  - obj.author = Jane
  - request.user = John
  - Result: ❌ False (John is not the author!)
  
  Permission failed!

↓

Step 6: Return 403 Forbidden
Response:
{
    "detail": "You do not have permission to perform this action."
}
```

### Different Scenarios:

#### Scenario 1: List View (No Object)

```python
GET /api/articles/

Step 1: Authentication → John
Step 2: has_permission() → ✅ All pass
Step 3: No object → Skip has_object_permission()
Step 4: View executes → Return list
```

#### Scenario 2: Retrieve View (Object Check)

```python
GET /api/articles/5/

Step 1: Authentication → John
Step 2: has_permission() → ✅ All pass
Step 3: Get object → Article 5 (author: John)
Step 4: has_object_permission() → ✅ John is author
Step 5: View executes → Return article
```

#### Scenario 3: Create View (No Object Yet)

```python
POST /api/articles/
Body: {"title": "New Article"}

Step 1: Authentication → John
Step 2: has_permission() → ✅ All pass
Step 3: No existing object → Skip has_object_permission()
Step 4: View executes → Create article (author=John)
Step 5: Return 201 Created
```

#### Scenario 4: Update View (Object Check)

```python
PUT /api/articles/5/
Body: {"title": "Updated"}

Step 1: Authentication → John
Step 2: has_permission() → ✅ All pass
Step 3: Get object → Article 5 (author: Jane)
Step 4: has_object_permission() → ❌ John != Jane
Step 5: Return 403 Forbidden
```

### Permission Methods:

```python
class MyPermission(BasePermission):
    def has_permission(self, request, view):
        """
        View-level permission
        Called for all requests
        
        কখন call হয়:
        - সব requests এর জন্য
        - Object retrieve করার আগে
        
        কখন ব্যবহার করবেন:
        - General access control
        - Authentication check
        - Role-based access
        
        Example checks:
        - Is user authenticated?
        - Is user admin?
        - Is user verified?
        """
        return True  # or False
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission
        Called when accessing specific object
        
        কখন call হয়:
        - retrieve, update, partial_update, destroy
        - has_permission() pass করার পরে
        - Object retrieve করার পরে
        
        কখন ব্যবহার করবেন:
        - Object ownership check
        - Per-object access control
        - Resource-specific permissions
        
        Example checks:
        - Is user the owner?
        - Is user in collaborators?
        - Is object published?
        """
        return obj.author == request.user
```

### SAFE_METHODS:

```python
from rest_framework import permissions

# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
# Read-only methods

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read operations: সবাই
        if request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS → Allow
            return True
        
        # Write operations: শুধু author
        # POST, PUT, PATCH, DELETE → Check ownership
        return obj.author == request.user
```

**কখন কী হচ্ছে:**

```python
# GET request (SAFE_METHOD)
GET /api/articles/5/
→ request.method = 'GET'
→ 'GET' in SAFE_METHODS? ✅ Yes
→ Return True (সবাই read করতে পারবে)

# DELETE request (NOT SAFE)
DELETE /api/articles/5/
→ request.method = 'DELETE'
→ 'DELETE' in SAFE_METHODS? ❌ No
→ Check: obj.author == request.user
→ If True: Allow delete
→ If False: 403 Forbidden
```

### Multiple Permissions - AND Logic:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor, IsVerified]
    # ALL three must pass!

# Execution order:
# 1. IsAuthenticated.has_permission() → Must be True
# 2. IsAuthor.has_permission() → Must be True
# 3. IsVerified.has_permission() → Must be True
# If ANY returns False → 403 Forbidden
```

**Flow:**

```
Request arrives
↓
IsAuthenticated.has_permission()
  → False? → 403 Forbidden ❌
  → True? → Continue ✅
↓
IsAuthor.has_permission()
  → False? → 403 Forbidden ❌
  → True? → Continue ✅
↓
IsVerified.has_permission()
  → False? → 403 Forbidden ❌
  → True? → Continue ✅
↓
All passed → Execute view ✅
```

### Real-World Complete Example:

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

# permissions.py
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    - Read: সবাই (যদি published)
    - Write: শুধু author
    """
    
    def has_object_permission(self, request, view, obj):
        # Read operations
        if request.method in permissions.SAFE_METHODS:
            # Published articles: সবাই
            # Unpublished: শুধু author
            return obj.is_published or obj.author == request.user
        
        # Write operations: শুধু author
        return obj.author == request.user

# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

# Test scenarios:
# 1. Anonymous user, GET published article
#    → IsAuthenticatedOrReadOnly: ✅ (SAFE_METHOD)
#    → IsAuthorOrReadOnly: ✅ (is_published=True)
#    → Result: 200 OK

# 2. Anonymous user, GET unpublished article
#    → IsAuthenticatedOrReadOnly: ✅ (SAFE_METHOD)
#    → IsAuthorOrReadOnly: ❌ (not published, not author)
#    → Result: 403 Forbidden

# 3. Logged in user (not author), DELETE article
#    → IsAuthenticatedOrReadOnly: ✅ (authenticated)
#    → IsAuthorOrReadOnly: ❌ (not author)
#    → Result: 403 Forbidden

# 4. Author, DELETE own article
#    → IsAuthenticatedOrReadOnly: ✅ (authenticated)
#    → IsAuthorOrReadOnly: ✅ (is author)
#    → Result: 204 No Content
```

---

## Built-in Permission Classes

DRF ৬টি built-in permission classes প্রদান করে:

### 1. AllowAny

**কাজ:** সবাইকে access দেয়, authenticated বা না।

**কখন ব্যবহার করবেন:**
- Public endpoints
- Login/Registration pages
- Public blog posts

```python
from rest_framework.permissions import AllowAny

class PublicArticleView(APIView):
    permission_classes = [AllowAny]  # Anyone can access
    
    def get(self, request):
        articles = Article.objects.filter(is_published=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
```

**⚠️ Warning:** এটি default permission! যদি কোনো permission না দেন, AllowAny ব্যবহার হবে।

---

### 2. IsAuthenticated ⭐⭐⭐ (Most Common!)

**কাজ:** শুধু authenticated users access পাবে।

**কখন ব্যবহার করবেন:**
- User dashboard
- Profile pages
- Protected content
- 80%+ use cases!

```python
from rest_framework.permissions import IsAuthenticated

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Must be logged in
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**Example:**

```bash
# Without authentication
GET /api/articles/
→ 401 Unauthorized

# With authentication
GET /api/articles/
Authorization: Bearer eyJ0eXAi...
→ 200 OK (returns articles)
```

---

### 3. IsAdminUser

**কাজ:** শুধু admin users (is_staff=True) access পাবে।

**কখন ব্যবহার করবেন:**
- Admin panel
- User management
- System settings

```python
from rest_framework.permissions import IsAdminUser

class UserManagementView(APIView):
    permission_classes = [IsAdminUser]  # Only admins
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
```

**Check:**

```python
# User must have:
user.is_staff == True
```

---

### 4. IsAuthenticatedOrReadOnly ⭐⭐

**কাজ:** 
- Authenticated users: সব operations (read + write)
- Unauthenticated users: শুধু read (GET, HEAD, OPTIONS)

**কখন ব্যবহার করবেন:**
- Public blogs (সবাই read, শুধু authors write)
- Forums
- Comments sections

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Unauthenticated:
# GET /articles/     ✅ Allowed
# POST /articles/    ❌ 403 Forbidden

# Authenticated:
# GET /articles/     ✅ Allowed
# POST /articles/    ✅ Allowed
```

---

### 5. DjangoModelPermissions

**কাজ:** Django এর built-in model permissions ব্যবহার করে।

**Django Permissions:**
- `add_<model>` - Create
- `change_<model>` - Update
- `delete_<model>` - Delete
- `view_<model>` - View (Django 2.1+)

```python
from rest_framework.permissions import DjangoModelPermissions

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# User must have:
# - 'myapp.add_article' for POST
# - 'myapp.change_article' for PUT/PATCH
# - 'myapp.delete_article' for DELETE
```

**Assigning Permissions:**

```python
# Django admin or code
from django.contrib.auth.models import Permission

user = User.objects.get(username='john')
permission = Permission.objects.get(codename='add_article')
user.user_permissions.add(permission)
```

---

### 6. DjangoModelPermissionsOrAnonReadOnly

**কাজ:** DjangoModelPermissions + anonymous users শুধু read করতে পারবে।

```python
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Anonymous users: GET only
# Authenticated users: Based on Django permissions
```

---

## Custom Permissions

Built-in permissions যথেষ্ট না হলে custom permissions তৈরি করুন।

### Basic Structure:

```python
from rest_framework import permissions

class MyCustomPermission(permissions.BasePermission):
    """
    Custom permission description
    """
    
    def has_permission(self, request, view):
        """
        View-level permission
        Return True to allow, False to deny
        """
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission
        Return True to allow, False to deny
        """
        return True
```

### উদাহরণ 1: IsAuthor (সবচেয়ে Common!)

```python
class IsAuthor(permissions.BasePermission):
    """
    User শুধু নিজের content edit/delete করতে পারবে
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions: সবাই
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions: শুধু author
        return obj.author == request.user

# Usage:
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

### উদাহরণ 2: IsOwnerOrReadOnly

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object owner edit করতে পারবে, বাকিরা শুধু read
    """
    
    def has_object_permission(self, request, view, obj):
        # Read: সবাই
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write: শুধু owner
        return obj.owner == request.user
```

### উদাহরণ 3: IsPremiumUser

```python
class IsPremiumUser(permissions.BasePermission):
    """
    শুধু premium users access পাবে
    """
    message = 'You must be a premium user to access this.'
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_premium

# Usage:
class PremiumContentView(APIView):
    permission_classes = [IsPremiumUser]
    
    def get(self, request):
        return Response({'content': 'Premium content here'})
```

### উদাহরণ 4: IsVerifiedUser

```python
class IsVerifiedUser(permissions.BasePermission):
    """
    Email verified users only
    """
    message = 'Please verify your email first.'
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_email_verified
        )
```

### উদাহরণ 5: ReadOnly

```python
class ReadOnly(permissions.BasePermission):
    """
    শুধু read operations allow করবে
    """
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
```

### উদাহরণ 6: IsAdminOrReadOnly

```python
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin সব করতে পারবে, বাকিরা শুধু read
    """
    
    def has_permission(self, request, view):
        # Read: সবাই
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write: শুধু admin
        return request.user and request.user.is_staff
```

### Custom Error Messages:

```python
class IsAuthor(permissions.BasePermission):
    message = 'You must be the author to edit this article.'
    code = 'not_author'
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# Error response:
{
    "detail": "You must be the author to edit this article."
}
```

---

## Object-Level Permissions

Object-level permissions specific objects এর জন্য।

### কখন প্রয়োজন:

```python
# View-level: সব articles access
GET /api/articles/  ✅

# Object-level: শুধু নিজের article edit
PUT /api/articles/5/  ✅ (যদি আপনার article)
PUT /api/articles/6/  ❌ (অন্যের article)
```

### Implementation:

```python
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj = Article instance
        return obj.author == request.user

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# GET /articles/5/
# 1. IsAuthenticated.has_permission() → True
# 2. IsAuthor.has_object_permission(obj=Article #5) → True/False
```

### Multiple Owners:

```python
class IsAuthorOrCollaborator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Author বা collaborators edit করতে পারবে
        return (
            obj.author == request.user or
            request.user in obj.collaborators.all()
        )
```

### Role-Based Object Permissions:

```python
class CanEditArticle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin: সব articles
        if request.user.is_staff:
            return True
        
        # Author: নিজের articles
        if obj.author == request.user:
            return True
        
        # Editor: assigned articles
        if request.user.role == 'editor' and obj.assigned_editor == request.user:
            return True
        
        return False
```

---

## Combining Permissions

একাধিক permissions একসাথে ব্যবহার করা:

### AND Logic (সব permissions pass করতে হবে):

```python
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    # User must be authenticated AND author
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

### OR Logic (কোনো একটি permission pass করলেই হবে):

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class IsAuthenticatedOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            IsAuthenticated().has_permission(request, view) or
            IsAdminUser().has_permission(request, view)
        )

# অথবা Python 3.9+ এ:
class ArticleView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
```

### Complex Logic:

```python
class CanAccessArticle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read: সবাই (যদি published)
        if request.method in permissions.SAFE_METHODS:
            return obj.is_published or obj.author == request.user
        
        # Write: Author বা Admin
        return obj.author == request.user or request.user.is_staff
```

### Per-Action Permissions:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        """
        Different permissions for different actions
        """
        if self.action == 'list':
            # List: সবাই
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # Create: authenticated users
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Edit/Delete: author only
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            # Default
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
```

---

## Best Practices

### 1. Principle of Least Privilege

```python
# Good - Minimum necessary permissions
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]

# Bad - Too permissive
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # Anyone can delete!
```

### 2. Explicit Permissions

```python
# Good - Clear what's allowed
class ArticleView(APIView):
    permission_classes = [IsAuthenticated]

# Bad - Relying on defaults
class ArticleView(APIView):
    pass  # Uses AllowAny by default!
```

### 3. Separate Permission Files

```python
# permissions.py
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsPremiumUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_premium

# views.py
from .permissions import IsAuthor, IsPremiumUser

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
```

### 4. Descriptive Permission Names

```python
# Good - Clear names
class IsArticleAuthor(permissions.BasePermission):
    pass

class CanPublishArticle(permissions.BasePermission):
    pass

# Bad - Vague names
class Permission1(permissions.BasePermission):
    pass

class Check(permissions.BasePermission):
    pass
```

### 5. Test Permissions

```python
# tests.py
class PermissionTests(APITestCase):
    def test_only_author_can_edit(self):
        # Create article by user1
        article = Article.objects.create(author=self.user1, title='Test')
        
        # user2 tries to edit
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/api/articles/{article.id}/', {...})
        
        # Should be forbidden
        self.assertEqual(response.status_code, 403)
```

### 6. Document Permissions

```python
class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for articles.
    
    Permissions:
    - List: Anyone (public articles only)
    - Create: Authenticated users
    - Retrieve: Anyone (if published) or Author
    - Update/Delete: Author only
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: Blog API

```python
# permissions.py
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            # Public list
            return [AllowAny()]
        elif self.action == 'create':
            # Authenticated users can create
            return [IsAuthenticated()]
        else:
            # Author can edit/delete
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
    
    def get_queryset(self):
        # Authors see their drafts too
        if self.request.user.is_authenticated:
            return Article.objects.filter(
                Q(is_published=True) | Q(author=self.request.user)
            )
        return Article.objects.filter(is_published=True)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

### উদাহরণ 2: E-commerce

```python
# permissions.py
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

# views.py
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    # Anyone can view, only admin can add/edit

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    
    def get_queryset(self):
        # Users see only their orders
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
```

### উদাহরণ 3: Social Media

```python
# permissions.py
class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# views.py
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsPostOwner()]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        Like.objects.get_or_create(post=post, user=request.user)
        return Response({'status': 'liked'})
```

### উদাহরণ 4: Multi-Role System

```python
# permissions.py
class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'manager']

class CanApproveArticle(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'editor']

# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsAuthor()]
        elif self.action == 'destroy':
            return [IsAdminOrManager()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'], permission_classes=[CanApproveArticle])
    def approve(self, request, pk=None):
        article = self.get_object()
        article.is_approved = True
        article.save()
        return Response({'status': 'approved'})
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Permissions: https://www.django-rest-framework.org/api-guide/permissions/
- Django Permissions: https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization

### সম্পর্কিত বিষয়
- Authentication (আগের documentation)
- Throttling
- Filtering

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
