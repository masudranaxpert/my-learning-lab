# Django REST Framework ViewSet Cheatsheet (2026)

## কোন ViewSet কখন ব্যবহার করবো?

| ViewSet ক্লাস                  | কখন ব্যবহার করবো?                                      | CRUD অপারেশন পায়? | সবচেয়ে বেশি ব্যবহার হয়? |
|-------------------------------|----------------------------------------------------------|---------------------|---------------------------|
| `ViewSet`                     | সবকিছু নিজে হ্যান্ডেল করতে চাইলে (কাস্টম লজিক)            | না (নিজে লিখতে হয়) | খুব কম                    |
| `GenericViewSet`              | শুধু queryset + serializer দিয়ে শুরু করতে চাইলে         | না                  | মাঝে মাঝে                 |
| `ModelViewSet`                | পুরো CRUD (create, list, retrieve, update, destroy) চাই | হ্যাঁ (সব)          | **সবচেয়ে বেশি** (৮০% ক্ষেত্রে) |
| `ReadOnlyModelViewSet`        | শুধু GET (list + detail) চাই, কোনো write নয়              | শুধু read           | খুব ভালো (public API)     |

**সাজেশন (শুরুর জন্য):**  
প্রথমে সবসময় `ModelViewSet` দিয়ে শুরু করো। পরে দরকার হলে অন্য ক্লাসে চেঞ্জ করো।

## ModelViewSet এর ভেতরে মেইন attributes ও methods

| নাম                          | কী? (কাজ)                                                                 | ডিফল্ট আছে? | আমরা কীভাবে override করি?                              | কখন ব্যবহার করবো? |
|------------------------------|---------------------------------------------------------------------------|-------------|----------------------------------------------------------|---------------------|
| `queryset`                   | কোন ডাটা থেকে কাজ করবে (Model.objects.all())                              | না          | সরাসরি লিখি বা get_queryset() দিয়ে ডায়নামিক করি        | সবসময়              |
| `serializer_class`           | কোন সিরিয়ালাইজার ব্যবহার করবে                                           | না          | সরাসরি লিখি                                              | সবসময়              |
| `permission_classes`         | কে অ্যাক্সেস করতে পারবে? (IsAuthenticated, IsAdminUser ইত্যাদি)          | না          | লিস্ট দিয়ে দেই                                         | প্রায় সবসময়        |
| `authentication_classes`     | কীভাবে লগইন চেক করবে? (TokenAuthentication ইত্যাদি)                       | না          | লিস্ট দিয়ে দেই                                         | যদি auth লাগে       |
| `filterset_fields`           | কোন ফিল্ডে ?filter=value করা যাবে                                        | না          | লিস্ট দেই (django-filter লাগে)                           | search/filter চাইলে |
| `search_fields`              | ?search=keyword দিয়ে সার্চ করা যাবে                                      | না          | লিস্ট দেই                                               | সার্চ চাইলে         |
| `ordering_fields`            | ?ordering=name,-calories দিয়ে সর্ট করা যাবে                              | না          | লিস্ট দেই                                               | সর্ট চাইলে         |

### মেইন methods যেগুলো আমরা override করি (সবচেয়ে গুরুত্বপূর্ণ)

| মেথড নাম              | কখন কল হয়?                          | আমরা কী করি? (সাধারণ উদাহরণ)                                   | খুব বেশি ব্যবহার হয়? |
|-----------------------|---------------------------------------|------------------------------------------------------------------|-----------------------|
| `get_queryset()`      | প্রত্যেক GET/POST/PUT এর আগে          | user-এর ডাটা ফিল্টার করা (যেমন: filter(user=self.request.user)) | হ্যাঁ (খুব বেশি)      |
| `get_serializer_class()` | কোন সিরিয়ালাইজার ব্যবহার করবে তা ডিসাইড করতে | action অনুসারে আলাদা সিরিয়ালাইজার দেই (list vs detail)       | মাঝে মাঝে             |
| `perform_create()`    | POST (create) এর সময় সেভ করার আগে     | serializer.save(created_by=self.request.user)                   | হ্যাঁ (user অটো অ্যাড) |
| `perform_update()`    | PUT/PATCH এর সময় সেভ করার আগে         | অতিরিক্ত লজিক যোগ করা                                            | কম                    |
| `perform_destroy()`   | DELETE এর সময়                        | soft delete করা বা লগ করা                                        | কম                    |
| `list()` / `retrieve()` / `create()` ইত্যাদি | নিজে পুরো লজিক লিখতে চাইলে            | খুব কাস্টম ভিউ চাইলে override করি                               | খুব কম                |

### সবচেয়ে কমন override (৯০% প্রজেক্টে লাগে)

```python
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

<br>

<br>


```python
class MealViewSet(viewsets.ModelViewSet):
    """
    Production-ready Meal ViewSet Example
    Covers: Authentication, Pagination, Filtering, Search, Ordering, User-scoping
    """

    # মেইন সেটিংস
    serializer_class       = MealSerializer
    permission_classes     = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # অথবা Session + Token মিলিয়ে

    # ১. Pagination (খুব জরুরি – large data এর জন্য mandatory)
    pagination_class = PageNumberPagination   # অথবা LimitOffsetPagination / CursorPagination

    # ২. Filtering + Search + Ordering (এগুলো ছাড়া API অসম্পূর্ণ)
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = ['date', 'meal_type']          # ?date=2026-01-12
    search_fields    = ['note', 'items__food__name']  # ?search=ভাত
    ordering_fields  = ['date', 'created_at']         # ?ordering=-date
    ordering         = ['-date']                      # ডিফল্ট সর্ট

    # ৩. Lookup কাস্টম করা (UUID / slug চাইলে)
    # lookup_field = 'uuid'           # যদি pk এর বদলে uuid ব্যবহার করো
    # lookup_url_kwarg = 'uuid'       # URL-এ ?uuid=... হলে

    # ৪. Allowed HTTP methods (security hardening)
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    # ৫. queryset স্কোপ করা (সবচেয়ে গুরুত্বপূর্ণ)
    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user).order_by('-date')

    # ৬. Create-এ অটো user যোগ
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ৭. Update-এ অতিরিক্ত লজিক (যদি লাগে)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)  # optional

    # ৮. Custom actions – ViewSet এর আসল শক্তি
    @action(detail=False, methods=['get'], url_path='today')
    def today_meals(self, request):
        today = timezone.now().date()
        meals = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        meal = self.get_object()
        # এখানে MealItem যোগ করার লজিক
        return Response({"message": "Item added"})

    # ৯. Custom response (optional – আরো user-friendly)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            "status": "success",
            "count": response.data.get("count"),
            "results": response.data.get("results"),
            "message": "Meals fetched successfully"
        }
        return response
```
