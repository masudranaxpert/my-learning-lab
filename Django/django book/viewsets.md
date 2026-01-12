# Django REST Framework - ViewSets & Routers

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [ViewSet কী এবং কেন?](#viewset-কী-এবং-কেন)
3. [ViewSet vs Generic Views](#viewset-vs-generic-views)
4. [ViewSet Types](#viewset-types)
   - [ViewSet](#viewset)
   - [GenericViewSet](#genericviewset)
   - [ModelViewSet](#modelviewset)
   - [ReadOnlyModelViewSet](#readonlymodelviewset)
5. [Routers](#routers)
   - [DefaultRouter](#defaultrouter)
   - [SimpleRouter](#simplerouter)
6. [Custom Actions (@action Decorator)](#custom-actions-action-decorator)
7. [ViewSet Methods এবং Attributes](#viewset-methods-এবং-attributes)
8. [Best Practices](#best-practices)
9. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)
10. [Customization Techniques](#customization-techniques)

---

## শেখার ক্রম

এই documentation টি পড়ার সময় নিচের ক্রম অনুসরণ করুন:

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **পরিচিতি** - ViewSet কী এবং কেন প্রয়োজন
2. ⭐⭐⭐ **ModelViewSet** - সবচেয়ে important এবং commonly used
3. ⭐⭐⭐ **Routers** - URL configuration automatic করা
4. ⭐⭐⭐ **ViewSet Methods এবং Attributes** - কোনটা কী return করে

### এরপর পড়ুন (গুরুত্বপূর্ণ):

5. ⭐⭐ **Custom Actions (@action Decorator)** - Extra functionality যোগ করা
6. ⭐⭐ **ViewSet vs Generic Views** - কখন কোনটি ব্যবহার করবেন
7. ⭐⭐ **Best Practices** - Professional code লেখার নিয়ম
8. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ** - Real-world scenarios

### শেষে পড়ুন (Advanced):

9. ⭐ **ViewSet এবং GenericViewSet** - Custom viewsets তৈরি করা
10. ⭐ **ReadOnlyModelViewSet** - Specific use cases
11. ⭐ **Customization Techniques** - Advanced scenarios

### দ্রষ্টব্য:
- ⭐⭐⭐ = অবশ্যই পড়তে হবে, real projects এ সবচেয়ে বেশি ব্যবহার হয়
- ⭐⭐ = গুরুত্বপূর্ণ, professional development এর জন্য জানা দরকার
- ⭐ = Advanced topics, specific scenarios এর জন্য

---

## পরিচিতি

আপনি যদি Generic Views দিয়ে কাজ করে থাকেন, তাহলে দেখেছেন যে একটি model এর জন্য অনেকগুলো views তৈরি করতে হয়:

```python
# Generic Views - ৪টি আলাদা views
class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Plus URL configuration
urlpatterns = [
    path('articles/', ArticleListCreateView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
]
```

এই একই কাজ ViewSet দিয়ে মাত্র একটি class এ:

```python
# ViewSet - একটি class, automatic URLs!
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Router automatically URLs তৈরি করবে
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls
```

দেখুন কত সহজ এবং clean!

---

## ViewSet কী এবং কেন?

### ViewSet কী?

**সহজ ভাষায়:** ViewSet হলো একটি class যেখানে একটি model এর সব related operations (list, create, retrieve, update, delete) একসাথে থাকে।

**Technical:** ViewSet হলো একটি class-based view যা HTTP methods (`.get()`, `.post()`) এর পরিবর্তে actions (`.list()`, `.create()`, `.retrieve()`) provide করে।

### কেন ViewSet ব্যবহার করবেন?

**Generic Views এর সমস্যা:**
- একটি model এর জন্য একাধিক views
- URL patterns manually define করতে হয়
- Queryset এবং serializer একাধিক জায়গায় repeat হয়

**ViewSet এর সুবিধা:**
- একটি class এ সব operations
- Automatic URL generation (routers দিয়ে)
- DRY principle - queryset একবার define করলেই হয়
- Consistent API structure
- কম code (৬০% কম!)

### Real-World তুলনা:

**Generic Views (৫০+ লাইন):**

```python
# views.py
class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# urls.py
urlpatterns = [
    path('articles/', ArticleListView.as_view()),
    path('articles/create/', ArticleCreateView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view()),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view()),
]
```

**ViewSet (মাত্র ১০ লাইন!):**

```python
# views.py
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# urls.py
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls

# Automatically generates:
# GET    /articles/          -> list
# POST   /articles/          -> create
# GET    /articles/{pk}/     -> retrieve
# PUT    /articles/{pk}/     -> update
# PATCH  /articles/{pk}/     -> partial_update
# DELETE /articles/{pk}/     -> destroy
```

---

## ViewSet vs Generic Views

### কখন ViewSet ব্যবহার করবেন:

✅ **ViewSet ব্যবহার করুন যখন:**
- একটি model এর জন্য full CRUD operations প্রয়োজন
- Standard RESTful API structure চান
- Automatic URL routing চান
- Consistent API design চান
- Large projects যেখানে অনেক models আছে

✅ **উদাহরণ Use Cases:**
- Blog API (Articles, Comments, Categories)
- E-commerce API (Products, Orders, Customers)
- Social Media API (Posts, Users, Likes)
- Any standard CRUD API

### কখন Generic Views ব্যবহার করবেন:

✅ **Generic Views ব্যবহার করুন যখন:**
- Specific operations প্রয়োজন (শুধু list, শুধু create)
- Custom URL structure চান
- Non-standard operations
- Simple API যেখানে কয়েকটি endpoints

✅ **উদাহরণ Use Cases:**
- Login/Logout endpoints
- Password reset
- File upload endpoints
- Custom dashboard APIs

### তুলনা Table:

| Feature | Generic Views | ViewSets |
|---------|--------------|----------|
| Code Amount | বেশি | কম (৬০% কম) |
| URL Configuration | Manual | Automatic |
| Flexibility | বেশি | কম |
| Learning Curve | সহজ | একটু কঠিন |
| Best For | Simple/Custom APIs | Standard CRUD APIs |
| URL Structure Control | Full control | Limited control |
| Industry Standard | ✓ | ✓✓✓ (বেশি popular) |

### 2025/2026 Recommendation:

**Professional Projects এ:**
- **70%+ cases:** `ModelViewSet` ব্যবহার করুন
- **20% cases:** Generic Views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`)
- **10% cases:** Custom `APIView`

**কারণ:**
- ViewSets দ্রুত development করতে দেয়
- Industry standard
- Less boilerplate code
- Easier to maintain

---

## ViewSet Types

Django REST Framework চার ধরনের ViewSets প্রদান করে:

### 1. ViewSet

**বর্ণনা:** সবচেয়ে basic ViewSet। কোনো built-in actions নেই।

**Inherits from:** `APIView`

**কখন ব্যবহার করবেন:** যখন আপনি সম্পূর্ণ custom actions চান।

**Built-in Actions:** কিছু নেই

**আপনাকে define করতে হবে:**
- `.list()` - List of objects
- `.create()` - Create new object
- `.retrieve()` - Single object
- `.update()` - Update object
- `.partial_update()` - Partial update
- `.destroy()` - Delete object

**উদাহরণ:**

```python
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    
    def list(self, request):
        """
        GET /users/
        Returns list of all users
        """
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        GET /users/{pk}/
        Returns a single user
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def create(self, request):
        """
        POST /users/
        Creates a new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

**URL Configuration:**

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

**কখন ব্যবহার করবেন:**
- খুব কম ব্যবহৃত হয়
- যখন সম্পূর্ণ custom logic প্রয়োজন
- Non-model based operations

### 2. GenericViewSet

**বর্ণনা:** `GenericAPIView` এর functionality সহ ViewSet।

**Inherits from:** `GenericAPIView`

**Built-in Features:**
- `queryset` এবং `serializer_class` attributes
- `get_object()`, `get_queryset()` methods
- Pagination, filtering support

**Built-in Actions:** কিছু নেই (Mixins এর সাথে combine করতে হবে)

**কখন ব্যবহার করবেন:** Mixins এর সাথে combine করে custom viewsets তৈরি করা।

**উদাহরণ:**

```python
from rest_framework import mixins, viewsets

class ArticleViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    A viewset that provides `list`, `create`, and `retrieve` actions.
    Update এবং Delete নেই।
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**কী হয়:**
- `ListModelMixin` -> `.list()` method যোগ করে
- `CreateModelMixin` -> `.create()` method যোগ করে
- `RetrieveModelMixin` -> `.retrieve()` method যোগ করে

**Generated URLs:**

```
GET  /articles/          -> list
POST /articles/          -> create
GET  /articles/{pk}/     -> retrieve
```

**কখন ব্যবহার করবেন:**
- যখন সব CRUD operations প্রয়োজন নেই
- Specific mixins select করতে চান
- Custom combination চান

### 3. ModelViewSet ⭐⭐⭐ (সবচেয়ে Important!)

**বর্ণনা:** সম্পূর্ণ CRUD operations সহ ViewSet। সবচেয়ে commonly used!

**Inherits from:** `GenericAPIView` + সব mixins

**Built-in Actions:**
- `.list()` - GET /articles/
- `.create()` - POST /articles/
- `.retrieve()` - GET /articles/{pk}/
- `.update()` - PUT /articles/{pk}/
- `.partial_update()` - PATCH /articles/{pk}/
- `.destroy()` - DELETE /articles/{pk}/

**Minimum Requirements:**
- `queryset` attribute
- `serializer_class` attribute

**Basic উদাহরণ:**

```python
from rest_framework import viewsets

class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing article instances.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**এই ছোট্ট code টি automatically provide করে:**

| HTTP Method | URL | Action | কাজ |
|------------|-----|--------|-----|
| GET | /articles/ | list | সব articles এর list |
| POST | /articles/ | create | নতুন article তৈরি |
| GET | /articles/{pk}/ | retrieve | Single article |
| PUT | /articles/{pk}/ | update | Full update |
| PATCH | /articles/{pk}/ | partial_update | Partial update |
| DELETE | /articles/{pk}/ | destroy | Article delete |

**Advanced উদাহরণ:**

```python
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Dynamic queryset
        user = self.request.user
        if user.is_staff:
            return Article.objects.all()
        return Article.objects.filter(is_published=True)
    
    def get_serializer_class(self):
        # Different serializers for different actions
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleSerializer
    
    def perform_create(self, serializer):
        # Custom logic on create
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        # Custom logic on update
        serializer.save(updated_by=self.request.user)
```

**কখন ব্যবহার করবেন:**
- **সবচেয়ে বেশি ব্যবহৃত হয়!**
- যখন full CRUD operations প্রয়োজন
- Standard RESTful API
- 70%+ real-world cases

### 4. ReadOnlyModelViewSet

**বর্ণনা:** শুধুমাত্র read operations (list এবং retrieve)।

**Built-in Actions:**
- `.list()` - GET /articles/
- `.retrieve()` - GET /articles/{pk}/

**কখন ব্যবহার করবেন:** যখন শুধুমাত্র data read করতে দিতে চান, modify নয়।

**উদাহরণ:**

```python
from rest_framework import viewsets

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides only `list` and `retrieve` actions.
    Create, Update, Delete নেই।
    """
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
```

**Generated URLs:**

```
GET /articles/          -> list
GET /articles/{pk}/     -> retrieve
```

**Use Cases:**
- Public APIs যেখানে শুধু data দেখানো হয়
- Archive/historical data
- Reference data (Categories, Tags)
- Documentation APIs

---

## Routers

Routers automatically URL patterns generate করে ViewSets এর জন্য।

### কেন Routers ব্যবহার করবেন?

**Manual URL Configuration (Generic Views):**

```python
urlpatterns = [
    path('articles/', ArticleListView.as_view()),
    path('articles/create/', ArticleCreateView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view()),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view()),
]
```

**Router (ViewSets):**

```python
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls
```

দেখুন কত সহজ!

### DefaultRouter

**Features:**
- Standard REST URL patterns
- API root view (browsable API homepage)
- Format suffixes (.json, .api)

**Basic ব্যবহার:**

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'users', UserViewSet, basename='user')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
```

**Generated URLs:**

```
GET    /                      -> API root (browsable API)
GET    /articles/             -> article-list
POST   /articles/             -> article-list
GET    /articles/{pk}/        -> article-detail
PUT    /articles/{pk}/        -> article-detail
PATCH  /articles/{pk}/        -> article-detail
DELETE /articles/{pk}/        -> article-detail
GET    /users/                -> user-list
POST   /users/                -> user-list
...
```

**Existing urlpatterns এর সাথে:**

```python
from django.urls import path, include

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

# URLs হবে:
# /api/articles/
# /api/users/
# /api/comments/
```

### SimpleRouter

**Features:**
- Basic URL patterns
- কোনো API root view নেই
- Lightweight

**কখন ব্যবহার করবেন:**
- API root view প্রয়োজন নেই
- Minimal URLs চান

**উদাহরণ:**

```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'articles', ArticleViewSet)
```

**Generated URLs (API root নেই):**

```
GET    /articles/
POST   /articles/
GET    /articles/{pk}/
PUT    /articles/{pk}/
PATCH  /articles/{pk}/
DELETE /articles/{pk}/
```

### basename Parameter

**কী:** URL names এর prefix।

**কখন প্রয়োজন:**
- যখন `queryset` attribute ViewSet এ define করা নেই
- যখন `get_queryset()` override করা হয়েছে

**উদাহরণ:**

```python
# queryset আছে - basename optional
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

router.register(r'articles', ArticleViewSet)  # basename auto-detected

# queryset নেই - basename required
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

router.register(r'articles', ArticleViewSet, basename='article')  # basename required!
```

**basename কীভাবে ব্যবহৃত হয়:**

```python
router.register(r'articles', ArticleViewSet, basename='article')

# Generated URL names:
# article-list
# article-detail

# Reverse URL:
from django.urls import reverse
url = reverse('article-list')  # /articles/
url = reverse('article-detail', kwargs={'pk': 5})  # /articles/5/
```

---

## Custom Actions (@action Decorator)

Standard CRUD operations এর বাইরে custom endpoints তৈরি করতে `@action` decorator ব্যবহার করুন।

### কী এবং কেন?

**সমস্যা:** ModelViewSet শুধু standard CRUD দেয়। কিন্তু যদি custom operations প্রয়োজন হয়?

**সমাধান:** `@action` decorator দিয়ে custom endpoints তৈরি করা।

### Basic Syntax

```python
from rest_framework.decorators import action

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Custom action to publish an article
        URL: POST /articles/{pk}/publish/
        """
        article = self.get_object()
        article.is_published = True
        article.save()
        return Response({'status': 'article published'})
```

### detail Parameter

**detail=True:** Single object এর জন্য (URL এ pk থাকবে)

```python
@action(detail=True, methods=['post'])
def publish(self, request, pk=None):
    # URL: /articles/{pk}/publish/
    article = self.get_object()
    # ... logic
```

**detail=False:** Collection এর জন্য (URL এ pk থাকবে না)

```python
@action(detail=False, methods=['get'])
def recent(self, request):
    # URL: /articles/recent/
    recent_articles = Article.objects.all().order_by('-created_at')[:10]
    # ... logic
```

### methods Parameter

**Default:** `['get']`

**Multiple methods:**

```python
@action(detail=True, methods=['post', 'delete'])
def like(self, request, pk=None):
    article = self.get_object()
    
    if request.method == 'POST':
        # Add like
        Like.objects.create(article=article, user=request.user)
        return Response({'status': 'liked'})
    
    elif request.method == 'DELETE':
        # Remove like
        Like.objects.filter(article=article, user=request.user).delete()
        return Response({'status': 'unliked'})
```

### Custom Permissions

```python
from rest_framework.permissions import IsAdminUser

@action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
def approve(self, request, pk=None):
    """
    Only admin can approve articles
    """
    article = self.get_object()
    article.is_approved = True
    article.save()
    return Response({'status': 'approved'})
```

### Complete উদাহরণ

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Publish an article
        URL: POST /articles/{pk}/publish/
        """
        article = self.get_object()
        article.is_published = True
        article.published_at = timezone.now()
        article.save()
        
        serializer = self.get_serializer(article)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """
        Unpublish an article
        URL: POST /articles/{pk}/unpublish/
        """
        article = self.get_object()
        article.is_published = False
        article.save()
        return Response({'status': 'article unpublished'})
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent articles
        URL: GET /articles/recent/
        """
        recent_articles = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular articles
        URL: GET /articles/popular/
        """
        popular_articles = self.get_queryset().order_by('-views')[:10]
        serializer = self.get_serializer(popular_articles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like an article
        URL: POST /articles/{pk}/like/
        """
        article = self.get_object()
        user = request.user
        
        Like.objects.get_or_create(article=article, user=user)
        
        return Response({
            'status': 'liked',
            'total_likes': article.likes.count()
        })
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for an article
        URL: GET /articles/{pk}/comments/
        """
        article = self.get_object()
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
```

**Generated URLs:**

```
# Standard CRUD
GET    /articles/
POST   /articles/
GET    /articles/{pk}/
PUT    /articles/{pk}/
PATCH  /articles/{pk}/
DELETE /articles/{pk}/

# Custom Actions
POST   /articles/{pk}/publish/
POST   /articles/{pk}/unpublish/
GET    /articles/recent/
GET    /articles/popular/
POST   /articles/{pk}/like/
GET    /articles/{pk}/comments/
```

---

## ViewSet Methods এবং Attributes

### Built-in Actions (ModelViewSet)

| Method | HTTP | URL | কী করে | Return করে |
|--------|------|-----|---------|-------------|
| `list()` | GET | /articles/ | সব objects এর list | List of objects (paginated) |
| `create()` | POST | /articles/ | নতুন object তৈরি | Created object (201) |
| `retrieve()` | GET | /articles/{pk}/ | Single object | Single object |
| `update()` | PUT | /articles/{pk}/ | Full update | Updated object |
| `partial_update()` | PATCH | /articles/{pk}/ | Partial update | Updated object |
| `destroy()` | DELETE | /articles/{pk}/ | Object delete | Empty (204) |

### Attributes

| Attribute | Type | কী | উদাহরণ |
|-----------|------|-----|---------|
| `queryset` | QuerySet | Database থেকে কোন objects | `Article.objects.all()` |
| `serializer_class` | Serializer | Data কীভাবে serialize করবে | `ArticleSerializer` |
| `permission_classes` | List | কে access করতে পারবে | `[IsAuthenticated]` |
| `authentication_classes` | List | কীভাবে authenticate করবে | `[TokenAuthentication]` |
| `filter_backends` | List | Filtering/searching | `[DjangoFilterBackend]` |
| `pagination_class` | Class | Pagination | `PageNumberPagination` |
| `lookup_field` | String | কোন field দিয়ে lookup | `'slug'` (default: `'pk'`) |

### Customization Methods

| Method | কখন Call হয় | কী করে | Return করে |
|--------|-------------|---------|-------------|
| `get_queryset()` | প্রতিটি request এ | Dynamic queryset | QuerySet |
| `get_serializer_class()` | Serializer তৈরির সময় | Dynamic serializer | Serializer class |
| `get_object()` | Detail views এ | Single object retrieve | Model instance |
| `get_permissions()` | প্রতিটি request এ | Dynamic permissions | List of permissions |
| `perform_create(serializer)` | Create এর সময় | Custom create logic | None (saves object) |
| `perform_update(serializer)` | Update এর সময় | Custom update logic | None (saves object) |
| `perform_destroy(instance)` | Delete এর সময় | Custom delete logic | None (deletes object) |

### Special Attributes

| Attribute | Type | কী | উদাহরণ |
|-----------|------|-----|---------|
| `action` | String | Current action name | `'list'`, `'create'`, `'retrieve'` |
| `basename` | String | URL name prefix | `'article'` |
| `detail` | Boolean | Detail view কিনা | `True` or `False` |

**ব্যবহার:**

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_serializer_class(self):
        # self.action ব্যবহার করে
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleSerializer
```

---

## Best Practices

### 1. ModelViewSet ব্যবহার করুন Standard CRUD এর জন্য

```python
# Good - Clean and concise
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Bad - Generic Views দিয়ে অনেক code
class ArticleListView(ListCreateAPIView):
    # ...
class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    # ...
```

### 2. get_queryset() Override করুন Dynamic Filtering এর জন্য

```python
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Article.objects.all()
        return Article.objects.filter(is_published=True)
```

### 3. action-based Serializers

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer  # Lighter
        elif self.action == 'retrieve':
            return ArticleDetailSerializer  # Detailed
        return ArticleSerializer  # Default
```

### 4. perform_create/update/destroy ব্যবহার করুন

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.save()
```

### 5. Action-Based Permissions

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:  # update, destroy
            return [IsAuthenticated(), IsAuthor()]
```

### 6. ReadOnlyModelViewSet ব্যবহার করুন Read-Only APIs এর জন্য

```python
# Good - Explicit read-only
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Bad - ModelViewSet এবং permissions দিয়ে restrict করা
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly]  # Confusing
```

### 7. Custom Actions এর জন্য Descriptive Names

```python
# Good - Clear names
@action(detail=True, methods=['post'])
def publish(self, request, pk=None):
    pass

@action(detail=False)
def recent_articles(self, request):
    pass

# Bad - Unclear names
@action(detail=True, methods=['post'])
def do_something(self, request, pk=None):
    pass
```

### 8. basename সবসময় Provide করুন যদি get_queryset() Override করেন

```python
# Good
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

router.register(r'articles', ArticleViewSet, basename='article')

# Bad - basename নেই, error হবে
router.register(r'articles', ArticleViewSet)
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: Blog API - Complete Setup

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# serializers.py
class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'author_name', 'category', 'created_at', 'views']

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'is_published']

# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'category')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_published', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleCreateUpdateSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsAuthor()]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        article = self.get_object()
        article.is_published = True
        article.published_at = timezone.now()
        article.save()
        return Response({'status': 'published'})
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, slug=None):
        article = self.get_object()
        article.views += 1
        article.save()
        return Response({'views': article.views})
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_articles = self.get_queryset().order_by('-views')[:10]
        serializer = self.get_serializer(popular_articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_articles = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_articles, many=True)
        return Response(serializer.data)

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('api/', include(router.urls)),
]

# Generated URLs:
# GET    /api/articles/                    -> list
# POST   /api/articles/                    -> create
# GET    /api/articles/{slug}/             -> retrieve
# PUT    /api/articles/{slug}/             -> update
# PATCH  /api/articles/{slug}/             -> partial_update
# DELETE /api/articles/{slug}/             -> destroy
# POST   /api/articles/{slug}/publish/     -> publish
# POST   /api/articles/{slug}/increment_views/ -> increment_views
# GET    /api/articles/popular/            -> popular
# GET    /api/articles/recent/             -> recent
```

### উদাহরণ 2: E-commerce Product API

```python
# views.py
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        on_sale_products = Product.objects.filter(
            is_active=True,
            discount__gt=0
        )
        serializer = self.get_serializer(on_sale_products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity', 0)
        
        product.stock += quantity
        product.save()
        
        return Response({
            'product': product.name,
            'new_stock': product.stock
        })

# urls.py
router.register(r'products', ProductViewSet, basename='product')
```

### উদাহরণ 3: User Profile API

```python
# views.py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Invalid old password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'status': 'password changed'})

# urls.py
router.register(r'users', UserViewSet, basename='user')

# URLs:
# GET  /users/me/                -> Current user
# POST /users/change_password/  -> Change password
```

---

## Customization Techniques

### 1. Nested Resources

```python
# views.py
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        article_id = self.kwargs['article_pk']
        return Comment.objects.filter(article_id=article_id)
    
    def perform_create(self, serializer):
        article_id = self.kwargs['article_pk']
        serializer.save(
            author=self.request.user,
            article_id=article_id
        )

# urls.py (using drf-nested-routers)
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)

articles_router = routers.NestedDefaultRouter(router, r'articles', lookup='article')
articles_router.register(r'comments', CommentViewSet, basename='article-comments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(articles_router.urls)),
]

# URLs:
# /api/articles/{article_pk}/comments/
# /api/articles/{article_pk}/comments/{pk}/
```

### 2. Custom Response Format

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data,
                'message': 'Articles retrieved successfully'
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
```

### 3. Soft Delete

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_deleted=False)
    serializer_class = ArticleSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def restore(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        article.is_deleted = False
        article.deleted_at = None
        article.save()
        return Response({'status': 'restored'})
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework ViewSets: https://www.django-rest-framework.org/api-guide/viewsets/
- Django REST Framework Routers: https://www.django-rest-framework.org/api-guide/routers/
- Classy Django REST Framework: http://www.cdrf.co

### সম্পর্কিত বিষয়
- Generic Views
- Serializers
- Permissions
- Authentication
- Filtering এবং Searching

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
