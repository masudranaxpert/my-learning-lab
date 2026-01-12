# Django REST Framework - Serializers

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Serializer কী এবং কেন?](#serializer-কী-এবং-কেন)
3. [Serializer Types](#serializer-types)
4. [ModelSerializer - সবচেয়ে Important!](#modelserializer---সবচেয়ে-important)
5. [Serializer Fields](#serializer-fields)
6. [Serialization এবং Deserialization](#serialization-এবং-deserialization)
7. [Validation](#validation)
8. [Nested Serializers](#nested-serializers)
9. [SerializerMethodField](#serializermethodfield)
10. [read_only এবং write_only Fields](#read_only-এবং-write_only-fields)
11. [Custom Serializers](#custom-serializers)
12. [Best Practices](#best-practices)
13. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)
14. [Performance Optimization](#performance-optimization)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **পরিচিতি** - Serializer কী এবং কেন প্রয়োজন
2. ⭐⭐⭐ **ModelSerializer** - সবচেয়ে বেশি ব্যবহৃত
3. ⭐⭐⭐ **Serialization এবং Deserialization** - কীভাবে কাজ করে
4. ⭐⭐⭐ **Validation** - Data validate করা
5. ⭐⭐⭐ **Serializer Fields** - কোন fields কী করে

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **read_only এবং write_only Fields**
7. ⭐⭐ **Nested Serializers** - Related data handle করা
8. ⭐⭐ **SerializerMethodField** - Custom fields
9. ⭐⭐ **Best Practices** - Professional code
10. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ**

### শেষে পড়ুন (Advanced):

11. ⭐ **Custom Serializers** - নিজের serializer তৈরি করা
12. ⭐ **Performance Optimization** - N+1 problem solve করা

### দ্রষ্টব্য:
- ⭐⭐⭐ = অবশ্যই পড়তে হবে
- ⭐⭐ = গুরুত্বপূর্ণ
- ⭐ = Advanced topics

---

## পরিচিতি

Django REST Framework এ API তৈরি করার সময় আপনাকে দুটি main কাজ করতে হয়:

1. **Database থেকে Python objects নেওয়া** → **JSON এ convert করা** (Response পাঠানোর জন্য)
2. **Client থেকে JSON নেওয়া** → **Python objects এ convert করা** → **Database এ save করা**

এই দুটি কাজ করে **Serializers**!

### সহজ উদাহরণ:

```python
# Database এ Article model আছে
article = Article.objects.get(id=1)
# article = <Article: My First Article>

# Serializer দিয়ে JSON এ convert
serializer = ArticleSerializer(article)
print(serializer.data)
# Output: {'id': 1, 'title': 'My First Article', 'content': '...'}

# JSON response পাঠানো
return Response(serializer.data)
```

---

## Serializer কী এবং কেন?

### Serializer কী?

**সহজ ভাষায়:** Serializer হলো একটি translator যা:
- Python objects কে JSON এ convert করে (Serialization)
- JSON কে Python objects এ convert করে (Deserialization)
- Data validate করে

**Technical:** Serializer হলো একটি class যা complex data types (Django models, QuerySets) কে native Python datatypes এ convert করে, যা পরে JSON, XML ইত্যাদিতে render করা যায়।

### কেন Serializer প্রয়োজন?

**সমস্যা:** Django models সরাসরি JSON এ convert করা যায় না।

```python
# এটা কাজ করবে না!
article = Article.objects.get(id=1)
return JsonResponse(article)  # Error!
```

**সমাধান:** Serializer ব্যবহার করুন।

```python
# এটা কাজ করবে!
article = Article.objects.get(id=1)
serializer = ArticleSerializer(article)
return Response(serializer.data)  # Success!
```

### Serializer এর কাজ:

| কাজ | বর্ণনা | উদাহরণ |
|-----|--------|---------|
| **Serialization** | Python → JSON | Model instance → JSON response |
| **Deserialization** | JSON → Python | JSON request → Model instance |
| **Validation** | Data check করা | Email valid কিনা, required fields আছে কিনা |
| **Saving** | Database এ save | Validated data → Database |

---

## Serializer Types

Django REST Framework তিন ধরনের serializers প্রদান করে:

### 1. Serializer (Base Class)

**কখন ব্যবহার করবেন:** যখন Django model নেই, custom data structure আছে।

**উদাহরণ:**

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

### 2. ModelSerializer ⭐⭐⭐ (সবচেয়ে Important!)

**কখন ব্যবহার করবেন:** যখন Django model আছে (90%+ cases)।

**উদাহরণ:**

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']
```

### 3. HyperlinkedModelSerializer

**কখন ব্যবহার করবেন:** যখন relationships URLs দিয়ে represent করতে চান।

**উদাহরণ:**

```python
class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['url', 'title', 'content']
```

### তুলনা:

| Feature | Serializer | ModelSerializer | HyperlinkedModelSerializer |
|---------|-----------|-----------------|----------------------------|
| Model Required | ❌ | ✅ | ✅ |
| Auto Fields | ❌ | ✅ | ✅ |
| Auto Validation | ❌ | ✅ | ✅ |
| Relationships | Manual | IDs | URLs |
| Use Cases | Custom data | 90% cases | RESTful APIs |

---

## ModelSerializer - সবচেয়ে Important!

`ModelSerializer` হলো সবচেয়ে commonly used serializer কারণ এটি:
- Automatically fields generate করে model থেকে
- Automatically validators তৈরি করে
- Built-in `.create()` এবং `.update()` methods আছে

### Basic Structure:

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article  # কোন model
        fields = ['id', 'title', 'content', 'created_at']  # কোন fields
```

### কী হয় Internally:

যখন আপনি এই serializer define করেন, DRF automatically:

1. **Fields তৈরি করে:**
   - `id` → `IntegerField(read_only=True)`
   - `title` → `CharField(max_length=200)`
   - `content` → `TextField()`
   - `created_at` → `DateTimeField(read_only=True)`

2. **Validators যোগ করে:**
   - `unique=True` থাকলে `UniqueValidator`
   - `unique_together` থাকলে `UniqueTogetherValidator`

3. **Methods তৈরি করে:**
   - `.create()` - নতুন object তৈরি করে
   - `.update()` - existing object update করে

### Fields Specify করার উপায়:

#### 1. Specific Fields:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content']  # শুধু এই fields
```

#### 2. All Fields:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'  # সব fields
```

**⚠️ Warning:** Production এ `'__all__'` ব্যবহার করবেন না! Security risk!

#### 3. Exclude Fields:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ['password', 'secret_key']  # এই fields বাদে সব
```

### Inspecting a ModelSerializer:

কোন fields automatically তৈরি হয়েছে দেখতে:

```python
# Django shell এ
python manage.py shell

>>> from myapp.serializers import ArticleSerializer
>>> serializer = ArticleSerializer()
>>> print(repr(serializer))

# Output:
ArticleSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=200)
    content = TextField()
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
    created_at = DateTimeField(read_only=True)
```

---

## Serializer Fields

Serializer fields হলো individual data pieces যা serialize/deserialize করা হয়।

### Common Fields:

| Field Type | Django Model Field | কী Data Accept করে |
|-----------|-------------------|-------------------|
| `CharField` | `CharField`, `TextField` | String |
| `IntegerField` | `IntegerField` | Integer |
| `FloatField` | `FloatField` | Float |
| `DecimalField` | `DecimalField` | Decimal |
| `BooleanField` | `BooleanField` | True/False |
| `DateTimeField` | `DateTimeField` | DateTime |
| `DateField` | `DateField` | Date |
| `EmailField` | `EmailField` | Email |
| `URLField` | `URLField` | URL |
| `FileField` | `FileField` | File |
| `ImageField` | `ImageField` | Image |

### Field Arguments:

```python
class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=200,      # Maximum length
        min_length=5,        # Minimum length
        required=True,       # Required field
        allow_blank=False,   # Empty string allowed?
        allow_null=False,    # NULL allowed?
        default='Untitled',  # Default value
        help_text='Article title',  # Help text
        error_messages={     # Custom error messages
            'required': 'Title is required',
            'max_length': 'Title too long'
        }
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title']
```

### Relational Fields:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # ForeignKey - শুধু ID
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    # ForeignKey - String representation
    author = serializers.StringRelatedField()
    
    # ForeignKey - Nested serializer
    author = UserSerializer()
    
    # ForeignKey - Hyperlink
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']
```

---

## Serialization এবং Deserialization

**কী এবং কেন?**

Serialization এবং Deserialization হলো serializer এর দুটি main কাজ:
- **Serialization:** Python objects → JSON (Response পাঠানোর জন্য)
- **Deserialization:** JSON → Python objects (Request থেকে data নেওয়ার জন্য)

### Serialization (Python → JSON)

**কাজ:** Database থেকে data নিয়ে JSON এ convert করা।

**কখন ব্যবহার হয়:**
- GET requests (list, retrieve)
- Response পাঠানোর সময়
- Database data কে API response এ convert করার সময়

#### Single Object Serialization:

```python
# Model instance
article = Article.objects.get(id=1)
# article = <Article: My First Article>

# Serialize
serializer = ArticleSerializer(article)

# JSON data
print(serializer.data)
# Output: {'id': 1, 'title': 'My Article', 'content': '...'}

# Response পাঠানো
return Response(serializer.data)
```

**কখন কী হচ্ছে - Step by Step:**

```
1. Database Query
   Article.objects.get(id=1)
   → Database থেকে Article object আসলো
   
2. Serializer Initialize
   ArticleSerializer(article)
   → Serializer article object নিলো
   
3. Serialization Process (Internally):
   a. Serializer article এর fields check করলো
   b. প্রতিটি field এর value নিলো:
      - article.id → 1
      - article.title → "My Article"
      - article.content → "Content here..."
   c. Python dict তৈরি করলো
   
4. .data Property Access
   serializer.data
   → Python dict return করলো
   → DRF internally JSON-compatible format এ convert করলো
   
5. Response
   Response(serializer.data)
   → JSON response client এ পাঠালো
```

**Example with Details:**

```python
# Model
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Serializer
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at']

# View
def get_article(request, pk):
    # Step 1: Database query
    article = Article.objects.get(pk=pk)
    # article.id = 1
    # article.title = "Django REST Framework"
    # article.content = "DRF is awesome..."
    # article.author = <User: john>
    # article.created_at = datetime(2026, 1, 12, 10, 0, 0)
    
    # Step 2: Serialize
    serializer = ArticleSerializer(article)
    
    # Step 3: Get data (internally converts to dict)
    print(serializer.data)
    # {
    #     'id': 1,
    #     'title': 'Django REST Framework',
    #     'content': 'DRF is awesome...',
    #     'author': 5,  # ForeignKey → ID
    #     'created_at': '2026-01-12T10:00:00Z'  # DateTime → ISO format
    # }
    
    # Step 4: Return JSON response
    return Response(serializer.data)
    # Client receives JSON
```

#### Multiple Objects Serialization:

```python
# QuerySet
articles = Article.objects.all()
# [<Article: Article 1>, <Article: Article 2>, ...]

# Serialize (many=True দিতে হবে!)
serializer = ArticleSerializer(articles, many=True)

# JSON data
print(serializer.data)
# Output: [{'id': 1, ...}, {'id': 2, ...}, ...]

return Response(serializer.data)
```

**কেন many=True লাগে?**

```python
# Without many=True (Wrong!)
articles = Article.objects.all()
serializer = ArticleSerializer(articles)
# Error! Serializer expects single object, got QuerySet

# With many=True (Correct!)
serializer = ArticleSerializer(articles, many=True)
# Works! Serializer knows it's a list
```

**কখন কী হচ্ছে:**

```
1. Database Query
   Article.objects.all()
   → QuerySet [Article1, Article2, Article3]
   
2. Serializer Initialize (many=True)
   ArticleSerializer(articles, many=True)
   → Serializer বুঝলো: এটা list
   
3. Serialization Process:
   For each article in articles:
     a. Article1 serialize → dict1
     b. Article2 serialize → dict2
     c. Article3 serialize → dict3
   
4. Combine Results
   [dict1, dict2, dict3]
   
5. Return
   Response([dict1, dict2, dict3])
```

---

### Deserialization (JSON → Python)

**কাজ:** Client থেকে JSON নিয়ে Python object এ convert করা এবং validate করা।

**কখন ব্যবহার হয়:**
- POST requests (create)
- PUT/PATCH requests (update)
- Client থেকে data receive করার সময়

#### Creating New Object:

```python
# Client থেকে JSON data
data = {
    'title': 'New Article',
    'content': 'Article content here',
    'author': 1
}

# Deserialize
serializer = ArticleSerializer(data=data)

# Validate
if serializer.is_valid():
    # Save to database
    article = serializer.save()
    return Response(serializer.data, status=201)
else:
    # Validation errors
    return Response(serializer.errors, status=400)
```

**কখন কী হচ্ছে - Step by Step:**

```
1. Client Request
   POST /api/articles/
   Body: {"title": "New Article", "content": "Content", "author": 1}
   → JSON data আসলো
   
2. Serializer Initialize (data=...)
   ArticleSerializer(data=data)
   → Serializer data নিলো
   → এখনো validate হয়নি!
   
3. Validation (.is_valid())
   serializer.is_valid()
   
   a. Field-level validation:
      - title: CharField → check max_length, required
      - content: TextField → check required
      - author: ForeignKey → check exists in database
   
   b. Object-level validation:
      - validate() method call হয় (যদি থাকে)
   
   c. Custom validators:
      - validate_<field>() methods call হয়
   
   d. Result:
      - All valid → return True
      - Any invalid → return False, set errors
   
4. Save (.save())
   serializer.save()
   
   a. validated_data থেকে data নেয়
   b. create() method call করে
   c. Article.objects.create(**validated_data)
   d. Database এ save হয়
   e. Created object return করে
   
5. Response
   Response(serializer.data, status=201)
   → Created object JSON এ convert হয়ে client এ যায়
```

**Detailed Example:**

```python
# View
def create_article(request):
    # Step 1: Get data from request
    data = request.data
    # data = {
    #     'title': 'New Article',
    #     'content': 'Content here',
    #     'author': 1
    # }
    
    # Step 2: Initialize serializer
    serializer = ArticleSerializer(data=data)
    # Serializer created, but NOT validated yet
    
    # Step 3: Validate
    if serializer.is_valid():
        # Validation passed!
        # serializer.validated_data = {
        #     'title': 'New Article',
        #     'content': 'Content here',
        #     'author': <User: john>  # ForeignKey resolved
        # }
        
        # Step 4: Save to database
        article = serializer.save()
        # Internally calls:
        # Article.objects.create(
        #     title='New Article',
        #     content='Content here',
        #     author=<User: john>
        # )
        # Returns: <Article: New Article>
        
        # Step 5: Return response
        return Response(serializer.data, status=201)
        # serializer.data = {
        #     'id': 11,  # Auto-generated
        #     'title': 'New Article',
        #     'content': 'Content here',
        #     'author': 1,
        #     'created_at': '2026-01-12T10:30:00Z'  # Auto-generated
        # }
    else:
        # Validation failed!
        return Response(serializer.errors, status=400)
        # serializer.errors = {
        #     'title': ['This field is required.'],
        #     'content': ['Ensure this field has at least 100 characters.']
        # }
```

#### Updating Existing Object:

```python
# Existing object
article = Article.objects.get(id=1)

# Updated data
data = {
    'title': 'Updated Title',
    'content': 'Updated content'
}

# Deserialize with instance
serializer = ArticleSerializer(article, data=data)

# Validate and update
if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
else:
    return Response(serializer.errors, status=400)
```

**কখন কী হচ্ছে:**

```
1. Get Existing Object
   article = Article.objects.get(id=1)
   → Database থেকে existing article
   
2. Serializer Initialize (instance + data)
   ArticleSerializer(article, data=data)
   → Serializer বুঝলো: এটা update
   → instance = article (existing)
   → data = new data
   
3. Validation
   serializer.is_valid()
   → Same validation process
   
4. Save (Update)
   serializer.save()
   
   a. validated_data থেকে data নেয়
   b. update() method call করে
   c. Existing article update করে:
      article.title = 'Updated Title'
      article.content = 'Updated content'
      article.save()
   d. Updated object return করে
   
5. Response
   Response(serializer.data)
   → Updated data JSON এ
```

#### Partial Update (PATCH):

```python
# শুধু title update করতে চাই
data = {'title': 'New Title'}

serializer = ArticleSerializer(article, data=data, partial=True)

if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
```

**partial=True কেন লাগে?**

```python
# Without partial=True (PUT behavior)
data = {'title': 'New Title'}  # শুধু title
serializer = ArticleSerializer(article, data=data)
serializer.is_valid()
# Error! 'content' field is required
# PUT expects ALL fields

# With partial=True (PATCH behavior)
data = {'title': 'New Title'}  # শুধু title
serializer = ArticleSerializer(article, data=data, partial=True)
serializer.is_valid()
# Success! Only 'title' will be updated
# Other fields remain unchanged
```

**কখন কী হচ্ছে:**

```
1. Partial Update Request
   data = {'title': 'New Title'}
   → শুধু title update করবো
   
2. Serializer (partial=True)
   ArticleSerializer(article, data=data, partial=True)
   → Serializer বুঝলো: partial update
   
3. Validation (Partial)
   serializer.is_valid()
   → শুধু provided fields validate করবে
   → Missing fields ignore করবে
   
4. Save (Partial Update)
   serializer.save()
   → শুধু title update হবে
   → content, author ইত্যাদি unchanged থাকবে
```

### Serialization vs Deserialization - Quick Comparison:

| Feature | Serialization | Deserialization |
|---------|--------------|-----------------|
| Direction | Python → JSON | JSON → Python |
| কখন | Response পাঠানোর সময় | Request receive করার সময় |
| Input | Model instance/QuerySet | JSON data (dict) |
| Output | JSON-compatible dict | Model instance |
| Validation | ❌ Not needed | ✅ Required |
| Methods | `.data` | `.is_valid()`, `.save()` |
| Example | `GET /articles/` | `POST /articles/` |

### Common Patterns:

```python
# Pattern 1: List (Serialization)
def list_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)  # 200 OK

# Pattern 2: Retrieve (Serialization)
def get_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)  # 200 OK

# Pattern 3: Create (Deserialization)
def create_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)  # 201 Created
    return Response(serializer.errors, status=400)  # 400 Bad Request

# Pattern 4: Update (Deserialization)
def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)  # 200 OK
    return Response(serializer.errors, status=400)  # 400 Bad Request

# Pattern 5: Partial Update (Deserialization)
def partial_update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)  # 200 OK
    return Response(serializer.errors, status=400)  # 400 Bad Request
```

---

## Validation

Validation হলো incoming data check করা যে সেটা valid কিনা।

### Validation Levels:

DRF তিন level এ validation করে:

1. **Field-level validation** - Individual fields
2. **Object-level validation** - Multiple fields together
3. **Validator classes** - Reusable validators

### 1. Field-Level Validation:

**Method:** `validate_<field_name>(self, value)`

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content']
    
    def validate_title(self, value):
        """
        Title অবশ্যই 'Django' শব্দ থাকতে হবে
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError(
                "Title must contain 'Django'"
            )
        return value
    
    def validate_content(self, value):
        """
        Content minimum 100 characters
        """
        if len(value) < 100:
            raise serializers.ValidationError(
                "Content must be at least 100 characters"
            )
        return value
```

**ব্যবহার:**

```python
data = {'title': 'My Article', 'content': 'Short'}
serializer = ArticleSerializer(data=data)

if serializer.is_valid():
    serializer.save()
else:
    print(serializer.errors)
    # Output: {
    #     'title': ['Title must contain Django'],
    #     'content': ['Content must be at least 100 characters']
    # }
```

### 2. Object-Level Validation:

**Method:** `validate(self, data)`

যখন multiple fields একসাথে check করতে হয়:

```python
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'start_date', 'end_date']
    
    def validate(self, data):
        """
        end_date অবশ্যই start_date এর পরে হতে হবে
        """
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                "End date must be after start date"
            )
        return data
```

### 3. Validator Classes:

Reusable validators তৈরি করা:

```python
from rest_framework import serializers

def validate_even_number(value):
    """
    Value অবশ্যই even number হতে হবে
    """
    if value % 2 != 0:
        raise serializers.ValidationError(
            f'{value} is not an even number'
        )

class MySerializer(serializers.Serializer):
    number = serializers.IntegerField(
        validators=[validate_even_number]
    )
```

### Built-in Validators:

```python
from rest_framework.validators import UniqueValidator

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Article.objects.all(),
                message='Article with this title already exists'
            )
        ]
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title']
```

### Validation Flow:

```
1. Field-level validation (validate_<field_name>)
   ↓
2. Validators on fields
   ↓
3. Object-level validation (validate)
   ↓
4. Model validation (if saving)
```

---

## Nested Serializers

Nested serializers ব্যবহার করা হয় related objects represent করতে।

### Problem:

```python
# Model
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# Simple serializer
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']

# Output:
# {'id': 1, 'title': 'My Article', 'author': 5}  # শুধু ID!
```

### Solution: Nested Serializer

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Nested!
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']

# Output:
# {
#     'id': 1,
#     'title': 'My Article',
#     'author': {
#         'id': 5,
#         'username': 'john',
#         'email': 'john@example.com'
#     }
# }
```

### Read-Only Nested Serializers:

```python
class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # শুধু read করতে পারবে
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']
```

### Writable Nested Serializers:

```python
class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']
    
    def create(self, validated_data):
        # Author data আলাদা করা
        author_data = validated_data.pop('author')
        
        # Author তৈরি করা
        author = User.objects.create(**author_data)
        
        # Article তৈরি করা
        article = Article.objects.create(author=author, **validated_data)
        
        return article
```

### Many-to-Many Relationships:

```python
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)  # many=True!
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'tags']

# Output:
# {
#     'id': 1,
#     'title': 'My Article',
#     'tags': [
#         {'id': 1, 'name': 'Django'},
#         {'id': 2, 'name': 'Python'}
#     ]
# }
```

---

## SerializerMethodField

`SerializerMethodField` ব্যবহার করা হয় custom computed fields এর জন্য যা model এ নেই।

### Basic Usage:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # Custom field
    word_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'word_count']
    
    def get_word_count(self, obj):
        """
        Method name: get_<field_name>
        """
        return len(obj.content.split())

# Output:
# {
#     'id': 1,
#     'title': 'My Article',
#     'content': 'This is my article content...',
#     'word_count': 150
# }
```

### Common Use Cases:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # Full name from first_name + last_name
    author_full_name = serializers.SerializerMethodField()
    
    # Count related objects
    comment_count = serializers.SerializerMethodField()
    
    # Custom URL
    absolute_url = serializers.SerializerMethodField()
    
    # Conditional field
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title',
            'author_full_name',
            'comment_count',
            'absolute_url',
            'is_owner'
        ]
    
    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_absolute_url(self, obj):
        return f"/articles/{obj.slug}/"
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.author == request.user
        return False
```

### Accessing Request in SerializerMethodField:

```python
# View এ
serializer = ArticleSerializer(article, context={'request': request})

# Serializer এ
def get_is_owner(self, obj):
    request = self.context.get('request')
    return obj.author == request.user
```

---

## ReadOnlyField

`ReadOnlyField` হলো একটি special field যা model এর attributes বা properties কে read-only হিসেবে serialize করে।

### কী এবং কেন?

**সহজ ভাষায়:** `ReadOnlyField` model এর যেকোনো attribute/property কে response এ include করে কিন্তু create/update এ ignore করে।

**পার্থক্য SerializerMethodField থেকে:**

| Feature | ReadOnlyField | SerializerMethodField |
|---------|--------------|----------------------|
| কাজ | Model attribute/property access | Custom method call করে |
| Method লাগবে? | ❌ | ✅ (get_<field_name>) |
| Performance | দ্রুত | একটু slow (method call) |
| Use Case | Simple attributes | Complex calculations |

### Basic Usage:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def author_name(self):
        return self.author.username

class ArticleSerializer(serializers.ModelSerializer):
    # ReadOnlyField - model property access
    author_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'author_name', 'created_at']

# Output:
# {
#     'id': 1,
#     'title': 'My Article',
#     'author': 5,
#     'author_name': 'john',  # From property
#     'created_at': '2026-01-12T10:00:00Z'
# }
```

### source Parameter:

`source` parameter দিয়ে specify করা যায় কোন attribute access করবে:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # Direct attribute access
    author_username = serializers.ReadOnlyField(source='author.username')
    author_email = serializers.ReadOnlyField(source='author.email')
    
    # Property access
    full_title = serializers.ReadOnlyField(source='get_full_title')
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author_username', 'author_email', 'full_title']

# Model:
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_full_title(self):
        return f"{self.title} by {self.author.username}"
```

### Common Use Cases:

#### 1. Model Properties:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    @property
    def word_count(self):
        return len(self.content.split())
    
    @property
    def read_time(self):
        return self.word_count // 200  # 200 words per minute

class ArticleSerializer(serializers.ModelSerializer):
    word_count = serializers.ReadOnlyField()
    read_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'word_count', 'read_time']
```

#### 2. Related Object Attributes:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # Author details
    author_name = serializers.ReadOnlyField(source='author.username')
    author_email = serializers.ReadOnlyField(source='author.email')
    
    # Category details
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Article
        fields = [
            'id', 'title',
            'author_name', 'author_email',
            'category_name'
        ]
```

#### 3. Method Results:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    
    def get_absolute_url(self):
        return f"/articles/{self.id}/"
    
    def is_recent(self):
        from datetime import timedelta
        from django.utils import timezone
        return self.created_at > timezone.now() - timedelta(days=7)

class ArticleSerializer(serializers.ModelSerializer):
    absolute_url = serializers.ReadOnlyField(source='get_absolute_url')
    is_recent = serializers.ReadOnlyField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'absolute_url', 'is_recent']
```

#### 4. Computed Values:

```python
class Order(models.Model):
    items = models.ManyToManyField(OrderItem)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
    @property
    def total(self):
        return self.subtotal - self.discount

class OrderSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields = ['id', 'items', 'discount', 'subtotal', 'total']
```

### ReadOnlyField vs SerializerMethodField:

**কখন ReadOnlyField:**
```python
# Simple attribute/property access
class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    # Fast, simple
```

**কখন SerializerMethodField:**
```python
# Complex logic, multiple operations
class ArticleSerializer(serializers.ModelSerializer):
    author_info = serializers.SerializerMethodField()
    
    def get_author_info(self, obj):
        # Complex logic
        return {
            'name': obj.author.username,
            'email': obj.author.email,
            'is_premium': obj.author.is_premium,
            'post_count': obj.author.articles.count()
        }
```

### Performance Comparison:

```python
# ReadOnlyField - Direct access (faster)
author_name = serializers.ReadOnlyField(source='author.username')

# SerializerMethodField - Method call (slower)
author_name = serializers.SerializerMethodField()

def get_author_name(self, obj):
    return obj.author.username

# Recommendation: Use ReadOnlyField for simple cases
```

### Default Value:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # Default value if attribute is None
    author_name = serializers.ReadOnlyField(
        source='author.username',
        default='Anonymous'
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author_name']
```

### Nested Access:

```python
class ArticleSerializer(serializers.ModelSerializer):
    # Deep nesting
    author_profile_bio = serializers.ReadOnlyField(source='author.profile.bio')
    author_country = serializers.ReadOnlyField(source='author.profile.country.name')
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author_profile_bio', 'author_country']
```

---

## read_only এবং write_only Fields

### read_only Fields:

**কাজ:** শুধু response এ থাকবে, create/update এ ignore হবে।

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# অথবা individual field এ
class ArticleSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at']
```

### write_only Fields:

**কাজ:** শুধু create/update এ থাকবে, response এ থাকবে না।

```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Request:
# {'username': 'john', 'email': 'john@example.com', 'password': 'secret123'}

# Response:
# {'id': 1, 'username': 'john', 'email': 'john@example.com'}
# password নেই!
```

### extra_kwargs:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'content': {'write_only': True, 'required': False}
        }
```

---

## Custom Serializers

যখন `ModelSerializer` যথেষ্ট নয়, তখন custom serializer তৈরি করুন।

### Basic Serializer:

```python
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
```

### Dynamic Fields:

```python
class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    URL এ fields specify করে শুধু সেগুলো return করা
    Example: /articles/?fields=id,title
    """
    
    def __init__(self, *args, **kwargs):
        # Get fields from request
        fields = self.context['request'].query_params.get('fields')
        
        super().__init__(*args, **kwargs)
        
        if fields:
            fields = fields.split(',')
            # Remove fields not in the list
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ArticleSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']
```

---

## Best Practices

### 1. Explicitly Define Fields

```python
# Good - Explicit
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content']

# Bad - Security risk!
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'  # Sensitive data expose হতে পারে!
```

### 2. Separate Read and Write Serializers

```python
# Read serializer - Detailed
class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'comments']

# Write serializer - Simple
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

# View এ
def get_serializer_class(self):
    if self.action == 'retrieve':
        return ArticleDetailSerializer
    return ArticleCreateSerializer
```

### 3. Use read_only_fields

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
```

### 4. Optimize Queries

```python
# View এ queryset optimize করুন
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer
```

### 5. Keep Serializers Thin

```python
# Bad - Business logic serializer এ
class ArticleSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # অনেক business logic...
        # Email পাঠানো, notifications, ইত্যাদি
        pass

# Good - Business logic আলাদা
class ArticleSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Article.objects.create(**validated_data)

# Service layer এ business logic
def create_article(data, user):
    article = Article.objects.create(**data, author=user)
    send_notification(article)
    return article
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: Blog API

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# List serializer - Light
class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug',
            'author_name', 'category_name',
            'is_published', 'views',
            'created_at'
        ]

# Detail serializer - Detailed
class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    word_count = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content',
            'author', 'category', 'tags',
            'is_published', 'views',
            'word_count', 'read_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['views', 'created_at', 'updated_at']
    
    def get_word_count(self, obj):
        return len(obj.content.split())
    
    def get_read_time(self, obj):
        words = len(obj.content.split())
        return round(words / 200)  # 200 words per minute

# Create/Update serializer
class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'content',
            'category', 'tags', 'is_published'
        ]
    
    def validate_slug(self, value):
        # Check if slug already exists (for create)
        if self.instance is None:
            if Article.objects.filter(slug=value).exists():
                raise serializers.ValidationError(
                    "Article with this slug already exists"
                )
        return value
    
    def validate_content(self, value):
        if len(value) < 100:
            raise serializers.ValidationError(
                "Content must be at least 100 characters"
            )
        return value
```

### উদাহরণ 2: E-commerce Product

```python
# serializers.py
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'discount_price', 'stock',
            'category_name', 'images',
            'average_rating', 'is_in_stock',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_average_rating(self, obj):
        ratings = obj.reviews.aggregate(Avg('rating'))
        return ratings['rating__avg'] or 0
    
    def get_is_in_stock(self, obj):
        return obj.stock > 0
```

### উদাহরণ 3: User Registration

```python
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
```

---

## Performance Optimization

### Problem: N+1 Queries

```python
# Bad - N+1 problem!
class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username')
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author_name']

# 10 articles থাকলে:
# 1 query for articles
# 10 queries for each author
# Total: 11 queries!
```

### Solution: select_related

```python
# View এ optimize করুন
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'category')
    serializer_class = ArticleSerializer

# এখন শুধু 1 query!
```

### Many-to-Many: prefetch_related

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer
```

### SerializerMethodField Optimization:

```python
# Bad - Query in method
class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    
    def get_comment_count(self, obj):
        return obj.comments.count()  # Query প্রতিটি article এর জন্য!

# Good - Annotate in queryset
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.annotate(
        comment_count=Count('comments')
    )
    serializer_class = ArticleSerializer

class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Serializers: https://www.django-rest-framework.org/api-guide/serializers/
- Classy Django REST Framework: http://www.cdrf.co

### সম্পর্কিত বিষয়
- Validators (পরবর্তী documentation)
- Serializer Relations
- Serializer Fields

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
