# Python Deep Dive - Decorators

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Decorator কী এবং কেন?](#decorator-কী-এবং-কেন)
3. [Function Basics - Prerequisites](#function-basics---prerequisites)
4. [Simple Decorator](#simple-decorator)
5. [Decorator কীভাবে কাজ করে](#decorator-কীভাবে-কাজ-করে)
6. [Decorators with Arguments](#decorators-with-arguments)
7. [Multiple Decorators](#multiple-decorators)
8. [Class Decorators](#class-decorators)
9. [Built-in Decorators](#built-in-decorators)
10. [Real-World Examples](#real-world-examples)
11. [Common Use Cases](#common-use-cases)
12. [Best Practices](#best-practices)

---

## শেখার ক্রম

### প্রথমে পড়ুন (অবশ্যই):

1. ⭐⭐⭐ **Decorator কী এবং কেন?**
2. ⭐⭐⭐ **Function Basics** - First-class functions
3. ⭐⭐⭐ **Simple Decorator** - Basic syntax
4. ⭐⭐⭐ **Decorator কীভাবে কাজ করে** - Step-by-step
5. ⭐⭐⭐ **Real-World Examples**

### এরপর পড়ুন (গুরুত্বপূর্ণ):

6. ⭐⭐ **Decorators with Arguments**
7. ⭐⭐ **Multiple Decorators**
8. ⭐⭐ **Built-in Decorators** - @property, @staticmethod
9. ⭐⭐ **Common Use Cases**

### শেষে পড়ুন (Advanced):

10. ⭐ **Class Decorators**
11. ⭐ **Advanced Patterns**

---

## পরিচিতি

Decorators হলো Python এর একটি powerful feature যা functions বা classes এর behavior modify করতে দেয়।

### সহজ উদাহরণ:

```python
# Without decorator
def greet():
    print("Hello!")

greet()  # Output: Hello!

# With decorator - adds extra functionality
@make_bold
def greet():
    print("Hello!")

greet()  # Output: **Hello!**
```

---

## Decorator কী এবং কেন?

### Decorator কী?

**সহজ ভাষায়:** Decorator হলো একটি function যা অন্য function কে modify করে নতুন functionality add করে।

**Technical:** Decorator হলো একটি callable (function বা class) যা অন্য function/class কে input হিসেবে নেয় এবং modified version return করে।

### কেন Decorator প্রয়োজন?

**সমস্যা:** একই code বারবার লিখতে হচ্ছে

```python
# Without decorator - Repeated code
def add(a, b):
    print("Function called")  # Logging
    result = a + b
    print("Function finished")  # Logging
    return result

def multiply(a, b):
    print("Function called")  # Same logging!
    result = a * b
    print("Function finished")  # Same logging!
    return result

def divide(a, b):
    print("Function called")  # Same logging again!
    result = a / b
    print("Function finished")  # Same logging again!
    return result
```

**সমাধান:** Decorator ব্যবহার করুন

```python
# With decorator - Write once, use everywhere!
def log_function(func):
    def wrapper(*args, **kwargs):
        print("Function called")
        result = func(*args, **kwargs)
        print("Function finished")
        return result
    return wrapper

@log_function
def add(a, b):
    return a + b

@log_function
def multiply(a, b):
    return a * b

@log_function
def divide(a, b):
    return a / b

# All functions now have logging!
add(2, 3)
# Output:
# Function called
# Function finished
```

### Decorator এর সুবিধা:

1. **Code Reusability** - একবার লিখুন, সবখানে ব্যবহার করুন
2. **Separation of Concerns** - Main logic আলাদা, extra functionality আলাদা
3. **Clean Code** - Function clean থাকে
4. **Easy to Maintain** - একজায়গায় change করলেই সব জায়গায় apply হয়

### Real-World তুলনা:

```
Decorator = Gift Wrapper

Original Function = Gift (মূল জিনিস)
Decorator = Wrapper (মোড়ক)

Gift wrapper জিনিসটা change করে না,
শুধু presentation সুন্দর করে।

তেমনি Decorator function এর core logic change করে না,
শুধু extra features add করে।
```

---

## Function Basics - Prerequisites

Decorator বুঝতে হলে আগে Python এর কিছু concepts জানতে হবে:

### 1. Functions are First-Class Objects

Python এ functions হলো objects - variables এ store করা যায়।

```python
# Function কে variable এ assign করা
def greet():
    return "Hello!"

# greet function কে say_hello variable এ assign
say_hello = greet

print(say_hello())  # Output: Hello!
print(greet())      # Output: Hello!

# উভয়ই same function!
```

### 2. Functions can be Passed as Arguments

Function কে অন্য function এর argument হিসেবে pass করা যায়।

```python
def greet():
    return "Hello!"

def call_function(func):
    # func parameter এ একটা function আসবে
    result = func()
    print(result)

# greet function কে argument হিসেবে pass করা
call_function(greet)  # Output: Hello!
```

### 3. Functions can Return Functions

Function অন্য function return করতে পারে।

```python
def create_greeter():
    def greet():
        return "Hello!"
    
    # Inner function return করছে
    return greet

# create_greeter() একটা function return করে
my_greeter = create_greeter()

# Returned function call করা
print(my_greeter())  # Output: Hello!
```

### 4. Nested Functions (Closures)

Function এর ভিতরে function তৈরি করা যায়।

```python
def outer_function(message):
    # Outer function এর parameter
    
    def inner_function():
        # Inner function outer এর variables access করতে পারে
        print(message)
    
    return inner_function

# Function তৈরি করা
say_hello = outer_function("Hello!")
say_goodbye = outer_function("Goodbye!")

say_hello()    # Output: Hello!
say_goodbye()  # Output: Goodbye!
```

**এই ৪টি concept বুঝলেই Decorator বুঝা সহজ!**

---

## Simple Decorator

### Basic Structure:

```python
def my_decorator(func):
    """
    Decorator function
    
    Parameters:
        func: The function to be decorated
    
    Returns:
        wrapper: Modified function
    """
    def wrapper():
        # Code before original function
        print("Before function call")
        
        # Call original function
        func()
        
        # Code after original function
        print("After function call")
    
    return wrapper

# Using decorator
@my_decorator
def say_hello():
    print("Hello!")

# Call decorated function
say_hello()

# Output:
# Before function call
# Hello!
# After function call
```

### কী হচ্ছে Step by Step:

```python
# Step 1: Define decorator
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

# Step 2: Define function
def say_hello():
    print("Hello!")

# Step 3: Apply decorator
say_hello = my_decorator(say_hello)

# এটাই হয় যখন আমরা @my_decorator লিখি!
```

### @ Syntax:

```python
# These two are EXACTLY the same:

# Method 1: Using @ syntax (Recommended)
@my_decorator
def say_hello():
    print("Hello!")

# Method 2: Manual decoration
def say_hello():
    print("Hello!")
say_hello = my_decorator(say_hello)
```

---

## Decorator কীভাবে কাজ করে

### Complete Flow:

```python
# Decorator definition
def my_decorator(func):
    print(f"Decorating {func.__name__}")
    
    def wrapper():
        print("Wrapper: Before")
        result = func()
        print("Wrapper: After")
        return result
    
    return wrapper

# Function definition with decorator
@my_decorator
def greet():
    print("Greet: Hello!")
    return "Done"

# Call the function
result = greet()
print(f"Result: {result}")
```

**কখন কী হচ্ছে:**

```
Step 1: Python sees @my_decorator
  ↓
Step 2: Python calls my_decorator(greet)
  → Decorator receives original greet function
  → Prints: "Decorating greet"
  → Creates wrapper function
  → Returns wrapper function
  ↓
Step 3: greet = wrapper (original greet replaced!)
  ↓
Step 4: When we call greet()
  → Actually calling wrapper()
  → Prints: "Wrapper: Before"
  → Calls original greet function
  → Prints: "Greet: Hello!"
  → Prints: "Wrapper: After"
  → Returns "Done"
  ↓
Step 5: Result printed
  → Prints: "Result: Done"
```

**Complete Output:**

```
Decorating greet
Wrapper: Before
Greet: Hello!
Wrapper: After
Result: Done
```

### Visual Representation:

```
Before Decoration:
greet() → "Hello!"

After Decoration:
greet() → wrapper() → Before → Original greet() → After
```

---

## Decorators with Arguments

### Problem: Function এর arguments handle করা

```python
# This won't work!
def my_decorator(func):
    def wrapper():  # No parameters!
        print("Before")
        func()  # Can't pass arguments!
        print("After")
    return wrapper

@my_decorator
def add(a, b):
    return a + b

add(2, 3)  # Error! wrapper() takes 0 arguments but 2 were given
```

### Solution: *args and **kwargs

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # *args = positional arguments (tuple)
        # **kwargs = keyword arguments (dict)
        print(f"Before - Args: {args}, Kwargs: {kwargs}")
        
        # Pass all arguments to original function
        result = func(*args, **kwargs)
        
        print(f"After - Result: {result}")
        return result
    
    return wrapper

@my_decorator
def add(a, b):
    return a + b

@my_decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Test
print(add(2, 3))
# Output:
# Before - Args: (2, 3), Kwargs: {}
# After - Result: 5
# 5

print(greet("John", greeting="Hi"))
# Output:
# Before - Args: ('John',), Kwargs: {'greeting': 'Hi'}
# After - Result: Hi, John!
# Hi, John!
```

### কী হচ্ছে:

```python
add(2, 3)
  ↓
wrapper(2, 3)
  → args = (2, 3)
  → kwargs = {}
  ↓
func(*args, **kwargs)
  → func(2, 3)
  → Original add(2, 3)
  → Returns 5
```

---

## Decorators with Parameters

Decorator নিজেই parameters নিতে পারে!

### Structure:

```python
def repeat(times):
    """
    Decorator factory - returns a decorator
    
    Parameters:
        times: How many times to repeat
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Usage
@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("John")
# Output:
# Hello, John!
# Hello, John!
# Hello, John!
```

### কী হচ্ছে:

```
Step 1: @repeat(times=3)
  → repeat(3) called
  → Returns decorator function
  ↓
Step 2: @decorator
  → decorator(greet) called
  → Returns wrapper function
  ↓
Step 3: greet = wrapper
  ↓
Step 4: greet("John")
  → wrapper("John") called
  → Loops 3 times
  → Each time calls original greet("John")
```

### Another Example: Timer Decorator

```python
import time

def timer(func):
    """Measure function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"{func.__name__} took {duration:.4f} seconds")
        return result
    
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    return "Done"

@timer
def fast_function():
    return sum(range(1000))

slow_function()
# Output: slow_function took 2.0001 seconds

fast_function()
# Output: fast_function took 0.0001 seconds
```

---

## Multiple Decorators

একটা function এ একাধিক decorators ব্যবহার করা যায়।

### Example:

```python
def bold(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"**{result}**"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"*{result}*"
    return wrapper

def underline(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"_{result}_"
    return wrapper

# Multiple decorators
@underline
@italic
@bold
def greet(name):
    return f"Hello, {name}"

print(greet("John"))
# Output: _***Hello, John**_*
```

### Execution Order:

```
Decorators are applied from bottom to top!

@underline        ← Applied last (3rd)
@italic           ← Applied second (2nd)
@bold             ← Applied first (1st)
def greet(name):
    return f"Hello, {name}"

Equivalent to:
greet = underline(italic(bold(greet)))
```

**Step by Step:**

```
1. bold(greet) → greet_bold
2. italic(greet_bold) → greet_italic
3. underline(greet_italic) → greet_final

When called:
greet("John")
  → underline wrapper
    → italic wrapper
      → bold wrapper
        → original greet("John") → "Hello, John"
      → bold result → "**Hello, John**"
    → italic result → "*Hello, John*"
  → underline result → "_*Hello, John*_"
```

---

## Class Decorators

Classes কেও decorate করা যায়!

### Example 1: Add Method to Class

```python
def add_str_method(cls):
    """Add __str__ method to class"""
    def __str__(self):
        return f"{cls.__name__} instance"
    
    cls.__str__ = __str__
    return cls

@add_str_method
class Person:
    def __init__(self, name):
        self.name = name

person = Person("John")
print(person)  # Output: Person instance
```

### Example 2: Singleton Pattern

```python
def singleton(cls):
    """Ensure only one instance of class exists"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Database initialized")

# Test
db1 = Database()  # Output: Database initialized
db2 = Database()  # No output (same instance!)

print(db1 is db2)  # Output: True
```

---

## Built-in Decorators

Python এর built-in decorators:

### 1. @property

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Get radius"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Set radius with validation"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self):
        """Calculate area (read-only)"""
        return 3.14159 * self._radius ** 2

# Usage
circle = Circle(5)
print(circle.radius)  # Output: 5
print(circle.area)    # Output: 78.53975

circle.radius = 10    # Setter called
print(circle.area)    # Output: 314.159

# circle.area = 100   # Error! No setter for area
```

### 2. @staticmethod

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        """Static method - no self parameter"""
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b

# Call without creating instance
print(MathUtils.add(2, 3))       # Output: 5
print(MathUtils.multiply(4, 5))  # Output: 20

# Can also call with instance
utils = MathUtils()
print(utils.add(10, 20))  # Output: 30
```

### 3. @classmethod

```python
class Person:
    count = 0
    
    def __init__(self, name):
        self.name = name
        Person.count += 1
    
    @classmethod
    def get_count(cls):
        """Class method - receives cls instead of self"""
        return cls.count
    
    @classmethod
    def create_anonymous(cls):
        """Factory method"""
        return cls("Anonymous")

# Usage
person1 = Person("John")
person2 = Person("Jane")

print(Person.get_count())  # Output: 2

anonymous = Person.create_anonymous()
print(anonymous.name)      # Output: Anonymous
print(Person.get_count())  # Output: 3
```

---

## Real-World Examples

### 1. Login Required Decorator (Django-style)

```python
def login_required(func):
    """Check if user is logged in"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {"error": "Please login first"}
        return func(request, *args, **kwargs)
    return wrapper

@login_required
def view_profile(request):
    return {"profile": request.user.profile}

@login_required
def delete_account(request):
    request.user.delete()
    return {"message": "Account deleted"}
```

### 2. Cache Decorator

```python
def cache(func):
    """Cache function results"""
    cached_results = {}
    
    def wrapper(*args):
        if args in cached_results:
            print(f"Cache hit for {args}")
            return cached_results[args]
        
        print(f"Cache miss for {args}")
        result = func(*args)
        cached_results[args] = result
        return result
    
    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))
# Output:
# Cache miss for (5,)
# Cache miss for (4,)
# Cache miss for (3,)
# Cache miss for (2,)
# Cache miss for (1,)
# Cache miss for (0,)
# Cache hit for (1,)
# Cache hit for (2,)
# Cache hit for (3,)
# 5
```

### 3. Retry Decorator

```python
import time

def retry(max_attempts=3, delay=1):
    """Retry function on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    print(f"Attempt {attempts} failed. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unreliable_api_call():
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("API Error")
    return "Success!"

# Will retry up to 3 times
result = unreliable_api_call()
```

### 4. Validation Decorator

```python
def validate_positive(func):
    """Validate that all arguments are positive"""
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Argument must be positive: {arg}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def calculate_area(length, width):
    return length * width

print(calculate_area(5, 10))   # Output: 50
# calculate_area(-5, 10)       # Error: Argument must be positive: -5
```

---

## Common Use Cases

### 1. Logging

```python
import logging

def log_calls(func):
    """Log function calls"""
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return wrapper
```

### 2. Authentication & Authorization

```python
def require_role(role):
    """Check user role"""
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.role != role:
                raise PermissionError(f"Requires {role} role")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_role("admin")
def delete_user(user, target_user_id):
    # Only admins can delete users
    pass
```

### 3. Rate Limiting

```python
import time

def rate_limit(max_calls, time_window):
    """Limit function calls"""
    calls = []
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            calls[:] = [call for call in calls if call > now - time_window]
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=3, time_window=60)
def api_call():
    return "API response"
```

### 4. Deprecation Warning

```python
import warnings

def deprecated(message="This function is deprecated"):
    """Mark function as deprecated"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated. {message}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@deprecated("Use new_function() instead")
def old_function():
    return "Old implementation"
```

---

## Best Practices

### 1. Use functools.wraps

```python
from functools import wraps

# Without functools.wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def greet():
    """Say hello"""
    pass

print(greet.__name__)  # Output: wrapper (Wrong!)
print(greet.__doc__)   # Output: None (Lost!)

# With functools.wraps
def good_decorator(func):
    @wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def greet():
    """Say hello"""
    pass

print(greet.__name__)  # Output: greet (Correct!)
print(greet.__doc__)   # Output: Say hello (Preserved!)
```

### 2. Keep Decorators Simple

```python
# Good - Simple and focused
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start}")
        return result
    return wrapper

# Bad - Too complex
def complex_decorator(func):
    # 50 lines of complex logic
    # Hard to understand and maintain
    pass
```

### 3. Document Your Decorators

```python
def my_decorator(func):
    """
    Short description of what decorator does.
    
    Args:
        func: Function to be decorated
    
    Returns:
        Decorated function
    
    Example:
        @my_decorator
        def my_function():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 4. Make Decorators Reusable

```python
# Good - Reusable
def validate_type(expected_type):
    def decorator(func):
        @wraps(func)
        def wrapper(value, *args, **kwargs):
            if not isinstance(value, expected_type):
                raise TypeError(f"Expected {expected_type}")
            return func(value, *args, **kwargs)
        return wrapper
    return decorator

@validate_type(int)
def process_number(n):
    return n * 2

@validate_type(str)
def process_string(s):
    return s.upper()
```

---

## Summary

### Decorator Cheat Sheet:

```python
# 1. Simple decorator
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

# 2. Decorator with parameters
def my_decorator(param):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use param
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 3. Class decorator
def class_decorator(cls):
    # Modify class
    return cls

# 4. Usage
@my_decorator
def function():
    pass

@my_decorator(param="value")
def function():
    pass

@class_decorator
class MyClass:
    pass
```

### Key Points:

- ✅ Decorators modify function behavior without changing code
- ✅ Use `@wraps` to preserve function metadata
- ✅ `*args, **kwargs` to handle any arguments
- ✅ Decorators execute at definition time, not call time
- ✅ Multiple decorators applied bottom to top
- ✅ Keep decorators simple and focused
- ✅ Document your decorators

**Decorators = Code reusability + Clean code + Powerful features!** 🚀
