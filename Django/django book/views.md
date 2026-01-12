# Django REST Framework - Views

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Class-Based Views (CBV)](#class-based-views-cbv)
   - [APIView কী?](#apiview-কী)
   - [APIView কখন ব্যবহার করবেন?](#apiview-কখন-ব্যবহার-করবেন)
   - [APIView এর মূল বৈশিষ্ট্য](#apiview-এর-মূল-বৈশিষ্ট্য)
3. [API Policy Attributes](#api-policy-attributes)
   - [renderer_classes](#renderer_classes)
   - [parser_classes](#parser_classes)
   - [authentication_classes](#authentication_classes)
   - [throttle_classes](#throttle_classes)
   - [permission_classes](#permission_classes)
   - [content_negotiation_class](#content_negotiation_class)
4. [API Policy Instantiation Methods](#api-policy-instantiation-methods)
5. [API Policy Implementation Methods](#api-policy-implementation-methods)
6. [Dispatch Methods](#dispatch-methods)
7. [HTTP Method Handlers](#http-method-handlers)
8. [Class-Based Views এর উদাহরণ](#class-based-views-এর-উদাহরণ)
9. [Function-Based Views (FBV)](#function-based-views-fbv)
   - [@api_view Decorator](#api_view-decorator)
   - [API Policy Decorators](#api-policy-decorators)
10. [CBV vs FBV - কখন কোনটি ব্যবহার করবেন?](#cbv-vs-fbv---কখন-কোনটি-ব্যবহার-করবেন)
11. [Best Practices](#best-practices)
12. [সাধারণ ব্যবহারের উদাহরণ](#সাধারণ-ব্যবহারের-উদাহরণ)
13. [Error Handling](#error-handling)

---

## শেখার ক্রম

এই documentation টি পড়ার সময় নিচের ক্রম অনুসরণ করুন। Star চিহ্ন দিয়ে priority বোঝানো হয়েছে:

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **পরিচিতি** - Views কী এবং কেন প্রয়োজন
2. ⭐⭐⭐ **Class-Based Views (CBV)** - APIView এর মূল ধারণা
3. ⭐⭐⭐ **HTTP Method Handlers** - GET, POST, PUT, DELETE কীভাবে handle করবেন
4. ⭐⭐⭐ **Class-Based Views এর উদাহরণ** (উদাহরণ 1-3) - Basic usage

### এরপর পড়ুন (গুরুত্বপূর্ণ):

5. ⭐⭐ **API Policy Attributes** - authentication_classes, permission_classes, parser_classes
6. ⭐⭐ **Function-Based Views (FBV)** - @api_view decorator এবং basic usage
7. ⭐⭐ **CBV vs FBV** - কখন কোনটি ব্যবহার করবেন
8. ⭐⭐ **Best Practices** - Clean code লেখার নিয়ম
9. ⭐⭐ **সাধারণ ব্যবহারের উদাহরণ** - Real-world scenarios

### শেষে পড়ুন (Advanced):

10. ⭐ **API Policy Instantiation Methods** - get_permissions(), get_authenticators() ইত্যাদি
11. ⭐ **API Policy Implementation Methods** - check_permissions(), check_throttles()
12. ⭐ **Dispatch Methods** - initial(), handle_exception(), finalize_response()
13. ⭐ **Error Handling** - Custom exception handlers

### দ্রষ্টব্য:
- ⭐⭐⭐ = অবশ্যই পড়তে হবে, এগুলো ছাড়া কাজ করা যাবে না
- ⭐⭐ = গুরুত্বপূর্ণ, ভালো code লেখার জন্য জানা দরকার
- ⭐ = Advanced topics, প্রয়োজন হলে পড়বেন

---

## পরিচিতি

Django REST Framework দুই ধরনের views প্রদান করে:

1. **Class-Based Views (CBV)** - Object-oriented approach, reusable এবং structured
2. **Function-Based Views (FBV)** - Simple এবং straightforward approach

এই documentation এ আমরা মূলত **Class-Based Views** এর উপর focus করব কারণ এটি:
- বেশি reusable এবং maintainable
- DRY (Don't Repeat Yourself) principle follow করে
- Built-in authentication, permissions, throttling সহজে handle করে
- Large এবং complex projects এর জন্য উপযুক্ত

---

## Class-Based Views (CBV)

### APIView কী?

`APIView` হলো Django REST Framework এর সবচেয়ে fundamental class-based view। এটি Django এর standard `View` class কে extend করে এবং API-specific functionality যোগ করে।

**Django এর View থেকে APIView এর পার্থক্য:**

| বৈশিষ্ট্য | Django View | DRF APIView |
|---------|------------|-------------|
| Request Object | `HttpRequest` | DRF এর `Request` |
| Response Object | `HttpResponse` | DRF এর `Response` |
| Content Negotiation | ম্যানুয়াল | স্বয়ংক্রিয় |
| Authentication | ম্যানুয়াল | Built-in support |
| Permissions | ম্যানুয়াল | Built-in support |
| Throttling | ম্যানুয়াল | Built-in support |
| Exception Handling | Django এর standard | DRF এর custom handling |

### APIView কখন ব্যবহার করবেন?

`APIView` ব্যবহার করুন যখন:

1. **Custom Logic প্রয়োজন** - Standard CRUD operations এর বাইরে কিছু করতে হবে
2. **Multiple Models** - একাধিক models থেকে data aggregate করতে হবে
3. **Non-CRUD Endpoints** - Login, logout, password reset, dashboard ইত্যাদি
4. **External Services** - Third-party APIs এর সাথে interact করতে হবে
5. **Complex Business Logic** - যা generic views দিয়ে সহজে করা যায় না
6. **Full Control** - Request/Response এর প্রতিটি aspect নিয়ন্ত্রণ করতে চান

### APIView এর মূল বৈশিষ্ট্য

1. **DRF Request এবং Response Objects**
   - Handler methods DRF এর `Request` instances পায়, Django এর `HttpRequest` নয়
   - `Response` return করতে পারেন, যা automatically content negotiation করে

2. **Automatic Exception Handling**
   - `APIException` এবং এর subclasses automatically catch হয়
   - Appropriate error responses generate হয়

3. **Built-in Authentication এবং Permissions**
   - Handler method call হওয়ার আগে authentication এবং permission checks run হয়

4. **HTTP Method Handlers**
   - `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()` methods define করতে পারেন

**Basic Structure:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MyAPIView(APIView):
    # API policy attributes
    authentication_classes = [...]
    permission_classes = [...]
    
    def get(self, request, *args, **kwargs):
        # Handle GET request
        return Response({'message': 'GET request'})
    
    def post(self, request, *args, **kwargs):
        # Handle POST request
        data = request.data
        return Response(data, status=status.HTTP_201_CREATED)
```

---

## API Policy Attributes

এই attributes গুলো আপনার API view এর বিভিন্ন aspects control করে। এগুলো class level এ define করতে হয়।

### renderer_classes

**কাজ:** Response কে কোন format এ render করা হবে তা নির্ধারণ করে।

**Default:** `settings.py` এর `DEFAULT_RENDERER_CLASSES` থেকে আসে

**উদাহরণ:**

```python
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

class MyView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
    def get(self, request):
        return Response({'message': 'Hello'})
```

**Common Renderers:**
- `JSONRenderer` - JSON format
- `BrowsableAPIRenderer` - HTML browsable API
- `TemplateHTMLRenderer` - HTML templates
- `XMLRenderer` - XML format

### parser_classes

**কাজ:** Request body কোন format থেকে parse করা হবে তা নির্ধারণ করে।

**Default:** `settings.py` এর `DEFAULT_PARSER_CLASSES` থেকে আসে

**উদাহরণ:**

```python
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        file = request.data.get('file')
        # Handle file upload
        return Response({'filename': file.name})
```

**Common Parsers:**
- `JSONParser` - JSON data
- `FormParser` - HTML form data
- `MultiPartParser` - Multipart form data (file uploads)
- `FileUploadParser` - Raw file uploads

### authentication_classes

**কাজ:** Request authenticate করার জন্য কোন authentication schemes ব্যবহার করা হবে।

**Default:** `settings.py` এর `DEFAULT_AUTHENTICATION_CLASSES` থেকে আসে

**উদাহরণ:**

```python
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get(self, request):
        user = request.user
        return Response({'username': user.username})
```

**Common Authentication Classes:**
- `TokenAuthentication` - Token-based auth
- `SessionAuthentication` - Session-based auth
- `BasicAuthentication` - HTTP Basic auth
- `JWTAuthentication` - JWT tokens (third-party package)

### throttle_classes

**কাজ:** Request rate limiting control করে - কতবার request করা যাবে তা নির্ধারণ করে।

**Default:** `settings.py` এর `DEFAULT_THROTTLE_CLASSES` থেকে আসে

**উদাহরণ:**

```python
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ThrottledView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get(self, request):
        return Response({'message': 'Rate limited endpoint'})
```

**Common Throttle Classes:**
- `AnonRateThrottle` - Anonymous users এর জন্য
- `UserRateThrottle` - Authenticated users এর জন্য
- `ScopedRateThrottle` - Specific scopes এর জন্য

### permission_classes

**কাজ:** কে এই view access করতে পারবে তা নির্ধারণ করে।

**Default:** `settings.py` এর `DEFAULT_PERMISSION_CLASSES` থেকে আসে

**উদাহরণ:**

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        return Response({'message': 'Admin only content'})
```

**Common Permission Classes:**
- `AllowAny` - সবাই access করতে পারবে
- `IsAuthenticated` - শুধুমাত্র authenticated users
- `IsAdminUser` - শুধুমাত্র admin users
- `IsAuthenticatedOrReadOnly` - Read করতে সবাই পারবে, modify শুধু authenticated users

### content_negotiation_class

**কাজ:** Client এবং server এর মধ্যে content type negotiation কীভাবে হবে তা নির্ধারণ করে।

**Default:** `DefaultContentNegotiation`

**উদাহরণ:**

```python
from rest_framework.negotiation import DefaultContentNegotiation

class MyView(APIView):
    content_negotiation_class = DefaultContentNegotiation
    
    def get(self, request):
        return Response({'data': 'example'})
```

**নোট:** সাধারণত এটি override করার প্রয়োজন হয় না।

---

## API Policy Instantiation Methods

এই methods গুলো DRF internally ব্যবহার করে বিভিন্ন API policies instantiate করতে। সাধারণত আপনাকে এগুলো override করতে হবে না।

### get_renderers(self)

Renderer instances এর list return করে।

```python
def get_renderers(self):
    # Custom logic to select renderers
    if self.request.user.is_staff:
        return [BrowsableAPIRenderer(), JSONRenderer()]
    return [JSONRenderer()]
```

### get_parsers(self)

Parser instances এর list return করে।

```python
def get_parsers(self):
    # Custom parser selection
    return [parser() for parser in self.parser_classes]
```

### get_authenticators(self)

Authentication instances এর list return করে।

```python
def get_authenticators(self):
    # Custom authentication logic
    return [auth() for auth in self.authentication_classes]
```

### get_throttles(self)

Throttle instances এর list return করে।

```python
def get_throttles(self):
    # Custom throttle logic
    return [throttle() for throttle in self.throttle_classes]
```

### get_permissions(self)

Permission instances এর list return করে।

**এটি frequently override করা হয় different HTTP methods এর জন্য different permissions set করতে:**

```python
def get_permissions(self):
    if self.request.method == 'GET':
        return [AllowAny()]
    return [IsAuthenticated()]
```

### get_content_negotiator(self)

Content negotiator instance return করে।

### get_exception_handler(self)

Exception handler function return করে।

---

## API Policy Implementation Methods

এই methods handler method call হওয়ার আগে execute হয়।

### check_permissions(self, request)

সব permission checks run করে। যদি কোনো permission fail করে, তাহলে `PermissionDenied` exception raise করে।

```python
def check_permissions(self, request):
    # Custom permission checking logic
    super().check_permissions(request)
    
    # Additional custom checks
    if not request.user.is_verified:
        raise PermissionDenied('Email not verified')
```

### check_throttles(self, request)

সব throttle checks run করে। যদি rate limit exceed হয়, তাহলে `Throttled` exception raise করে।

```python
def check_throttles(self, request):
    # Custom throttle checking
    super().check_throttles(request)
```

### perform_content_negotiation(self, request, force=False)

Client এবং server এর মধ্যে content negotiation করে এবং appropriate renderer select করে।

---

## Dispatch Methods

এই methods view এর `.dispatch()` method দ্বারা সরাসরি call করা হয়।

### initial(self, request, *args, **kwargs)

Handler method call হওয়ার আগে যে actions নিতে হবে সেগুলো perform করে:
- Permissions enforce করা
- Throttling check করা
- Content negotiation করা

```python
def initial(self, request, *args, **kwargs):
    super().initial(request, *args, **kwargs)
    
    # Custom initialization logic
    self.custom_setup()
```

**নোট:** সাধারণত এটি override করার প্রয়োজন হয় না।

### handle_exception(self, exc)

Handler method থেকে throw করা যেকোনো exception এই method এ pass করা হয়।

**Default behavior:**
- `APIException` এবং এর subclasses handle করে
- Django এর `Http404` এবং `PermissionDenied` handle করে
- Appropriate error response return করে

```python
from rest_framework.views import exception_handler

def handle_exception(self, exc):
    # Custom exception handling
    response = super().handle_exception(exc)
    
    # Add custom error information
    if response is not None:
        response.data['custom_error_code'] = 'ERR_001'
    
    return response
```

### initialize_request(self, request, *args, **kwargs)

Django এর `HttpRequest` কে DRF এর `Request` instance এ convert করে।

**নোট:** সাধারণত এটি override করার প্রয়োজন হয় না।

### finalize_response(self, request, response, *args, **kwargs)

Handler method থেকে return করা `Response` object কে proper content type এ render করে।

```python
def finalize_response(self, request, response, *args, **kwargs):
    response = super().finalize_response(request, response, *args, **kwargs)
    
    # Add custom headers
    response['X-Custom-Header'] = 'CustomValue'
    
    return response
```

---

## HTTP Method Handlers

এগুলো হলো actual methods যেগুলো আপনি define করবেন বিভিন্ন HTTP methods handle করার জন্য।

### get(self, request, *args, **kwargs)

GET requests handle করে - data retrieve করার জন্য।

```python
def get(self, request, *args, **kwargs):
    data = {'message': 'GET request handled'}
    return Response(data)
```

### post(self, request, *args, **kwargs)

POST requests handle করে - নতুন resource create করার জন্য।

```python
def post(self, request, *args, **kwargs):
    data = request.data
    # Create new resource
    return Response(data, status=status.HTTP_201_CREATED)
```

### put(self, request, *args, **kwargs)

PUT requests handle করে - existing resource সম্পূর্ণ update করার জন্য।

```python
def put(self, request, pk, *args, **kwargs):
    # Update entire resource
    return Response({'message': 'Resource updated'})
```

### patch(self, request, *args, **kwargs)

PATCH requests handle করে - existing resource partially update করার জন্য।

```python
def patch(self, request, pk, *args, **kwargs):
    # Partial update
    return Response({'message': 'Resource partially updated'})
```

### delete(self, request, *args, **kwargs)

DELETE requests handle করে - resource delete করার জন্য।

```python
def delete(self, request, pk, *args, **kwargs):
    # Delete resource
    return Response(status=status.HTTP_204_NO_CONTENT)
```

### head(self, request, *args, **kwargs)

HEAD requests handle করে - metadata retrieve করার জন্য।

### options(self, request, *args, **kwargs)

OPTIONS requests handle করে - available methods এবং options জানার জন্য।

---

## Class-Based Views এর উদাহরণ

### উদাহরণ 1: Simple APIView

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})
    
    def post(self, request):
        name = request.data.get('name', 'Guest')
        return Response({'message': f'Hello, {name}!'})
```

### উদাহরণ 2: Authentication এবং Permissions সহ

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User

class ListUsersView(APIView):
    """
    View to list all users in the system.
    Requires token authentication.
    Only authenticated users can access this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response({
            'count': len(usernames),
            'users': usernames
        })
```

### উদাহরণ 3: Multiple HTTP Methods

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer

class ArticleDetailView(APIView):
    """
    Retrieve, update or delete an article instance.
    """
    
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return None
    
    def get(self, request, pk):
        article = self.get_object(pk)
        if article is None:
            return Response(
                {'error': 'Article not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        if article is None:
            return Response(
                {'error': 'Article not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        if article is None:
            return Response(
                {'error': 'Article not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### উদাহরণ 4: Custom Permissions

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners to edit an object.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only for owner
        return obj.owner == request.user

class ArticleView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request, pk):
        # Anyone can read
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk):
        # Only owner can update
        article = Article.objects.get(pk=pk)
        self.check_object_permissions(request, article)
        
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### উদাহরণ 5: Dynamic Permissions

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

class DynamicPermissionView(APIView):
    """
    Different permissions for different HTTP methods.
    """
    
    def get_permissions(self):
        if self.request.method == 'GET':
            # Anyone can read
            return [AllowAny()]
        else:
            # Only authenticated users can write
            return [IsAuthenticated()]
    
    def get(self, request):
        return Response({'message': 'Public data'})
    
    def post(self, request):
        return Response({'message': 'Protected data created'})
```

### উদাহরণ 6: File Upload

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        file = request.data.get('file')
        
        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            return Response(
                {'error': 'Only image files are allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save file
        # ... your file saving logic
        
        return Response({
            'message': 'File uploaded successfully',
            'filename': file.name,
            'size': file.size
        }, status=status.HTTP_201_CREATED)
```

---

## Function-Based Views (FBV)

যদিও class-based views বেশি powerful এবং reusable, তবুও simple endpoints এর জন্য function-based views ব্যবহার করা যেতে পারে।

### @api_view Decorator

`@api_view` decorator একটি function-based view কে DRF view এ convert করে।

**Signature:** `@api_view(http_method_names=['GET'])`

**Default:** শুধুমাত্র `GET` method allowed। অন্য methods `405 Method Not Allowed` return করবে।

**Basic উদাহরণ:**

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def hello_world(request):
    return Response({'message': 'Hello, world!'})
```

**Multiple Methods:**

```python
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### API Policy Decorators

Function-based views এর জন্য বিভিন্ন decorators available যা class-based views এর attributes এর equivalent।

**Available Decorators:**
- `@renderer_classes(...)`
- `@parser_classes(...)`
- `@authentication_classes(...)`
- `@throttle_classes(...)`
- `@permission_classes(...)`

**নোট:** এই decorators অবশ্যই `@api_view` এর পরে (নিচে) আসতে হবে।

**উদাহরণ:**

```python
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': f'Hello, {request.user.username}!'})
```

**Throttling উদাহরণ:**

```python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def limited_view(request):
    return Response({'message': 'Hello for today! See you tomorrow!'})
```

**Parser উদাহরণ:**

```python
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser

@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser])
def upload_data(request):
    data = request.data
    return Response({'received': data})
```

---

## CBV vs FBV - কখন কোনটি ব্যবহার করবেন?

### Class-Based Views (CBV) ব্যবহার করুন যখন:

1. **Complex Logic** - একাধিক HTTP methods handle করতে হবে
2. **Reusability** - একই logic বিভিন্ন views এ reuse করতে হবে
3. **Inheritance** - Base classes থেকে inherit করে functionality extend করতে হবে
4. **Mixins** - বিভিন্ন mixins compose করে functionality build করতে হবে
5. **Large Projects** - বড় এবং maintainable codebase তৈরি করতে হবে
6. **Built-in Features** - DRF এর built-in authentication, permissions ইত্যাদি সহজে ব্যবহার করতে হবে

**সুবিধা:**
- DRY principle follow করে
- Code organization ভালো
- Inheritance এবং mixins এর সুবিধা
- Built-in features সহজে integrate করা যায়

**অসুবিধা:**
- Learning curve বেশি
- Simple tasks এর জন্য overkill হতে পারে

### Function-Based Views (FBV) ব্যবহার করুন যখন:

1. **Simple Endpoints** - খুব simple logic, একটি বা দুটি HTTP method
2. **Quick Prototyping** - দ্রুত কিছু test করতে হবে
3. **One-off Views** - যে view reuse হবে না
4. **Explicit Control** - প্রতিটি step explicitly control করতে চান
5. **Learning** - DRF শিখছেন এবং simple approach চান

**সুবিধা:**
- সহজ এবং straightforward
- কম code
- Explicit এবং readable

**অসুবিধা:**
- Code duplication হতে পারে
- Complex logic handle করা কঠিন
- Reusability কম

### 2025/2026 এর Recommendation:

**বেশিরভাগ ক্ষেত্রে Class-Based Views ব্যবহার করুন** কারণ:
- Modern Django/DRF projects CBV prefer করে
- Better code organization এবং maintainability
- Team collaboration এ সুবিধা
- Large-scale applications এর জন্য উপযুক্ত

**Function-Based Views ব্যবহার করুন** শুধুমাত্র:
- Very simple endpoints এর জন্য
- Quick prototyping এর জন্য
- Learning phase এ

---

## Best Practices

### 1. Appropriate View Type নির্বাচন করুন

```python
# Simple endpoint - FBV ঠিক আছে
@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})

# Complex endpoint - CBV ব্যবহার করুন
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Complex logic
        pass
```

### 2. DRY Principle Follow করুন

```python
# Bad - Code duplication
class ArticleListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        # ... logic

class ArticleDetailView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        # ... logic

# Good - Use permission classes
class ArticleListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # ... logic

class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # ... logic
```

### 3. Helper Methods ব্যবহার করুন

```python
class ArticleView(APIView):
    def get_object(self, pk):
        """
        Helper method to get article or return None
        """
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return None
    
    def get(self, request, pk):
        article = self.get_object(pk)
        if article is None:
            return Response({'error': 'Not found'}, status=404)
        # ... rest of logic
```

### 4. Proper Status Codes ব্যবহার করুন

```python
from rest_framework import status

class ArticleView(APIView):
    def post(self, request):
        # Created - 201
        return Response(data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        # No Content - 204
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        # Not Found - 404
        if not article:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
```

### 5. Serializers ব্যবহার করুন Validation এর জন্য

```python
# Bad - Manual validation
class ArticleView(APIView):
    def post(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title required'}, status=400)
        # ... more validation

# Good - Use serializers
class ArticleView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

### 6. Dynamic Permissions ব্যবহার করুন

```python
class ArticleView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwner()]
        return [AllowAny()]
```

### 7. Docstrings লিখুন

```python
class ArticleListView(APIView):
    """
    API endpoint for listing and creating articles.
    
    GET: Returns a list of all articles
    POST: Creates a new article (requires authentication)
    """
    
    def get(self, request):
        """
        Return a list of all articles.
        """
        pass
    
    def post(self, request):
        """
        Create a new article.
        """
        pass
```

### 8. Exception Handling সঠিকভাবে করুন

```python
from rest_framework.exceptions import NotFound, ValidationError

class ArticleView(APIView):
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise NotFound('Article not found')
        
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
```

---

## সাধারণ ব্যবহারের উদাহরণ

### উদাহরণ 1: User Registration

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserRegistrationView(APIView):
    """
    User registration endpoint.
    """
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create user
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### উদাহরণ 2: User Login

```python
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserLoginView(APIView):
    """
    User login endpoint.
    """
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
```

### উদাহরণ 3: User Logout

```python
from rest_framework.permissions import IsAuthenticated

class UserLogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Delete user's token
        request.user.auth_token.delete()
        
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
```

### উদাহরণ 4: Search Endpoint

```python
from django.db.models import Q

class ArticleSearchView(APIView):
    """
    Search articles by title or content.
    """
    
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'Search query required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search in title and content
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
        serializer = ArticleSerializer(articles, many=True)
        
        return Response({
            'count': articles.count(),
            'results': serializer.data
        })
```

### উদাহরণ 5: Statistics Dashboard

```python
from django.db.models import Count
from rest_framework.permissions import IsAdminUser

class DashboardStatsView(APIView):
    """
    Dashboard statistics for admin users.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Aggregate data from multiple models
        stats = {
            'total_users': User.objects.count(),
            'total_articles': Article.objects.count(),
            'total_comments': Comment.objects.count(),
            'articles_by_category': list(
                Article.objects.values('category__name')
                .annotate(count=Count('id'))
            ),
            'recent_users': UserSerializer(
                User.objects.order_by('-date_joined')[:5],
                many=True
            ).data
        }
        
        return Response(stats)
```

### উদাহরণ 6: Bulk Operations

```python
class BulkArticleDeleteView(APIView):
    """
    Delete multiple articles at once.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        article_ids = request.data.get('ids', [])
        
        if not article_ids:
            return Response(
                {'error': 'No article IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete articles
        deleted_count, _ = Article.objects.filter(
            id__in=article_ids
        ).delete()
        
        return Response({
            'message': f'{deleted_count} articles deleted successfully',
            'deleted_count': deleted_count
        })
```

---

## Error Handling

### Built-in Exception Handling

DRF automatically handle করে:
- `APIException` এবং এর subclasses
- Django এর `Http404`
- Django এর `PermissionDenied`

### Custom Exception Handler

```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize error response
        response.data['status_code'] = response.status_code
        response.data['error'] = True
    
    return response
```

**settings.py তে configure করুন:**

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler'
}
```

### View-Level Exception Handling

```python
class ArticleView(APIView):
    def handle_exception(self, exc):
        # Custom exception handling for this view
        response = super().handle_exception(exc)
        
        if response is not None:
            response.data['view'] = 'ArticleView'
            response.data['timestamp'] = timezone.now()
        
        return response
    
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise NotFound('Article not found')
        
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
```

### Common Exceptions

```python
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
    PermissionDenied,
    AuthenticationFailed,
    NotAuthenticated,
    Throttled
)

class MyView(APIView):
    def get(self, request, pk):
        # 404 Not Found
        if not article:
            raise NotFound('Article not found')
        
        # 400 Bad Request
        if not valid:
            raise ValidationError('Invalid data')
        
        # 403 Forbidden
        if not has_permission:
            raise PermissionDenied('You do not have permission')
        
        # 401 Unauthorized
        if not authenticated:
            raise NotAuthenticated('Authentication required')
```

---

## অতিরিক্ত Resources

### Official Documentation
- Django REST Framework Views: https://www.django-rest-framework.org/api-guide/views/
- Classy Django REST Framework: http://www.cdrf.co (Interactive reference)
- Django REST Framework Tutorial: https://www.django-rest-framework.org/tutorial/

### সম্পর্কিত বিষয়
- Generic Views (পরবর্তী documentation এ)
- ViewSets (পরবর্তী documentation এ)
- Serializers
- Permissions
- Authentication
- Throttling

---

সর্বশেষ আপডেট: জানুয়ারি ২০২৬
