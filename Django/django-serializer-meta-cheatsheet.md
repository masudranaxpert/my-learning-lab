```python
class Meta:
```
| Meta Attribute | কাজ কী? (সংক্ষেপে) | সবচেয়ে বেশি ব্যবহার হয়? | উদাহরণ |
|---------------|-------------------|--------------------------|--------|
| model | এই সিরিয়ালাইজার কোন মডেলের জন্য | সব সিরিয়ালাইজারে বাধ্যতামূলক | `model = FoodItem` |
| fields | কোন কোন ফিল্ড সিরিয়ালাইজ করবে (লিস্ট বা `'__all__'`) | প্রায় সবসময় | `fields = ['id', 'name', 'calories_per_100g']` বা `'__all__'` |
| exclude | কোন ফিল্ডগুলো বাদ দিবে (fields-এর উল্টো) | কম | `exclude = ['created_by']` |
| read_only_fields | এই ফিল্ডগুলো শুধু পড়া যাবে (POST/PUT-এ পাঠানো যাবে না) | খুব বেশি | `read_only_fields = ['id', 'created_by', 'created_at']` |
| extra_kwargs | নির্দিষ্ট ফিল্ডের জন্য অতিরিক্ত অপশন (read_only, write_only, required ইত্যাদি) | মাঝে মাঝে | `extra_kwargs = {'password': {'write_only': True}}` |
| depth | ForeignKey / OneToOne / ManyToMany কত লেভেল পর্যন্ত nested দেখাবে | শুরুতে ১–২ লেভেল | `depth = 1` |
| validators | কাস্টম ভ্যালিডেটর লিস্ট যোগ করা | কম | `validators = [UniqueTogetherValidator(...)]` |
| list_serializer_class | লিস্ট ভিউ (`many=True`) এর জন্য আলাদা সিরিয়ালাইজার | খুব কম | `list_serializer_class = CustomListSerializer` |
| ordering | ডিফল্ট অর্ডারিং (অর্ডার ফিল্ড লিস্ট) | কম (DB ordering বেশি ব্যবহৃত) | `ordering = ['-created_at']` |
| ordering_fields | কোন ফিল্ডগুলোতে ordering allowed (`?ordering=`) | কম | `ordering_fields = ['name', 'calories_per_100g']` |
