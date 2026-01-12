# Django REST Framework - Request Object

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Request কী?](#request-কী)
3. [Request কখন আসে?](#request-কখন-আসে)
4. [Request Parsing](#request-parsing)
   - [request.data](#requestdata)
   - [request.query_params](#requestquery_params)
   - [request.parsers](#requestparsers)
5. [Content Negotiation](#content-negotiation)
   - [request.accepted_renderer](#requestaccepted_renderer)
   - [request.accepted_media_type](#requestaccepted_media_type)
6. [Authentication](#authentication)
   - [request.user](#requestuser)
   - [request.auth](#requestauth)
   - [request.authenticators](#requestauthenticators)
7. [Browser Enhancements](#browser-enhancements)
   - [request.method](#requestmethod)
   - [request.content_type](#requestcontent_type)
   - [request.stream](#requeststream)
8. [Standard HttpRequest Attributes](#standard-httprequest-attributes)
9. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)
10. [Best Practices](#best-practices)
11. [Error Handling](#error-handling)

---

## পরিচিতি

Django REST Framework এর `Request` class হলো Django এর standard `HttpRequest` এর একটি extended version যা বিশেষভাবে RESTful API তৈরির জন্য ডিজাইন করা হয়েছে। এটি flexible request parsing, authentication, এবং content negotiation এর সুবিধা যোগ করে।

`Request` class traditional inheritance এর মাধ্যমে `HttpRequest` থেকে inherit করে না, বরং composition ব্যবহার করে এর functionality extend করে এবং সব standard Django request features বজায় রাখে।

---

## Request কী?

`Request` object হলো Django REST Framework এর core component যা incoming HTTP requests handle করে। এটি প্রদান করে:

- বিভিন্ন ধরনের request data এর flexible parsing (JSON, XML, form data, ইত্যাদি)
- প্রতিটি request এর জন্য আলাদা authentication support
- Content negotiation এর সুবিধা
- Browser-based PUT, PATCH, এবং DELETE operations এর enhancement
- সব standard Django HttpRequest attributes এর access

**Django এর HttpRequest থেকে মূল পার্থক্য:**

Django এর `HttpRequest` traditional web applications এর জন্য ডিজাইন করা যেখানে form-based data ব্যবহার হয়, কিন্তু DRF এর `Request` RESTful APIs এর জন্য optimized যা বিভিন্ন content types এবং HTTP methods এর সাথে কাজ করে।

---

## Request কখন আসে?

`Request` object নিম্নলিখিত পরিস্থিতিতে তৈরি হয় এবং উপলব্ধ থাকে:

### 1. APIView Class-Based Views

যখন আপনি `APIView` অথবা এর subclasses (যেমন `GenericAPIView`, `ListAPIView`, ইত্যাদি) ব্যবহার করেন, তখন request object স্বয়ংক্রিয়ভাবে তৈরি হয় এবং আপনার view methods এ pass করা হয়।

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        # request object is available here
        return Response({'message': 'Hello'})
    
    def post(self, request):
        # request object contains parsed data
        data = request.data
        return Response(data)
```

### 2. Function-Based Views with @api_view Decorator

যখন আপনি `@api_view` decorator ব্যবহার করেন, তখন standard Django request কে DRF `Request` object এ wrap করা হয়।

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def my_view(request):
    # request is a DRF Request object
    if request.method == 'POST':
        data = request.data
        return Response(data)
    return Response({'message': 'GET request'})
```

### 3. ViewSets

ViewSets এ, request object সব action methods এ উপলব্ধ থাকে।

```python
from rest_framework import viewsets

class MyViewSet(viewsets.ModelViewSet):
    def list(self, request):
        # request object available
        queryset = self.get_queryset()
        return Response(...)
    
    def create(self, request):
        # request.data contains the payload
        serializer = self.get_serializer(data=request.data)
        return Response(...)
```

### 4. Request Lifecycle

Request object তৈরি হয় যখন:
- একটি client আপনার API endpoint এ HTTP request পাঠায়
- Request টি Django এর middleware এর মধ্য দিয়ে যায়
- DRF এর `APIView` অথবা `@api_view` decorator standard HttpRequest কে wrap করে
- Wrapped Request object আপনার view function/method এ pass করা হয়

---

## Request Parsing

DRF এর Request objects flexible request parsing প্রদান করে যা আপনাকে JSON, XML, অথবা অন্যান্য media types এর সাথে form data এর মতো একইভাবে কাজ করতে দেয়।

### request.data

**Type:** `dict` অথবা `QueryDict`

**বর্ণনা:** Request body এর parsed content return করে।

**মূল বৈশিষ্ট্য:**

- সব parsed content অন্তর্ভুক্ত করে (file এবং non-file উভয় inputs)
- POST এর বাইরে অন্যান্য HTTP methods এর জন্য parsing support করে (PUT, PATCH, ইত্যাদি)
- একাধিক content types support করে (JSON, XML, form data, multipart)
- Django এর `request.POST` এবং `request.FILES` এর চেয়ে বেশি flexible

**উদাহরণ:**

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def create_user(request):
    # Access parsed JSON data
    username = request.data.get('username')
    email = request.data.get('email')
    
    # Works with nested data
    profile = request.data.get('profile', {})
    bio = profile.get('bio')
    
    return Response({
        'username': username,
        'email': email,
        'bio': bio
    })
```

**গুরুত্বপূর্ণ নোট:**

- `request.data` immutable (QueryDict এর মতো)
- যদি modify করতে হয়, তাহলে প্রথমে একটি copy তৈরি করুন
- Malformed content এর সাথে `request.data` access করলে `ParseError` raise হয় (400 Bad Request return করে)
- যদি content-type parse করা না যায়, তাহলে `UnsupportedMediaType` raise হয় (415 return করে)

**Django এর request.POST এর সাথে তুলনা:**

| বৈশিষ্ট্য | request.POST | request.data |
|---------|-------------|--------------|
| HTTP Methods | শুধুমাত্র POST | POST, PUT, PATCH, DELETE |
| Content Types | শুধুমাত্র Form data | JSON, XML, form data, ইত্যাদি |
| File Handling | আলাদা request.FILES | request.data তে অন্তর্ভুক্ত |
| Flexibility | সীমিত | উচ্চ |

### request.query_params

**Type:** `QueryDict`

**বর্ণনা:** Django এর `request.GET` এর একটি আরও সঠিক নামকরণ। URL query parameters access করতে ব্যবহৃত হয়।

**GET এর পরিবর্তে query_params কেন ব্যবহার করবেন?**

- আরও semantically সঠিক (query parameters যেকোনো HTTP method এ থাকতে পারে)
- Code clarity এবং readability উন্নত করে
- আপনার codebase কে আরও explicit করে তোলে

**উদাহরণ:**

```python
@api_view(['GET'])
def search_users(request):
    # Access query parameters
    search_term = request.query_params.get('q', '')
    page = request.query_params.get('page', 1)
    limit = request.query_params.get('limit', 10)
    
    # URL: /api/users/?q=john&page=2&limit=20
    
    return Response({
        'search': search_term,
        'page': page,
        'limit': limit
    })
```

**সাধারণ ব্যবহার:**

- Filtering: `?category=electronics&price_min=100`
- Pagination: `?page=2&page_size=20`
- Sorting: `?ordering=-created_at`
- Search: `?search=keyword`

### request.parsers

**Type:** `Parser` instances এর `list`

**বর্ণনা:** Parser instances এর একটি list যা request body parse করতে ব্যবহৃত হবে।

**কীভাবে Set হয়:**

- `APIView` অথবা `@api_view` decorator দ্বারা স্বয়ংক্রিয়ভাবে set হয়
- View এর `parser_classes` attribute এর উপর ভিত্তি করে
- `DEFAULT_PARSER_CLASSES` setting এ fallback করে

**উদাহরণ:**

```python
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView

class MyView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request):
        # request.parsers contains instances of the above parsers
        # You typically don't need to access this directly
        return Response({'received': request.data})
```

**নোট:** আপনাকে সাধারণত এই property সরাসরি access করতে হবে না। এটি DRF দ্বারা internally ব্যবহৃত হয়।

---

## Content Negotiation

Content negotiation server কে client preferences এবং available renderers এর উপর ভিত্তি করে response এর জন্য সেরা representation নির্বাচন করতে দেয়।

### request.accepted_renderer

**Type:** `Renderer` instance

**বর্ণনা:** Content negotiation stage দ্বারা নির্বাচিত renderer instance।

**উদাহরণ:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        # Check which renderer was selected
        renderer = request.accepted_renderer
        
        # You can use this to customize behavior
        if renderer.format == 'json':
            # JSON-specific logic
            pass
        
        return Response({'data': 'example'})
```

### request.accepted_media_type

**Type:** `str`

**বর্ণনা:** Content negotiation stage দ্বারা accepted media type কে represent করে এমন একটি string।

**উদাহরণ:**

```python
@api_view(['GET'])
def my_view(request):
    # Get the accepted media type
    media_type = request.accepted_media_type
    # Example: 'application/json' or 'application/xml'
    
    return Response({
        'media_type': media_type
    })
```

**ব্যবহার:**

বিভিন্ন media types এর জন্য বিভিন্ন serialization schemes implement করতে হলে এটি useful।

---

## Authentication

DRF flexible, per-request authentication প্রদান করে যা আপনাকে সুবিধা দেয়:

- আপনার API এর বিভিন্ন অংশের জন্য বিভিন্ন authentication policies ব্যবহার করতে
- একসাথে একাধিক authentication policies support করতে
- User এবং token উভয় information access করতে

### request.user

**Type:** `User` instance অথবা `AnonymousUser`

**বর্ণনা:** Authenticated user instance return করে।

**Default আচরণ:**

- যদি authenticated হয়: `django.contrib.auth.models.User` instance return করে (অথবা custom user model)
- যদি unauthenticated হয়: `django.contrib.auth.models.AnonymousUser` instance return করে

**উদাহরণ:**

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    # Access authenticated user
    user = request.user
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff
    })

@api_view(['GET'])
def public_view(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        return Response({'message': f'Hello, {request.user.username}'})
    else:
        return Response({'message': 'Hello, Guest'})
```

**সাধারণ Checks:**

```python
# Check if user is authenticated
if request.user.is_authenticated:
    # User is logged in
    pass

# Check if user is anonymous
if request.user.is_anonymous:
    # User is not logged in
    pass

# Check user permissions
if request.user.is_staff:
    # User is staff member
    pass

if request.user.has_perm('app.permission_name'):
    # User has specific permission
    pass
```

### request.auth

**Type:** বিভিন্ন (সাধারণত `Token` instance অথবা `None`)

**বর্ণনা:** যেকোনো অতিরিক্ত authentication context return করে। Exact type authentication policy এর উপর নির্ভর করে।

**সাধারণ Values:**

- Token Authentication: `Token` instance return করে
- JWT Authentication: Decoded JWT payload return করে
- Session Authentication: সাধারণত `None`
- Unauthenticated: `None`

**উদাহরণ:**

```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def protected_view(request):
    # Access the token
    token = request.auth
    
    if token:
        return Response({
            'user': request.user.username,
            'token_key': token.key,
            'token_created': token.created
        })
    
    return Response({'error': 'Not authenticated'}, status=401)
```

**JWT উদাহরণ:**

```python
# With JWT authentication
@api_view(['GET'])
def jwt_view(request):
    # request.auth contains decoded JWT payload
    payload = request.auth
    
    if payload:
        user_id = payload.get('user_id')
        exp = payload.get('exp')
        return Response({'user_id': user_id, 'expires': exp})
    
    return Response({'error': 'Invalid token'}, status=401)
```

### request.authenticators

**Type:** `Authentication` instances এর `list`

**বর্ণনা:** Request authenticate করতে ব্যবহৃত authentication instances এর একটি list।

**কীভাবে Set হয়:**

- `APIView` অথবা `@api_view` decorator দ্বারা স্বয়ংক্রিয়ভাবে set হয়
- View এর `authentication_classes` attribute এর উপর ভিত্তি করে
- `DEFAULT_AUTHENTICATORS` setting এ fallback করে

**উদাহরণ:**

```python
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView

class MyView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get(self, request):
        # request.authenticators contains instances of both authenticators
        # You typically don't need to access this directly
        return Response({'data': 'example'})
```

**নোট:** আপনাকে সাধারণত এই property সরাসরি access করতে হবে না।

**Error Handling:**

`.user` অথবা `.auth` properties access করার সময় আপনি `WrappedAttributeError` encounter করতে পারেন। এটি ঘটে যখন একটি authenticator `AttributeError` raise করে, যা suppress হওয়া থেকে রক্ষা করতে একটি ভিন্ন exception type হিসেবে re-raise করা হয়।

---

## Browser Enhancements

DRF browser-based enhancements support করে যা testing এবং development সহজ করে, বিশেষত HTTP methods এর জন্য যা browsers natively forms এ support করে না।

### request.method

**Type:** `str`

**বর্ণনা:** Request এর HTTP method এর uppercased string representation return করে।

**Supported Methods:**

- GET
- POST
- PUT
- PATCH
- DELETE
- HEAD
- OPTIONS

**Browser Enhancement:**

DRF transparently browser-based PUT, PATCH, এবং DELETE forms support করে method overriding এর মাধ্যমে।

**উদাহরণ:**

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def item_detail(request, pk):
    if request.method == 'GET':
        return Response({'action': 'retrieve', 'id': pk})
    
    elif request.method == 'POST':
        return Response({'action': 'create', 'data': request.data})
    
    elif request.method == 'PUT':
        return Response({'action': 'update', 'id': pk, 'data': request.data})
    
    elif request.method == 'DELETE':
        return Response({'action': 'delete', 'id': pk})
```

### request.content_type

**Type:** `str`

**বর্ণনা:** HTTP request এর body এর media type কে represent করে এমন একটি string return করে, অথবা যদি কোনো media type প্রদান করা না হয় তাহলে একটি empty string।

**উদাহরণ:**

```python
@api_view(['POST'])
def upload_data(request):
    content_type = request.content_type
    # Examples: 'application/json', 'multipart/form-data', 'application/xml'
    
    if content_type == 'application/json':
        # Handle JSON data
        data = request.data
    elif content_type.startswith('multipart/form-data'):
        # Handle file upload
        file = request.data.get('file')
    
    return Response({'content_type': content_type})
```

**Best Practice:**

Better browser compatibility এবং cleaner code এর জন্য `request.META.get('HTTP_CONTENT_TYPE')` এর পরিবর্তে `request.content_type` ব্যবহার করুন।

### request.stream

**Type:** Stream object

**বর্ণনা:** Request body এর content কে represent করে এমন একটি stream return করে।

**উদাহরণ:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class StreamView(APIView):
    def post(self, request):
        # Access raw stream (rarely needed)
        stream = request.stream
        
        # You typically rely on request.data instead
        # which automatically parses the stream
        
        return Response({'received': 'data'})
```

**নোট:** আপনাকে সাধারণত এটি সরাসরি access করতে হবে না, কারণ DRF এর default request parsing এটি আপনার জন্য handle করে।

---

## Standard HttpRequest Attributes

যেহেতু DRF এর `Request` composition এর মাধ্যমে Django এর `HttpRequest` কে extend করে, তাই সব standard attributes এবং methods উপলব্ধ।

### সাধারণভাবে ব্যবহৃত Attributes

#### request.META

**Type:** `dict`

**বর্ণনা:** সব available HTTP headers এবং server metadata সম্বলিত একটি dictionary।

**উদাহরণ:**

```python
@api_view(['GET'])
def request_info(request):
    # Access HTTP headers
    user_agent = request.META.get('HTTP_USER_AGENT')
    remote_addr = request.META.get('REMOTE_ADDR')
    content_length = request.META.get('CONTENT_LENGTH')
    
    # Access custom headers (prefixed with HTTP_)
    custom_header = request.META.get('HTTP_X_CUSTOM_HEADER')
    
    return Response({
        'user_agent': user_agent,
        'ip_address': remote_addr,
        'content_length': content_length,
        'custom_header': custom_header
    })
```

**সাধারণ META Keys:**

- `HTTP_USER_AGENT`: Browser/client information
- `REMOTE_ADDR`: Client IP address
- `HTTP_REFERER`: Referring URL
- `HTTP_ACCEPT`: Accepted content types
- `HTTP_AUTHORIZATION`: Authorization header
- `REQUEST_METHOD`: HTTP method
- `CONTENT_TYPE`: Content type of request body
- `CONTENT_LENGTH`: Length of request body

#### request.session

**Type:** `SessionStore` object

**বর্ণনা:** Session data store করার জন্য একটি dictionary-like object।

**উদাহরণ:**

```python
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    
    # Store data in session
    request.session['username'] = username
    request.session['login_time'] = str(timezone.now())
    
    return Response({'message': 'Logged in'})

@api_view(['GET'])
def session_info(request):
    # Retrieve session data
    username = request.session.get('username')
    login_time = request.session.get('login_time')
    
    return Response({
        'username': username,
        'login_time': login_time
    })
```

#### request.FILES

**Type:** `MultiValueDict`

**বর্ণনা:** সব uploaded files সম্বলিত একটি dictionary-like object।

**উদাহরণ:**

```python
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    # Access uploaded file
    uploaded_file = request.FILES.get('file')
    
    if uploaded_file:
        return Response({
            'filename': uploaded_file.name,
            'size': uploaded_file.size,
            'content_type': uploaded_file.content_type
        })
    
    return Response({'error': 'No file uploaded'}, status=400)
```

**নোট:** DRF এর সাথে, আপনি `request.data` এর মাধ্যমেও files access করতে পারেন যা একটি আরও unified interface প্রদান করে।

#### request.COOKIES

**Type:** `dict`

**বর্ণনা:** সব cookies সম্বলিত একটি dictionary।

**উদাহরণ:**

```python
@api_view(['GET'])
def cookie_info(request):
    # Access cookies
    session_id = request.COOKIES.get('sessionid')
    custom_cookie = request.COOKIES.get('custom_cookie')
    
    return Response({
        'session_id': session_id,
        'custom_cookie': custom_cookie
    })
```

#### request.path

**Type:** `str`

**বর্ণনা:** URL এর path অংশ।

**উদাহরণ:**

```python
@api_view(['GET'])
def path_info(request):
    # request.path: '/api/users/123/'
    # request.get_full_path(): '/api/users/123/?page=1'
    
    return Response({
        'path': request.path,
        'full_path': request.get_full_path()
    })
```

#### request.headers

**Type:** `HttpHeaders` object (Django 2.2+)

**বর্ণনা:** HTTP headers access করার জন্য একটি case-insensitive dictionary-like object।

**উদাহরণ:**

```python
@api_view(['GET'])
def header_info(request):
    # Access headers (case-insensitive)
    auth_header = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    custom_header = request.headers.get('X-Custom-Header')
    
    return Response({
        'authorization': auth_header,
        'content_type': content_type,
        'custom': custom_header
    })
```

---

## সাধারণ ব্যবহারের উদাহরণ

### 1. JSON POST Requests Handle করা

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def create_post(request):
    # Access JSON data
    title = request.data.get('title')
    content = request.data.get('content')
    author_id = request.user.id
    
    # Validate data
    if not title or not content:
        return Response(
            {'error': 'Title and content are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create post (example)
    post = Post.objects.create(
        title=title,
        content=content,
        author_id=author_id
    )
    
    return Response({
        'id': post.id,
        'title': post.title,
        'created_at': post.created_at
    }, status=status.HTTP_201_CREATED)
```

### 2. Query Parameters দিয়ে Filtering

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def list_products(request):
    # Get query parameters
    category = request.query_params.get('category')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    search = request.query_params.get('search', '')
    
    # Build queryset
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    if search:
        queryset = queryset.filter(name__icontains=search)
    
    # Serialize and return
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)
```

### 3. File Upload Handling

```python
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    # Access uploaded file
    avatar = request.data.get('avatar')
    
    if not avatar:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file type
    if not avatar.content_type.startswith('image/'):
        return Response(
            {'error': 'File must be an image'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Save file
    user = request.user
    user.avatar = avatar
    user.save()
    
    return Response({
        'message': 'Avatar uploaded successfully',
        'filename': avatar.name
    })
```

### 4. Authentication-Based Logic

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user = request.user
    
    # Get user-specific data
    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(user=user)
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'stats': {
            'total_posts': posts.count(),
            'total_comments': comments.count()
        }
    })
```

### 5. Query Parameters দিয়ে Pagination

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator

@api_view(['GET'])
def paginated_list(request):
    # Get pagination parameters
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    
    # Get all items
    items = Item.objects.all()
    
    # Paginate
    paginator = Paginator(items, page_size)
    page_obj = paginator.get_page(page)
    
    # Serialize
    serializer = ItemSerializer(page_obj, many=True)
    
    return Response({
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'results': serializer.data
    })
```

### 6. একাধিক Content Types Handle করা

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def flexible_endpoint(request):
    content_type = request.content_type
    
    if content_type == 'application/json':
        # Handle JSON
        data = request.data
        return Response({'received': 'json', 'data': data})
    
    elif content_type.startswith('multipart/form-data'):
        # Handle form data with files
        file = request.data.get('file')
        name = request.data.get('name')
        return Response({'received': 'multipart', 'name': name})
    
    elif content_type == 'application/x-www-form-urlencoded':
        # Handle form data
        data = request.data
        return Response({'received': 'form', 'data': data})
    
    else:
        return Response({'error': 'Unsupported content type'}, status=415)
```

---

## Best Practices

### 1. request.POST এর পরিবর্তে request.data ব্যবহার করুন

```python
# খারাপ
@api_view(['POST'])
def bad_view(request):
    username = request.POST.get('username')  # Limited to form data
    return Response({'username': username})

# ভালো
@api_view(['POST'])
def good_view(request):
    username = request.data.get('username')  # Works with JSON, XML, etc.
    return Response({'username': username})
```

### 2. request.GET এর পরিবর্তে request.query_params ব্যবহার করুন

```python
# খারাপ
@api_view(['GET'])
def bad_view(request):
    search = request.GET.get('search')  # Less clear
    return Response({'search': search})

# ভালো
@api_view(['GET'])
def good_view(request):
    search = request.query_params.get('search')  # More explicit
    return Response({'search': search})
```

### 3. সবসময় Input Data Validate করুন

```python
@api_view(['POST'])
def create_item(request):
    # Use serializers for validation
    serializer = ItemSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 4. Authentication সুন্দরভাবে Handle করুন

```python
@api_view(['GET'])
def flexible_view(request):
    if request.user.is_authenticated:
        # Return personalized data
        return Response({
            'message': f'Hello, {request.user.username}',
            'user_data': get_user_data(request.user)
        })
    else:
        # Return public data
        return Response({
            'message': 'Hello, Guest',
            'public_data': get_public_data()
        })
```

### 5. Query Parameters এর জন্য Default Values ব্যবহার করুন

```python
@api_view(['GET'])
def list_items(request):
    # Provide sensible defaults
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    ordering = request.query_params.get('ordering', '-created_at')
    
    # Use the parameters
    items = Item.objects.all().order_by(ordering)
    # ... pagination logic
```

### 6. প্রয়োজন হলে Content Type Check করুন

```python
@api_view(['POST'])
def upload_endpoint(request):
    if not request.content_type.startswith('multipart/form-data'):
        return Response(
            {'error': 'This endpoint requires multipart/form-data'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Process file upload
    file = request.data.get('file')
    # ...
```

### 7. request.data সরাসরি Modify করবেন না

```python
# খারাপ
@api_view(['POST'])
def bad_view(request):
    request.data['modified'] = True  # Will raise error (immutable)
    return Response(request.data)

# ভালো
@api_view(['POST'])
def good_view(request):
    data = request.data.copy()  # Create a mutable copy
    data['modified'] = True
    return Response(data)
```

### 8. Query Parameters এর জন্য Type Conversion ব্যবহার করুন

```python
@api_view(['GET'])
def search_view(request):
    # Query parameters are always strings, convert as needed
    try:
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        min_price = float(request.query_params.get('min_price', 0))
    except ValueError:
        return Response(
            {'error': 'Invalid parameter type'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Use the converted values
    # ...
```

---

## Error Handling

### 1. ParseError (400 Bad Request)

Malformed content এর সাথে `request.data` access করলে raise হয়।

```python
from rest_framework.exceptions import ParseError
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def my_view(request):
    try:
        data = request.data
        # Process data
    except ParseError as e:
        return Response(
            {'error': 'Malformed request data', 'detail': str(e)},
            status=400
        )
```

**নোট:** DRF এর `APIView` এবং `@api_view` স্বয়ংক্রিয়ভাবে `ParseError` catch করে এবং একটি 400 response return করে।

### 2. UnsupportedMediaType (415)

Request content-type parse করা না গেলে raise হয়।

```python
# Automatically handled by DRF
# Returns 415 Unsupported Media Type response
```

### 3. WrappedAttributeError

`.user` অথবা `.auth` properties access করার সময় raise হয় যদি একটি authenticator `AttributeError` raise করে।

```python
from rest_framework.request import WrappedAttributeError

@api_view(['GET'])
def my_view(request):
    try:
        user = request.user
    except WrappedAttributeError:
        # Authenticator has an issue
        return Response(
            {'error': 'Authentication error'},
            status=500
        )
```

### 4. Missing Data Handle করা

```python
@api_view(['POST'])
def create_user(request):
    # Check for required fields
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in request.data]
    
    if missing_fields:
        return Response(
            {'error': f'Missing required fields: {", ".join(missing_fields)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Process data
    # ...
```

### 5. Invalid Query Parameters Handle করা

```python
@api_view(['GET'])
def list_items(request):
    try:
        page = int(request.query_params.get('page', 1))
        if page < 1:
            raise ValueError('Page must be positive')
    except ValueError as e:
        return Response(
            {'error': f'Invalid page parameter: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Continue processing
    # ...
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Requests: https://www.django-rest-framework.org/api-guide/requests/
- Django REST Framework Authentication: https://www.django-rest-framework.org/api-guide/authentication/
- Django REST Framework Parsers: https://www.django-rest-framework.org/api-guide/parsers/

### সম্পর্কিত বিষয়
- Response Object
- Serializers
- ViewSets
- Authentication Classes
- Permission Classes
- Parser Classes

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
