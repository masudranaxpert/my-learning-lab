# Django REST Framework - Validators & Pagination

## সূচিপত্র

### Part 1: Validators
1. [Validators পরিচিতি](#validators-পরিচিতি)
2. [Validation কী এবং কেন?](#validation-কী-এবং-কেন)
3. [Validation Levels](#validation-levels)
4. [Built-in Validators](#built-in-validators)
5. [Custom Validators](#custom-validators)
6. [Validator Best Practices](#validator-best-practices)

### Part 2: Pagination
7. [Pagination পরিচিতি](#pagination-পরিচিতি)
8. [Pagination কী এবং কেন?](#pagination-কী-এবং-কেন)
9. [Pagination Types](#pagination-types)
10. [PageNumberPagination](#pagenumberpagination)
11. [LimitOffsetPagination](#limitoffsetpagination)
12. [CursorPagination](#cursorpagination)
13. [Custom Pagination](#custom-pagination)
14. [Pagination Best Practices](#pagination-best-practices)

---

## শেখার ক্রম

### Part 1: Validators

#### প্রথমে পড়ুন (অবশ্যই):
1. ⭐⭐⭐ **Validation কী এবং কেন?**
2. ⭐⭐⭐ **Validation Levels** - Field, Object, Validator
3. ⭐⭐⭐ **Custom Validators** - নিজের validator তৈরি করা

#### এরপর পড়ুন (গুরুত্বপূর্ণ):
4. ⭐⭐ **Built-in Validators**
5. ⭐⭐ **Validator Best Practices**

### Part 2: Pagination

#### প্রথমে পড়ুন (অবশ্যই):
6. ⭐⭐⭐ **Pagination কী এবং কেন?**
7. ⭐⭐⭐ **PageNumberPagination** - সবচেয়ে common
8. ⭐⭐⭐ **Pagination Setup** - কীভাবে enable করবেন

#### এরপর পড়ুন (গুরুত্বপূর্ণ):
9. ⭐⭐ **LimitOffsetPagination**
10. ⭐⭐ **CursorPagination** - Large datasets এর জন্য
11. ⭐⭐ **Pagination Best Practices**

#### শেষে পড়ুন (Advanced):
12. ⭐ **Custom Pagination**

---

# Part 1: Validators

## Validators পরিচিতি

Validators হলো reusable validation logic যা বিভিন্ন serializers এ ব্যবহার করা যায়।

**সহজ উদাহরণ:**

```python
# একই validation logic বারবার লিখতে হচ্ছে
class ArticleSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Too short")
        return value

class PostSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if len(value) < 10:  # Same logic!
            raise serializers.ValidationError("Too short")
        return value

# Validator দিয়ে - একবার লিখুন, সবখানে ব্যবহার করুন!
def validate_min_length_10(value):
    if len(value) < 10:
        raise serializers.ValidationError("Too short")

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_min_length_10])

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_min_length_10])
```

---

## Validation কী এবং কেন?

### Validation কী?

**সহজ ভাষায়:** Validation হলো data check করা যে সেটা সঠিক কিনা।

**উদাহরণ:**
- Email সঠিক format এ আছে কিনা
- Password minimum 8 characters কিনা
- Age 18+ কিনা
- Username unique কিনা

### কেন Validation প্রয়োজন?

1. **Data Integrity** - Database এ শুধু valid data যাবে
2. **Security** - Malicious data block করা
3. **User Experience** - Clear error messages
4. **Business Rules** - Business logic enforce করা

### Validation কখন হয়?

```python
serializer = ArticleSerializer(data=request.data)

# এই line এ validation হয়!
if serializer.is_valid():
    serializer.save()
else:
    # Validation errors
    print(serializer.errors)
```

---

## Validation Levels

DRF তিন level এ validation করে:

### 1. Field-Level Validation

**কাজ:** Individual fields validate করা।

**Method:** `validate_<field_name>(self, value)`

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'age_rating']
    
    def validate_title(self, value):
        """
        Title validation
        """
        if len(value) < 10:
            raise serializers.ValidationError(
                "Title must be at least 10 characters"
            )
        
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Title must start with capital letter"
            )
        
        return value
    
    def validate_age_rating(self, value):
        """
        Age rating must be positive
        """
        if value < 0:
            raise serializers.ValidationError(
                "Age rating cannot be negative"
            )
        return value
```

**কখন ব্যবহার করবেন:**
- Single field এর validation
- Field এর value check করা

### 2. Object-Level Validation

**কাজ:** Multiple fields একসাথে validate করা।

**Method:** `validate(self, data)`

```python
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'start_date', 'end_date', 'price', 'discount_price']
    
    def validate(self, data):
        """
        Object-level validation
        """
        # Check: end_date > start_date
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        
        # Check: discount_price < price
        if data.get('discount_price') and data['discount_price'] >= data['price']:
            raise serializers.ValidationError({
                'discount_price': 'Discount price must be less than regular price'
            })
        
        return data
```

**কখন ব্যবহার করবেন:**
- Multiple fields এর মধ্যে relationship check করা
- Cross-field validation

### 3. Validator Functions/Classes

**কাজ:** Reusable validation logic।

```python
# Function-based validator
def validate_even_number(value):
    if value % 2 != 0:
        raise serializers.ValidationError(
            f'{value} is not an even number'
        )

# Class-based validator
class MultipleOfValidator:
    def __init__(self, multiple):
        self.multiple = multiple
    
    def __call__(self, value):
        if value % self.multiple != 0:
            raise serializers.ValidationError(
                f'{value} is not a multiple of {self.multiple}'
            )

# Usage
class MySerializer(serializers.Serializer):
    even_number = serializers.IntegerField(
        validators=[validate_even_number]
    )
    
    multiple_of_five = serializers.IntegerField(
        validators=[MultipleOfValidator(5)]
    )
```

**কখন ব্যবহার করবেন:**
- একই validation logic বিভিন্ন জায়গায় ব্যবহার করতে হবে
- Reusable components তৈরি করতে

---

## Built-in Validators

DRF অনেক built-in validators প্রদান করে:

### 1. UniqueValidator

**কাজ:** Field এর value unique কিনা check করে।

```python
from rest_framework.validators import UniqueValidator

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=200,
        validators=[
            UniqueValidator(
                queryset=Article.objects.all(),
                message='Article with this title already exists'
            )
        ]
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content']
```

### 2. UniqueTogetherValidator

**কাজ:** Multiple fields একসাথে unique কিনা check করে।

```python
from rest_framework.validators import UniqueTogetherValidator

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ['id', 'student', 'course']
        validators = [
            UniqueTogetherValidator(
                queryset=CourseEnrollment.objects.all(),
                fields=['student', 'course'],
                message='Student already enrolled in this course'
            )
        ]
```

### 3. Django's Built-in Validators

```python
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
    EmailValidator,
    URLValidator,
    RegexValidator
)

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message='Price must be positive'),
            MaxValueValidator(999999.99, message='Price too high')
        ]
    )
    
    discount_percentage = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    
    phone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be valid'
            )
        ]
    )
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount_percentage', 'phone']
```

---

## Custom Validators

### Function-Based Validators

**সহজ এবং commonly used:**

```python
from rest_framework import serializers

def validate_file_size(value):
    """
    File size maximum 5MB
    """
    limit = 5 * 1024 * 1024  # 5MB
    if value.size > limit:
        raise serializers.ValidationError(
            f'File too large. Size should not exceed 5MB'
        )

def validate_image_extension(value):
    """
    Only jpg, jpeg, png allowed
    """
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    if ext.lower() not in valid_extensions:
        raise serializers.ValidationError(
            f'Unsupported file extension. Allowed: {", ".join(valid_extensions)}'
        )

def validate_no_special_chars(value):
    """
    No special characters allowed
    """
    import re
    if not re.match(r'^[a-zA-Z0-9\s]+$', value):
        raise serializers.ValidationError(
            'Special characters not allowed'
        )

# Usage
class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[validate_no_special_chars]
    )
    
    image = serializers.ImageField(
        validators=[validate_file_size, validate_image_extension]
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'image']
```

### Class-Based Validators

**Configurable validators এর জন্য:**

```python
class FileSizeValidator:
    """
    Validate file size
    """
    def __init__(self, max_size_mb):
        self.max_size = max_size_mb * 1024 * 1024
    
    def __call__(self, value):
        if value.size > self.max_size:
            raise serializers.ValidationError(
                f'File too large. Maximum size: {self.max_size_mb}MB'
            )
    
    def __repr__(self):
        return f'FileSizeValidator({self.max_size_mb}MB)'

class MinWordsValidator:
    """
    Minimum number of words
    """
    def __init__(self, min_words):
        self.min_words = min_words
    
    def __call__(self, value):
        word_count = len(value.split())
        if word_count < self.min_words:
            raise serializers.ValidationError(
                f'Content must have at least {self.min_words} words. Current: {word_count}'
            )

class ProhibitedWordsValidator:
    """
    Check for prohibited words
    """
    def __init__(self, prohibited_words):
        self.prohibited_words = [word.lower() for word in prohibited_words]
    
    def __call__(self, value):
        value_lower = value.lower()
        found_words = [word for word in self.prohibited_words if word in value_lower]
        
        if found_words:
            raise serializers.ValidationError(
                f'Content contains prohibited words: {", ".join(found_words)}'
            )

# Usage
class ArticleSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        validators=[
            MinWordsValidator(100),
            ProhibitedWordsValidator(['spam', 'advertisement'])
        ]
    )
    
    image = serializers.ImageField(
        validators=[FileSizeValidator(5)]  # 5MB
    )
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image']
```

### Conditional Validation

```python
class ConditionalValidator:
    """
    Validate based on another field's value
    """
    def __init__(self, condition_field, condition_value, validator):
        self.condition_field = condition_field
        self.condition_value = condition_value
        self.validator = validator
    
    def __call__(self, value):
        # This needs to be used in object-level validation
        pass

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'is_premium', 'price']
    
    def validate(self, data):
        # If premium, price is required
        if data.get('is_premium') and not data.get('price'):
            raise serializers.ValidationError({
                'price': 'Price is required for premium articles'
            })
        
        # If not premium, price should not be set
        if not data.get('is_premium') and data.get('price'):
            raise serializers.ValidationError({
                'price': 'Price should not be set for free articles'
            })
        
        return data
```

---

## Validator Best Practices

### 1. Reusable Validators

```python
# Good - Reusable
def validate_positive_number(value):
    if value <= 0:
        raise serializers.ValidationError('Must be positive')

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(validators=[validate_positive_number])
    stock = serializers.IntegerField(validators=[validate_positive_number])

# Bad - Repeated code
class ProductSerializer(serializers.ModelSerializer):
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Must be positive')
        return value
    
    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError('Must be positive')
        return value
```

### 2. Clear Error Messages

```python
# Good - Clear message
def validate_username(value):
    if len(value) < 3:
        raise serializers.ValidationError(
            'Username must be at least 3 characters long'
        )
    if not value[0].isalpha():
        raise serializers.ValidationError(
            'Username must start with a letter'
        )

# Bad - Vague message
def validate_username(value):
    if len(value) < 3 or not value[0].isalpha():
        raise serializers.ValidationError('Invalid username')
```

### 3. Performance Optimization

```python
# Good - Cache expensive operations
class UniqueEmailValidator:
    def __init__(self):
        self._cache = {}
    
    def __call__(self, value):
        if value in self._cache:
            if self._cache[value]:
                raise serializers.ValidationError('Email already exists')
        else:
            exists = User.objects.filter(email=value).exists()
            self._cache[value] = exists
            if exists:
                raise serializers.ValidationError('Email already exists')

# Bad - Query every time
def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError('Email already exists')
```

### 4. Organize Validators

```python
# validators.py
"""
Reusable validators for the project
"""

def validate_phone_number(value):
    """Validate phone number format"""
    pass

def validate_postal_code(value):
    """Validate postal code"""
    pass

class FileSizeValidator:
    """Validate file size"""
    pass

# serializers.py
from .validators import validate_phone_number, FileSizeValidator

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone_number])
```

---

# Part 2: Pagination

## Pagination পরিচিতি

Pagination হলো large datasets কে ছোট ছোট pages এ ভাগ করা।

**সমস্যা:**

```python
# 10,000 articles আছে
articles = Article.objects.all()
serializer = ArticleSerializer(articles, many=True)
return Response(serializer.data)

# Problems:
# 1. Slow response (10,000 objects serialize করতে হবে)
# 2. Large response size (MBs of JSON data)
# 3. Memory issues
# 4. Poor user experience
```

**সমাধান: Pagination**

```python
# শুধু 20 articles at a time
# Page 1: Articles 1-20
# Page 2: Articles 21-40
# ...
```

---

## Pagination কী এবং কেন?

### Pagination কী?

**সহজ ভাষায়:** Data কে ছোট ছোট chunks (pages) এ ভাগ করা।

**উদাহরণ:**
- Google search results - প্রতি page এ 10 results
- Facebook feed - scroll করলে নতুন posts load হয়
- E-commerce products - প্রতি page এ 24 products

### কেন Pagination প্রয়োজন?

1. **Performance** - কম data = দ্রুত response
2. **Memory** - Server এবং client উভয়ের জন্য
3. **User Experience** - সব data একসাথে দেখার দরকার নেই
4. **Bandwidth** - কম data transfer

### Pagination কীভাবে কাজ করে?

```
Database: 100 articles

Without Pagination:
Request: GET /articles/
Response: All 100 articles

With Pagination (page_size=10):
Request: GET /articles/?page=1
Response: Articles 1-10 + pagination info

Request: GET /articles/?page=2
Response: Articles 11-20 + pagination info
```

---

## Pagination Types

DRF তিন ধরনের pagination styles প্রদান করে:

| Type | URL Example | Use Case | Performance |
|------|-------------|----------|-------------|
| **PageNumberPagination** | `?page=2` | সবচেয়ে common | Good |
| **LimitOffsetPagination** | `?limit=20&offset=40` | Flexible control | Good |
| **CursorPagination** | `?cursor=cD0yMDIx...` | Large/real-time data | Excellent |

### কোনটা কখন ব্যবহার করবেন?

```python
# PageNumberPagination - 90% cases
# - Simple pagination
# - Blog posts, products, users
# - URL: ?page=1, ?page=2

# LimitOffsetPagination - Specific cases
# - Client needs control over page size
# - Infinite scrolling
# - URL: ?limit=20&offset=40

# CursorPagination - Large datasets
# - Social media feeds
# - Real-time data
# - 10,000+ records
# - URL: ?cursor=cD0yMDIx...
```

---

## PageNumberPagination

সবচেয়ে commonly used pagination style।

### Setup (Global):

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20  # প্রতি page এ 20 items
}
```

### Response Format:

```json
{
    "count": 100,
    "next": "http://api.example.com/articles/?page=3",
    "previous": "http://api.example.com/articles/?page=1",
    "results": [
        {"id": 21, "title": "Article 21"},
        {"id": 22, "title": "Article 22"},
        ...
        {"id": 40, "title": "Article 40"}
    ]
}
```

### Custom PageNumberPagination:

```python
# pagination.py
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Client can change page size
    max_page_size = 100  # Maximum allowed page size
    page_query_param = 'page'  # Query parameter name

# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPageNumberPagination
```

### Usage Examples:

```bash
# Default page size (10)
GET /articles/

# Specific page
GET /articles/?page=2

# Custom page size
GET /articles/?page=1&page_size=50

# Last page
GET /articles/?page=last
```

### Configuration Options:

```python
class CustomPagination(PageNumberPagination):
    # Page size
    page_size = 20
    
    # Allow client to set page size
    page_size_query_param = 'page_size'
    
    # Maximum page size client can request
    max_page_size = 100
    
    # Query parameter for page number
    page_query_param = 'page'
    
    # Values for last page
    last_page_strings = ('last',)
```

---

## LimitOffsetPagination

Client limit এবং offset control করতে পারে।

### Setup:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}
```

### Response Format:

```json
{
    "count": 100,
    "next": "http://api.example.com/articles/?limit=20&offset=40",
    "previous": "http://api.example.com/articles/?limit=20&offset=0",
    "results": [...]
}
```

### Usage:

```bash
# First 20 items
GET /articles/?limit=20&offset=0

# Next 20 items
GET /articles/?limit=20&offset=20

# Items 41-60
GET /articles/?limit=20&offset=40

# Custom limit
GET /articles/?limit=50&offset=0
```

### Custom LimitOffsetPagination:

```python
from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20  # Default limit
    max_limit = 100  # Maximum limit
    limit_query_param = 'limit'
    offset_query_param = 'offset'
```

### কখন ব্যবহার করবেন:

- Infinite scrolling
- Client কে flexibility দিতে চান
- Skip করে data নিতে হবে

---

## CursorPagination

Large datasets এবং real-time data এর জন্য সবচেয়ে efficient।

### Setup:

```python
from rest_framework.pagination import CursorPagination

class ArticleCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'  # অবশ্যই ordering দিতে হবে
    cursor_query_param = 'cursor'
```

### Response Format:

```json
{
    "next": "http://api.example.com/articles/?cursor=cD0yMDIx...",
    "previous": "http://api.example.com/articles/?cursor=cj0xJnA9Mg==",
    "results": [...]
}
```

### Usage:

```bash
# First page
GET /articles/

# Next page
GET /articles/?cursor=cD0yMDIx...

# Previous page
GET /articles/?cursor=cj0xJnA9Mg==
```

### সুবিধা:

1. **Performance** - Indexed fields ব্যবহার করে, offset এর চেয়ে দ্রুত
2. **Consistency** - নতুন data add হলেও consistent results
3. **Scalability** - Large datasets এ excellent performance

### অসুবিধা:

1. **No Random Access** - Specific page এ যেতে পারবেন না
2. **Ordering Required** - অবশ্যই ordering field লাগবে
3. **Complex Cursors** - URLs complex হয়

### কখন ব্যবহার করবেন:

- Social media feeds
- Real-time data (chat messages, notifications)
- 10,000+ records
- Data frequently changes

---

## Custom Pagination

নিজের custom pagination তৈরি করা:

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'pagination': {
                'count': self.page.paginator.count,
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'page_size': self.page_size,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'data': data
        })

# Response:
# {
#     "success": true,
#     "pagination": {
#         "count": 100,
#         "page": 2,
#         "pages": 10,
#         "page_size": 10,
#         "next": "...",
#         "previous": "..."
#     },
#     "data": [...]
# }
```

### Custom Response Schema:

```python
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'meta': {
                'total_count': self.page.paginator.count,
                'page_count': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'per_page': self.page_size
            },
            'results': data
        })
```

---

## Pagination Best Practices

### 1. Always Enable Pagination

```python
# Good - Pagination enabled
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Bad - No pagination (performance issues!)
REST_FRAMEWORK = {
    # No pagination settings
}
```

### 2. Reasonable Page Size

```python
# Good - Reasonable sizes
class CustomPagination(PageNumberPagination):
    page_size = 20  # Good for most cases
    max_page_size = 100  # Prevent abuse

# Bad - Too large
class BadPagination(PageNumberPagination):
    page_size = 1000  # Too many items!
    max_page_size = 10000  # Way too large!
```

### 3. Use CursorPagination for Large Datasets

```python
# Good - CursorPagination for large data
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = CursorPagination  # Efficient!

# Bad - PageNumberPagination for 100,000+ records
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    pagination_class = PageNumberPagination  # Slow for large data!
```

### 4. Optimize Queries

```python
# Good - Optimized queryset
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination

# Bad - N+1 queries
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()  # Will cause N+1 problem!
```

### 5. Consistent Pagination Across API

```python
# Good - Same pagination everywhere
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'myapp.pagination.StandardPagination',
    'PAGE_SIZE': 20
}

# Bad - Different pagination everywhere
class ArticleViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

class UserViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination  # Inconsistent!
```

### 6. Document Pagination

```python
class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for articles.
    
    Pagination:
    - Default page size: 20
    - Max page size: 100
    - Query params: ?page=2&page_size=50
    
    Example:
    GET /api/articles/?page=1&page_size=20
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: Blog API with Pagination

```python
# pagination.py
class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

# views.py
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title', 'content']

# URLs:
# GET /articles/                    -> Page 1 (10 articles)
# GET /articles/?page=2             -> Page 2
# GET /articles/?page_size=20       -> 20 articles per page
# GET /articles/?category=tech&page=1  -> Filtered + paginated
```

### উদাহরণ 2: E-commerce Products

```python
class ProductPagination(PageNumberPagination):
    page_size = 24  # Common for product grids
    page_size_query_param = 'per_page'
    max_page_size = 100

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
```

### উদাহরণ 3: Social Media Feed

```python
class FeedCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = FeedCursorPagination
    
    def get_queryset(self):
        # User's feed
        return Post.objects.filter(
            author__in=self.request.user.following.all()
        ).select_related('author').prefetch_related('likes')
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Validators: https://www.django-rest-framework.org/api-guide/validators/
- Django REST Framework Pagination: https://www.django-rest-framework.org/api-guide/pagination/

### সম্পর্কিত বিষয়
- Serializers
- Filtering
- Searching
- Ordering

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
