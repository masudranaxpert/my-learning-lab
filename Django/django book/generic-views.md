# Django REST Framework - Generic Views

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Generic Views কী এবং কেন?](#generic-views-কী-এবং-কেন)
3. [মূল Concepts বোঝা](#মূল-concepts-বোঝা)
   - [queryset কী?](#queryset-কী)
   - [serializer_class কী?](#serializer_class-কী)
   - [lookup_field কী?](#lookup_field-কী)
4. [GenericAPIView](#genericapiview)
5. [Mixins বিস্তারিত](#mixins-বিস্তারিত)
6. [Concrete Generic Views](#concrete-generic-views)
7. [প্রতিটি Generic View এর বিস্তারিত](#প্রতিটি-generic-view-এর-বিস্তারিত)
8. [Customization Methods](#customization-methods)
9. [Best Practices](#best-practices)
10. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)

---

## শেখার ক্রম

এই documentation টি পড়ার সময় নিচের ক্রম অনুসরণ করুন:

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **পরিচিতি** - Generic Views কী এবং কেন প্রয়োজন
2. ⭐⭐⭐ **মূল Concepts বোঝা** - queryset, serializer_class, lookup_field
3. ⭐⭐⭐ **Concrete Generic Views** - কোনটা কী কাজ করে
4. ⭐⭐⭐ **ListCreateAPIView** - সবচেয়ে commonly used
5. ⭐⭐⭐ **RetrieveUpdateDestroyAPIView** - Detail endpoints এর জন্য

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **প্রতিটি Generic View এর বিস্তারিত** - সব views এর উদাহরণ
7. ⭐⭐ **Customization Methods** - get_queryset(), perform_create() ইত্যাদি
8. ⭐⭐ **Best Practices** - Professional code লেখার নিয়ম
9. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ** - Real-world scenarios

### শেষে পড়ুন (Advanced):

10. ⭐ **GenericAPIView এবং Mixins** - কীভাবে internally কাজ করে
11. ⭐ **Advanced Customization** - Complex scenarios

### দ্রষ্টব্য:
- ⭐⭐⭐ = অবশ্যই পড়তে হবে, এগুলো ছাড়া কাজ করা যাবে না
- ⭐⭐ = গুরুত্বপূর্ণ, ভালো code লেখার জন্য জানা দরকার
- ⭐ = Advanced topics, প্রয়োজন হলে পড়বেন

---

## পরিচিতি

আপনি যদি `APIView` দিয়ে কাজ করে থাকেন, তাহলে দেখেছেন যে একই ধরনের code বারবার লিখতে হয়:

```python
# APIView দিয়ে Article List
class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

এই একই কাজ Generic Views দিয়ে মাত্র ৩ লাইনে:

```python
# Generic View দিয়ে Article List
class ArticleListView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

দেখুন কত সহজ! এবং functionality একই।

---

## Generic Views কী এবং কেন?

### Generic Views কী?

Generic Views হলো Django REST Framework এর pre-built views যা common API patterns এর জন্য ready-to-use code প্রদান করে।

**সহজ ভাষায়:** এগুলো হলো "তৈরি খাবার" এর মতো। আপনাকে সব কিছু নিজে রান্না (code) করতে হবে না, শুধু বলে দিতে হবে কোন model এবং কোন serializer ব্যবহার করবেন।

### কেন Generic Views ব্যবহার করবেন?

**APIView এর সমস্যা:**
- অনেক boilerplate code
- একই logic বারবার লিখতে হয়
- Error handling manually করতে হয়
- Pagination, filtering manually setup করতে হয়

**Generic Views এর সুবিধা:**
- কম code (৮০% কম!)
- Built-in error handling
- Automatic pagination support
- DRY (Don't Repeat Yourself) principle
- Maintainable এবং readable code

### Real-World তুলনা:

```python
# APIView - ২৫+ লাইন code
class ArticleDetailView(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=204)

# Generic View - মাত্র ৩ লাইন!
class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

---

## মূল Concepts বোঝা

Generic Views ব্যবহার করার আগে তিনটি মূল concept বুঝতে হবে:

### queryset কী?

**সহজ ভাষায়:** `queryset` হলো database থেকে কোন objects নিয়ে কাজ করবেন সেটা বলে দেওয়া।

**Technical:** এটি একটি Django QuerySet যা database থেকে objects retrieve করে।

**উদাহরণ:**

```python
class ArticleListView(ListAPIView):
    # এই view সব Article objects নিয়ে কাজ করবে
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**বিভিন্ন queryset এর উদাহরণ:**

```python
# সব objects
queryset = Article.objects.all()

# শুধু published articles
queryset = Article.objects.filter(is_published=True)

# Ordering সহ
queryset = Article.objects.all().order_by('-created_at')

# Related objects সহ (performance optimization)
queryset = Article.objects.select_related('author').prefetch_related('tags')

# Specific fields only
queryset = Article.objects.only('id', 'title', 'created_at')
```

**কী হয় যখন queryset define করি:**

1. View এই queryset থেকে data নেয়
2. Serializer এই data কে JSON এ convert করে
3. Client কে response পাঠায়

**Dynamic queryset (Advanced):**

যদি queryset dynamic হতে হয় (যেমন logged-in user এর উপর নির্ভর করে), তাহলে `get_queryset()` method ব্যবহার করুন:

```python
class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        # Current user এর articles
        return Article.objects.filter(author=self.request.user)
```

### serializer_class কী?

**সহজ ভাষায়:** `serializer_class` হলো data কে কীভাবে JSON এ convert করবেন এবং validation করবেন সেটা বলে দেওয়া।

**Technical:** এটি একটি Serializer class যা model instances কে JSON এ convert করে এবং incoming data validate করে।

**উদাহরণ:**

```python
# serializers.py
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at']

# views.py
class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    # এই serializer ব্যবহার করে data convert হবে
    serializer_class = ArticleSerializer
```

**কী হয় যখন serializer_class define করি:**

**GET Request এ:**
1. View queryset থেকে Article objects নেয়
2. Serializer এগুলোকে JSON এ convert করে
3. Client কে JSON response পাঠায়

**POST/PUT Request এ:**
1. Client JSON data পাঠায়
2. Serializer data validate করে
3. Valid হলে database এ save করে
4. Response পাঠায়

**Multiple Serializers (Advanced):**

বিভিন্ন actions এর জন্য বিভিন্ন serializers:

```python
class ArticleListView(ListCreateAPIView):
    queryset = Article.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            # List এর জন্য light serializer
            return ArticleListSerializer
        else:
            # Create এর জন্য detailed serializer
            return ArticleCreateSerializer
```

### lookup_field কী?

**সহজ ভাষায়:** `lookup_field` হলো URL থেকে কোন field দিয়ে specific object খুঁজবেন সেটা বলে দেওয়া।

**Default:** `pk` (primary key)

**উদাহরণ:**

```python
# Default - pk দিয়ে খোঁজা
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # lookup_field = 'pk'  # Default, লেখার দরকার নেই

# URL: /articles/5/  -> pk=5 দিয়ে খুঁজবে
```

**Custom lookup_field:**

```python
# slug দিয়ে খোঁজা
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

# URL: /articles/my-first-article/  -> slug='my-first-article' দিয়ে খুঁজবে
```

**অন্যান্য উদাহরণ:**

```python
# Username দিয়ে
lookup_field = 'username'
# URL: /users/john_doe/

# UUID দিয়ে
lookup_field = 'uuid'
# URL: /articles/550e8400-e29b-41d4-a716-446655440000/

# Custom field
lookup_field = 'article_id'
# URL: /articles/ART-12345/
```

**URL Pattern এর সাথে match করতে হবে:**

```python
# views.py
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

# urls.py
urlpatterns = [
    # lookup_field এর নাম URL pattern এ থাকতে হবে
    path('articles/<slug:slug>/', ArticleDetailView.as_view()),
]
```

---

## GenericAPIView

`GenericAPIView` হলো সব Generic Views এর base class। এটি `APIView` কে extend করে এবং common functionality যোগ করে।

**কী কী functionality যোগ করে:**

1. **queryset এবং serializer_class support**
2. **get_object()** - Single object retrieve করা
3. **get_queryset()** - Queryset customize করা
4. **get_serializer()** - Serializer instance তৈরি করা
5. **Pagination support**
6. **Filtering support**

**সরাসরি ব্যবহার করা হয় না:**

আপনি সাধারণত `GenericAPIView` সরাসরি ব্যবহার করবেন না। এটি Mixins এর সাথে combine করে অথবা Concrete Generic Views ব্যবহার করবেন।

**উদাহরণ (শুধু বোঝার জন্য):**

```python
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class ArticleListView(GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get(self, request):
        # get_queryset() method ব্যবহার করা
        queryset = self.get_queryset()
        # get_serializer() method ব্যবহার করা
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

কিন্তু এটার চেয়ে ভালো হলো Concrete Generic Views ব্যবহার করা।

---

## Mixins বিস্তারিত

Mixins হলো ছোট ছোট reusable classes যা specific functionality প্রদান করে। এগুলো `GenericAPIView` এর সাথে combine করে powerful views তৈরি করা যায়।

### পাঁচটি Mixins:

| Mixin | Method | কাজ | HTTP Method |
|-------|--------|-----|-------------|
| ListModelMixin | list() | Objects এর list | GET |
| CreateModelMixin | create() | নতুন object তৈরি | POST |
| RetrieveModelMixin | retrieve() | Single object | GET |
| UpdateModelMixin | update(), partial_update() | Object update | PUT, PATCH |
| DestroyModelMixin | destroy() | Object delete | DELETE |

### কীভাবে কাজ করে:

**১. ListModelMixin:**

```python
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class ArticleListView(mixins.ListModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get(self, request, *args, **kwargs):
        # ListModelMixin এর list() method call করা
        return self.list(request, *args, **kwargs)
```

**কী হয়:**
1. `list()` method queryset থেকে সব objects নেয়
2. Serializer দিয়ে JSON এ convert করে
3. Pagination apply করে (যদি থাকে)
4. Response return করে

**২. CreateModelMixin:**

```python
class ArticleCreateView(mixins.CreateModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def post(self, request, *args, **kwargs):
        # CreateModelMixin এর create() method call করা
        return self.create(request, *args, **kwargs)
```

**কী হয়:**
1. `create()` method request data নেয়
2. Serializer দিয়ে validate করে
3. Valid হলে database এ save করে
4. 201 Created status সহ response return করে

**৩. RetrieveModelMixin:**

```python
class ArticleDetailView(mixins.RetrieveModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
```

**কী হয়:**
1. URL থেকে pk/lookup_field নেয়
2. Database থেকে object খুঁজে
3. Serializer দিয়ে JSON এ convert করে
4. Response return করে (404 যদি না পাওয়া যায়)

**৪. UpdateModelMixin:**

```python
class ArticleUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def put(self, request, *args, **kwargs):
        # Full update
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        # Partial update
        return self.partial_update(request, *args, **kwargs)
```

**কী হয়:**
1. Object খুঁজে নেয়
2. Request data দিয়ে update করে
3. Validate করে
4. Save করে এবং response return করে

**৫. DestroyModelMixin:**

```python
class ArticleDeleteView(mixins.DestroyModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

**কী হয়:**
1. Object খুঁজে নেয়
2. Delete করে
3. 204 No Content status return করে

### একাধিক Mixins একসাথে:

```python
class ArticleListCreateView(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

**কিন্তু এটা করার দরকার নেই!** কারণ DRF এর জন্য Concrete Generic Views আছে।

---

## Concrete Generic Views

Concrete Generic Views হলো `GenericAPIView` + Mixins এর pre-built combinations। এগুলো সবচেয়ে বেশি ব্যবহৃত হয়।

### সব Concrete Generic Views:

| View Class | Mixins | HTTP Methods | কাজ | Use Case |
|-----------|--------|--------------|-----|----------|
| **CreateAPIView** | Create | POST | নতুন object তৈরি | Registration, Add item |
| **ListAPIView** | List | GET | List দেখানো | Show all items |
| **RetrieveAPIView** | Retrieve | GET | Single object | Item details |
| **UpdateAPIView** | Update | PUT, PATCH | Update করা | Edit item |
| **DestroyAPIView** | Destroy | DELETE | Delete করা | Remove item |
| **ListCreateAPIView** | List + Create | GET, POST | List এবং create | Most common! |
| **RetrieveUpdateAPIView** | Retrieve + Update | GET, PUT, PATCH | View এবং edit | Profile edit |
| **RetrieveDestroyAPIView** | Retrieve + Destroy | GET, DELETE | View এবং delete | View & remove |
| **RetrieveUpdateDestroyAPIView** | All except List | GET, PUT, PATCH, DELETE | সব operations | Detail page |

### কোনটা কখন ব্যবহার করবেন:

**সবচেয়ে commonly used (80% cases):**

1. **ListCreateAPIView** - List endpoint এর জন্য
   ```
   GET  /articles/     -> সব articles
   POST /articles/     -> নতুন article তৈরি
   ```

2. **RetrieveUpdateDestroyAPIView** - Detail endpoint এর জন্য
   ```
   GET    /articles/5/  -> Article দেখা
   PUT    /articles/5/  -> Article update
   PATCH  /articles/5/  -> Partial update
   DELETE /articles/5/  -> Article delete
   ```

**বাকি views (20% cases):**

যখন specific operations প্রয়োজন:
- শুধু list দেখাতে হবে -> `ListAPIView`
- শুধু create করতে হবে -> `CreateAPIView`
- শুধু view করতে হবে -> `RetrieveAPIView`

---

## প্রতিটি Generic View এর বিস্তারিত

### 1. CreateAPIView

**কাজ:** শুধুমাত্র নতুন object তৈরি করা।

**HTTP Methods:** POST

**কখন ব্যবহার করবেন:** যখন শুধু create করতে দিতে চান, list দেখাতে চান না।

**Basic উদাহরণ:**

```python
from rest_framework.generics import CreateAPIView

class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**URL:**

```python
path('articles/create/', ArticleCreateView.as_view())
```

**Request:**

```bash
POST /articles/create/
{
    "title": "My Article",
    "content": "Article content here"
}
```

**Response:**

```json
{
    "id": 1,
    "title": "My Article",
    "content": "Article content here",
    "created_at": "2026-01-12T10:00:00Z"
}
```

**Customization - author automatically set করা:**

```python
class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Author automatically current user set হবে
        serializer.save(author=self.request.user)
```

### 2. ListAPIView

**কাজ:** শুধুমাত্র objects এর list দেখানো।

**HTTP Methods:** GET

**কখন ব্যবহার করবেন:** যখন শুধু list দেখাতে চান, create করতে দিতে চান না।

**Basic উদাহরণ:**

```python
from rest_framework.generics import ListAPIView

class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**URL:**

```python
path('articles/', ArticleListView.as_view())
```

**Response:**

```json
[
    {
        "id": 1,
        "title": "First Article",
        "created_at": "2026-01-12T10:00:00Z"
    },
    {
        "id": 2,
        "title": "Second Article",
        "created_at": "2026-01-12T11:00:00Z"
    }
]
```

**Filtering উদাহরণ:**

```python
class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        # Query parameter থেকে filter করা
        queryset = Article.objects.all()
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset

# URL: /articles/?category=tech
```

### 3. RetrieveAPIView

**কাজ:** শুধুমাত্র single object দেখানো।

**HTTP Methods:** GET

**কখন ব্যবহার করবেন:** যখন শুধু view করতে দিতে চান, edit/delete করতে দিতে চান না।

**Basic উদাহরণ:**

```python
from rest_framework.generics import RetrieveAPIView

class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**URL:**

```python
path('articles/<int:pk>/', ArticleDetailView.as_view())
```

**Request:**

```bash
GET /articles/5/
```

**Response:**

```json
{
    "id": 5,
    "title": "My Article",
    "content": "Full content here",
    "author": "John Doe",
    "created_at": "2026-01-12T10:00:00Z"
}
```

**Slug দিয়ে retrieve:**

```python
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

# URL: /articles/my-first-article/
```

### 4. UpdateAPIView

**কাজ:** শুধুমাত্র object update করা।

**HTTP Methods:** PUT, PATCH

**কখন ব্যবহার করবেন:** যখন শুধু edit করতে দিতে চান।

**Basic উদাহরণ:**

```python
from rest_framework.generics import UpdateAPIView

class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
```

**URL:**

```python
path('articles/<int:pk>/update/', ArticleUpdateView.as_view())
```

**PUT Request (Full Update):**

```bash
PUT /articles/5/update/
{
    "title": "Updated Title",
    "content": "Updated content"
}
```

**PATCH Request (Partial Update):**

```bash
PATCH /articles/5/update/
{
    "title": "Only title updated"
}
```

**Customization:**

```python
class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    
    def perform_update(self, serializer):
        # Update করার সময় updated_by set করা
        serializer.save(updated_by=self.request.user)
```

### 5. DestroyAPIView

**কাজ:** শুধুমাত্র object delete করা।

**HTTP Methods:** DELETE

**কখন ব্যবহার করবেন:** যখন শুধু delete করতে দিতে চান।

**Basic উদাহরণ:**

```python
from rest_framework.generics import DestroyAPIView

class ArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
```

**URL:**

```python
path('articles/<int:pk>/delete/', ArticleDeleteView.as_view())
```

**Request:**

```bash
DELETE /articles/5/delete/
```

**Response:**

```
Status: 204 No Content
(Empty response body)
```

**Soft Delete:**

```python
class ArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_destroy(self, instance):
        # Hard delete এর পরিবর্তে soft delete
        instance.is_deleted = True
        instance.save()
```

### 6. ListCreateAPIView ⭐ (সবচেয়ে Important!)

**কাজ:** List দেখা এবং নতুন object তৈরি করা।

**HTTP Methods:** GET, POST

**কখন ব্যবহার করবেন:** সবচেয়ে common use case! একটি endpoint এ list এবং create উভয়ই।

**Basic উদাহরণ:**

```python
from rest_framework.generics import ListCreateAPIView

class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**URL:**

```python
path('articles/', ArticleListCreateView.as_view())
```

**GET Request:**

```bash
GET /articles/
```

**Response:**

```json
[
    {"id": 1, "title": "Article 1"},
    {"id": 2, "title": "Article 2"}
]
```

**POST Request:**

```bash
POST /articles/
{
    "title": "New Article",
    "content": "Content here"
}
```

**Response:**

```json
{
    "id": 3,
    "title": "New Article",
    "content": "Content here",
    "created_at": "2026-01-12T10:00:00Z"
}
```

**Advanced উদাহরণ:**

```python
class ArticleListCreateView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        # GET request এ শুধু published articles
        return Article.objects.filter(is_published=True)
    
    def get_permissions(self):
        # GET এ সবাই access করতে পারবে
        if self.request.method == 'GET':
            return [AllowAny()]
        # POST এ শুধু authenticated users
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        # Author automatically set
        serializer.save(author=self.request.user)
```

### 7. RetrieveUpdateAPIView

**কাজ:** Object দেখা এবং update করা।

**HTTP Methods:** GET, PUT, PATCH

**কখন ব্যবহার করবেন:** Profile edit page এর মতো যেখানে view এবং edit উভয়ই।

**Basic উদাহরণ:**

```python
from rest_framework.generics import RetrieveUpdateAPIView

class ArticleRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**URL:**

```python
path('articles/<int:pk>/', ArticleRetrieveUpdateView.as_view())
```

**GET Request:**

```bash
GET /articles/5/
```

**PUT/PATCH Request:**

```bash
PATCH /articles/5/
{
    "title": "Updated Title"
}
```

### 8. RetrieveDestroyAPIView

**কাজ:** Object দেখা এবং delete করা।

**HTTP Methods:** GET, DELETE

**কখন ব্যবহার করবেন:** কম ব্যবহৃত হয়। যখন view এবং delete একসাথে চান কিন্তু edit না।

**Basic উদাহরণ:**

```python
from rest_framework.generics import RetrieveDestroyAPIView

class ArticleRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
```

### 9. RetrieveUpdateDestroyAPIView ⭐ (Detail Endpoint এর জন্য!)

**কাজ:** Object দেখা, update করা এবং delete করা - সব operations!

**HTTP Methods:** GET, PUT, PATCH, DELETE

**কখন ব্যবহার করবেন:** Detail endpoint এর জন্য সবচেয়ে common! একটি URL এ সব operations।

**Basic উদাহরণ:**

```python
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
```

**URL:**

```python
path('articles/<int:pk>/', ArticleDetailView.as_view())
```

**সব Operations:**

```bash
# View
GET /articles/5/

# Full Update
PUT /articles/5/
{"title": "New Title", "content": "New Content"}

# Partial Update
PATCH /articles/5/
{"title": "Only Title Changed"}

# Delete
DELETE /articles/5/
```

**Advanced উদাহরণ:**

```python
class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        # GET এ সবাই
        if self.request.method == 'GET':
            return [AllowAny()]
        # PUT, PATCH, DELETE এ শুধু author
        return [IsAuthenticated(), IsAuthor()]
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()
```

---

## Customization Methods

Generic Views এ কিছু methods আছে যেগুলো override করে আপনি custom behavior যোগ করতে পারেন।

### 1. get_queryset(self)

**কাজ:** Dynamic queryset return করা।

**কখন ব্যবহার করবেন:**
- User-specific data filter করতে
- Query parameters দিয়ে filter করতে
- Performance optimization করতে

**উদাহরণ:**

```python
class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        # Current user এর articles
        user = self.request.user
        
        if user.is_staff:
            # Staff সব articles দেখতে পারবে
            return Article.objects.all()
        else:
            # Normal users শুধু তাদের নিজের
            return Article.objects.filter(author=user)
```

**Query Parameters দিয়ে:**

```python
def get_queryset(self):
    queryset = Article.objects.all()
    
    # URL: /articles/?category=tech&status=published
    category = self.request.query_params.get('category')
    status = self.request.query_params.get('status')
    
    if category:
        queryset = queryset.filter(category=category)
    
    if status:
        queryset = queryset.filter(status=status)
    
    return queryset
```

**Performance Optimization:**

```python
def get_queryset(self):
    return Article.objects.select_related('author', 'category').prefetch_related('tags')
```

### 2. get_serializer_class(self)

**কাজ:** Dynamic serializer return করা।

**কখন ব্যবহার করবেন:**
- বিভিন্ন actions এর জন্য বিভিন্ন serializers
- List এ light serializer, detail এ full serializer

**উদাহরণ:**

```python
class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            # List এর জন্য light serializer
            return ArticleListSerializer
        else:
            # Create এর জন্য detailed serializer
            return ArticleCreateSerializer
```

### 3. get_object(self)

**কাজ:** Single object retrieve করা।

**কখন ব্যবহার করবেন:**
- Custom lookup logic
- Additional checks

**উদাহরণ:**

```python
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_object(self):
        obj = super().get_object()
        
        # View count increment
        obj.views += 1
        obj.save()
        
        return obj
```

### 4. perform_create(self, serializer)

**কাজ:** Object create করার সময় custom logic।

**কখন ব্যবহার করবেন:**
- Automatically fields set করতে (author, created_by ইত্যাদি)
- Additional processing

**উদাহরণ:**

```python
class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_create(self, serializer):
        # Author automatically set
        serializer.save(
            author=self.request.user,
            created_by=self.request.user
        )
```

**Multiple operations:**

```python
def perform_create(self, serializer):
    # Save করা
    article = serializer.save(author=self.request.user)
    
    # Email notification পাঠানো
    send_notification_email(article)
    
    # Log করা
    logger.info(f"Article created: {article.title}")
```

### 5. perform_update(self, serializer)

**কাজ:** Object update করার সময় custom logic।

**উদাহরণ:**

```python
class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_update(self, serializer):
        # Updated_by এবং updated_at set করা
        serializer.save(
            updated_by=self.request.user,
            updated_at=timezone.now()
        )
```

### 6. perform_destroy(self, instance)

**কাজ:** Object delete করার সময় custom logic।

**উদাহরণ:**

```python
class ArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        
        # অথবা hard delete
        # instance.delete()
```

### 7. get_permissions(self)

**কাজ:** Dynamic permissions।

**উদাহরণ:**

```python
class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            # List দেখতে সবাই পারবে
            return [AllowAny()]
        else:
            # Create করতে authenticated users
            return [IsAuthenticated()]
```

---

## Best Practices

### 1. সঠিক Generic View নির্বাচন করুন

```python
# Good - ListCreateAPIView ব্যবহার
class ArticleListView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Bad - APIView দিয়ে সব manually করা
class ArticleListView(APIView):
    def get(self, request):
        # ... অনেক code
    def post(self, request):
        # ... অনেক code
```

### 2. queryset Optimize করুন

```python
# Good - select_related এবং prefetch_related
class ArticleListView(ListAPIView):
    queryset = Article.objects.select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer

# Bad - N+1 query problem
class ArticleListView(ListAPIView):
    queryset = Article.objects.all()  # প্রতিটি article এর জন্য আলাদা query
    serializer_class = ArticleSerializer
```

### 3. get_queryset() ব্যবহার করুন Dynamic Filtering এর জন্য

```python
# Good
class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        return Article.objects.filter(is_published=True)

# Bad - queryset static
class ArticleListView(ListAPIView):
    queryset = Article.objects.all()  # সবাই সব দেখতে পারবে
    serializer_class = ArticleSerializer
```

### 4. perform_create/update ব্যবহার করুন

```python
# Good
class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Bad - serializer এ manually করা
class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # serializer এ author field required করা এবং manually pass করা
```

### 5. Permissions সঠিকভাবে Set করুন

```python
# Good - Method-based permissions
class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

# Bad - সব methods এর জন্য একই permission
class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]  # GET এও login লাগবে
```

### 6. Pagination Enable করুন

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# অথবা per-view
class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination
```

### 7. Filtering এবং Searching যোগ করুন

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']

# URL: /articles/?category=tech&search=django
```

### 8. Proper HTTP Status Codes ব্যবহার করুন

Generic Views automatically সঠিক status codes ব্যবহার করে:
- GET: 200 OK
- POST: 201 Created
- PUT/PATCH: 200 OK
- DELETE: 204 No Content
- Not Found: 404
- Validation Error: 400 Bad Request

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

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'is_published']

# views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ArticleListCreateView(ListCreateAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    
    def get_queryset(self):
        queryset = Article.objects.select_related('author', 'category')
        
        # Non-staff users শুধু published articles দেখবে
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleCreateSerializer
        return ArticleListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.select_related('author', 'category')
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleDetailSerializer
        return ArticleCreateSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAuthor()]
    
    def get_object(self):
        obj = super().get_object()
        # View count increment (শুধু GET request এ)
        if self.request.method == 'GET':
            obj.views += 1
            obj.save(update_fields=['views'])
        return obj
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_published = False
        instance.save()

# urls.py
urlpatterns = [
    path('articles/', ArticleListCreateView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]
```

### উদাহরণ 2: E-commerce Product API

```python
# views.py
class ProductListView(ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]

class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]

class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()

# urls.py
urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/create/', ProductCreateView.as_view()),
    path('products/<slug:slug>/', ProductDetailView.as_view()),
    path('products/<int:pk>/update/', ProductUpdateView.as_view()),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view()),
]
```

### উদাহরণ 3: User Profile API

```python
# views.py
class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Current user এর profile
        return self.request.user

# urls.py
path('profile/', UserProfileView.as_view(), name='user-profile')
```

### উদাহরণ 4: Comment System

```python
# views.py
class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Specific article এর comments
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article_id=article_id).select_related('author')
    
    def perform_create(self, serializer):
        article_id = self.kwargs['article_id']
        serializer.save(
            author=self.request.user,
            article_id=article_id
        )

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

# urls.py
urlpatterns = [
    path('articles/<int:article_id>/comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),
]
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Generic Views: https://www.django-rest-framework.org/api-guide/generic-views/
- Classy Django REST Framework: http://www.cdrf.co (Interactive reference)

### সম্পর্কিত বিষয়
- Serializers
- Permissions
- Authentication
- Filtering এবং Searching
- Pagination

### পরবর্তী শেখার বিষয়:
- ViewSets (আরও powerful এবং less code)
- Routers (Automatic URL generation)
- Custom Actions

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
