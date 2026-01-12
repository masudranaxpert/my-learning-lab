# Python Deep Dive - Args and Kwargs

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Args এবং Kwargs কী?](#args-এবং-kwargs-কী)
3. [*args - Variable Positional Arguments](#args---variable-positional-arguments)
4. [**kwargs - Variable Keyword Arguments](#kwargs---variable-keyword-arguments)
5. [*args এবং **kwargs একসাথে](#args-এবং-kwargs-একসাথে)
6. [Parameter Order](#parameter-order)
7. [Unpacking with * and **](#unpacking-with--and-)
8. [Real-World Examples](#real-world-examples)
9. [Common Use Cases](#common-use-cases)
10. [Best Practices](#best-practices)

---

## পরিচিতি

`*args` এবং `**kwargs` Python এর powerful features যা functions কে flexible বানায়।

### সমস্যা:

```python
# Fixed parameters - Limited!
def add_two(a, b):
    return a + b

def add_three(a, b, c):
    return a + b + c

def add_four(a, b, c, d):
    return a + b + c + d

# প্রতিবার নতুন function লিখতে হচ্ছে!
```

### সমাধান:

```python
# Variable parameters - Flexible!
def add(*numbers):
    return sum(numbers)

# যতগুলো চান ততগুলো arguments!
print(add(1, 2))           # 3
print(add(1, 2, 3))        # 6
print(add(1, 2, 3, 4, 5))  # 15
```

---

## Args এবং Kwargs কী?

### *args (Arguments)

**কী:** Variable number of positional arguments

**সহজ ভাষায়:** যতগুলো চান ততগুলো arguments pass করতে পারবেন (tuple হিসেবে পাবেন)

```python
def my_function(*args):
    print(type(args))  # <class 'tuple'>
    print(args)

my_function(1, 2, 3, 4, 5)
# Output: (1, 2, 3, 4, 5)
```

### **kwargs (Keyword Arguments)

**কী:** Variable number of keyword arguments

**সহজ ভাষায়:** যতগুলো চান ততগুলো key=value arguments pass করতে পারবেন (dict হিসেবে পাবেন)

```python
def my_function(**kwargs):
    print(type(kwargs))  # <class 'dict'>
    print(kwargs)

my_function(name="John", age=25, city="Dhaka")
# Output: {'name': 'John', 'age': 25, 'city': 'Dhaka'}
```

### Real-World তুলনা:

```
*args = Buffet Restaurant
- যতটা চান ততটা নিতে পারেন
- Order: যেভাবে নিলেন সেভাবেই (position matters)

**kwargs = À la carte Menu
- যা চান তা order করতে পারেন
- Name দিয়ে order করেন (key=value)
```

---

## *args - Variable Positional Arguments

### Basic Usage:

```python
def greet(*names):
    """
    Greet multiple people
    
    *names becomes a tuple of all arguments
    """
    for name in names:
        print(f"Hello, {name}!")

# Call with any number of arguments
greet("John")
# Output: Hello, John!

greet("John", "Jane", "Bob")
# Output:
# Hello, John!
# Hello, Jane!
# Hello, Bob!

greet()  # No arguments - empty tuple
# No output
```

### কী হচ্ছে:

```python
def my_function(*args):
    print(args)

my_function(1, 2, 3)
# args = (1, 2, 3)  # Tuple!

my_function('a', 'b', 'c', 'd')
# args = ('a', 'b', 'c', 'd')

my_function()
# args = ()  # Empty tuple
```

### Accessing Args:

```python
def process_numbers(*numbers):
    print(f"Received {len(numbers)} numbers")
    
    # Access by index
    if numbers:
        print(f"First number: {numbers[0]}")
        print(f"Last number: {numbers[-1]}")
    
    # Iterate
    for i, num in enumerate(numbers):
        print(f"Number {i+1}: {num}")
    
    # Use tuple methods
    total = sum(numbers)
    print(f"Total: {total}")

process_numbers(10, 20, 30, 40)
# Output:
# Received 4 numbers
# First number: 10
# Last number: 40
# Number 1: 10
# Number 2: 20
# Number 3: 30
# Number 4: 40
# Total: 100
```

### Mixing Regular and *args:

```python
def create_user(username, *hobbies):
    """
    username: required
    *hobbies: optional, any number
    """
    print(f"Username: {username}")
    print(f"Hobbies: {', '.join(hobbies)}")

create_user("john", "coding", "reading", "gaming")
# Output:
# Username: john
# Hobbies: coding, reading, gaming

create_user("jane")
# Output:
# Username: jane
# Hobbies: 
```

---

## **kwargs - Variable Keyword Arguments

### Basic Usage:

```python
def create_profile(**info):
    """
    Create user profile with any fields
    
    **info becomes a dict of all keyword arguments
    """
    print("Profile Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

create_profile(name="John", age=25, city="Dhaka")
# Output:
# Profile Information:
# name: John
# age: 25
# city: Dhaka

create_profile(username="john123", email="john@example.com")
# Output:
# Profile Information:
# username: john123
# email: john@example.com
```

### কী হচ্ছে:

```python
def my_function(**kwargs):
    print(kwargs)

my_function(a=1, b=2, c=3)
# kwargs = {'a': 1, 'b': 2, 'c': 3}  # Dict!

my_function(name="John", age=25)
# kwargs = {'name': 'John', 'age': 25}

my_function()
# kwargs = {}  # Empty dict
```

### Accessing Kwargs:

```python
def process_config(**config):
    # Get with default value
    host = config.get('host', 'localhost')
    port = config.get('port', 8000)
    debug = config.get('debug', False)
    
    print(f"Server: {host}:{port}")
    print(f"Debug mode: {debug}")
    
    # Check if key exists
    if 'database' in config:
        print(f"Database: {config['database']}")

process_config(host="example.com", port=3000, debug=True)
# Output:
# Server: example.com:3000
# Debug mode: True

process_config()
# Output:
# Server: localhost:8000
# Debug mode: False
```

### Mixing Regular and **kwargs:

```python
def send_email(to, subject, **options):
    """
    to: required
    subject: required
    **options: optional settings
    """
    print(f"To: {to}")
    print(f"Subject: {subject}")
    
    # Optional settings
    cc = options.get('cc', [])
    bcc = options.get('bcc', [])
    priority = options.get('priority', 'normal')
    
    print(f"CC: {cc}")
    print(f"Priority: {priority}")

send_email(
    "john@example.com",
    "Hello",
    cc=["jane@example.com"],
    priority="high"
)
```

---

## *args এবং **kwargs একসাথে

### Both Together:

```python
def flexible_function(*args, **kwargs):
    """
    Accept any positional and keyword arguments
    """
    print("Positional arguments (args):")
    for arg in args:
        print(f"  - {arg}")
    
    print("\nKeyword arguments (kwargs):")
    for key, value in kwargs.items():
        print(f"  - {key}: {value}")

flexible_function(1, 2, 3, name="John", age=25)
# Output:
# Positional arguments (args):
#   - 1
#   - 2
#   - 3
#
# Keyword arguments (kwargs):
#   - name: John
#   - age: 25
```

### Real Example: Logger

```python
def log(level, *messages, **metadata):
    """
    Flexible logging function
    
    level: required (ERROR, WARNING, INFO)
    *messages: any number of messages
    **metadata: additional info (user, ip, etc.)
    """
    print(f"[{level}]", end=" ")
    print(" ".join(str(msg) for msg in messages))
    
    if metadata:
        print("Metadata:", metadata)

log("ERROR", "Database connection failed", "Retrying...", 
    user="john", attempt=3)
# Output:
# [ERROR] Database connection failed Retrying...
# Metadata: {'user': 'john', 'attempt': 3}

log("INFO", "Server started")
# Output:
# [INFO] Server started
```

---

## Parameter Order

**Important:** Parameters এর order ঠিক রাখতে হবে!

### Correct Order:

```python
def function(
    regular_param,           # 1. Regular positional
    *args,                   # 2. *args
    keyword_only_param,      # 3. Keyword-only
    **kwargs                 # 4. **kwargs
):
    pass

# Example
def create_user(
    username,                # Required positional
    *roles,                  # Variable positional
    email,                   # Keyword-only (required)
    active=True,             # Keyword-only (with default)
    **metadata               # Variable keyword
):
    print(f"Username: {username}")
    print(f"Roles: {roles}")
    print(f"Email: {email}")
    print(f"Active: {active}")
    print(f"Metadata: {metadata}")

# Usage
create_user(
    "john",                  # username
    "admin", "editor",       # roles
    email="john@example.com", # email (must use keyword!)
    active=True,
    department="IT",         # metadata
    location="Dhaka"
)
```

### Wrong Order (Error!):

```python
# ❌ Wrong - **kwargs before *args
def wrong_function(**kwargs, *args):
    pass
# SyntaxError!

# ❌ Wrong - regular param after *args
def wrong_function(*args, regular_param):
    pass
# This makes regular_param keyword-only!
```

---

## Unpacking with * and **

### Unpacking Lists/Tuples with *:

```python
def add(a, b, c):
    return a + b + c

# Without unpacking
numbers = [1, 2, 3]
result = add(numbers[0], numbers[1], numbers[2])  # Tedious!

# With unpacking
numbers = [1, 2, 3]
result = add(*numbers)  # Unpacks to add(1, 2, 3)
print(result)  # 6

# Works with tuples too
numbers = (10, 20, 30)
result = add(*numbers)
print(result)  # 60
```

### Unpacking Dicts with **:

```python
def create_user(name, age, city):
    print(f"{name}, {age}, {city}")

# Without unpacking
user_data = {'name': 'John', 'age': 25, 'city': 'Dhaka'}
create_user(user_data['name'], user_data['age'], user_data['city'])

# With unpacking
user_data = {'name': 'John', 'age': 25, 'city': 'Dhaka'}
create_user(**user_data)  # Unpacks to create_user(name='John', age=25, city='Dhaka')
```

### Combining Multiple Iterables:

```python
# Combining lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]
print(combined)  # [1, 2, 3, 4, 5, 6]

# Combining dicts
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
combined = {**dict1, **dict2}
print(combined)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Override values
dict1 = {'name': 'John', 'age': 25}
dict2 = {'age': 30, 'city': 'Dhaka'}  # age will override
combined = {**dict1, **dict2}
print(combined)  # {'name': 'John', 'age': 30, 'city': 'Dhaka'}
```

---

## Real-World Examples

### 1. Wrapper Functions

```python
def timer(func):
    """Decorator that times function execution"""
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        
        # Call original function with all arguments
        result = func(*args, **kwargs)
        
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    
    return wrapper

@timer
def process_data(data, *filters, verbose=False):
    # Process with any number of filters
    for f in filters:
        data = f(data)
    if verbose:
        print(f"Processed: {data}")
    return data
```

### 2. Configuration Builder

```python
class Config:
    def __init__(self, **settings):
        """Initialize with any settings"""
        self.settings = {
            'debug': False,
            'host': 'localhost',
            'port': 8000,
            **settings  # Override defaults
        }
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def update(self, **new_settings):
        """Update multiple settings"""
        self.settings.update(new_settings)

# Usage
config = Config(debug=True, port=3000)
print(config.get('debug'))  # True
print(config.get('host'))   # localhost (default)

config.update(host='example.com', timeout=30)
```

### 3. API Request Builder

```python
def api_request(endpoint, method='GET', **params):
    """
    Make API request with flexible parameters
    
    endpoint: required
    method: optional (default GET)
    **params: query parameters, headers, etc.
    """
    url = f"https://api.example.com/{endpoint}"
    
    # Extract specific params
    headers = params.pop('headers', {})
    timeout = params.pop('timeout', 30)
    
    # Remaining params become query string
    query_params = params
    
    print(f"{method} {url}")
    print(f"Headers: {headers}")
    print(f"Params: {query_params}")
    print(f"Timeout: {timeout}")

# Usage
api_request(
    'users',
    method='GET',
    page=1,
    limit=10,
    headers={'Authorization': 'Bearer token'},
    timeout=60
)
```

### 4. Database Query Builder

```python
class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self.conditions = []
    
    def where(self, **conditions):
        """Add WHERE conditions"""
        for key, value in conditions.items():
            self.conditions.append(f"{key} = '{value}'")
        return self
    
    def build(self):
        """Build SQL query"""
        query = f"SELECT * FROM {self.table}"
        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        return query

# Usage
query = QueryBuilder('users') \
    .where(age=25, city='Dhaka', active=True) \
    .build()

print(query)
# SELECT * FROM users WHERE age = '25' AND city = 'Dhaka' AND active = 'True'
```

---

## Common Use Cases

### 1. Extending Functions

```python
# Original function
def calculate_total(price, quantity):
    return price * quantity

# Extended version with optional parameters
def calculate_total_extended(price, quantity, **options):
    total = price * quantity
    
    # Optional: Apply discount
    if 'discount' in options:
        total *= (1 - options['discount'] / 100)
    
    # Optional: Add tax
    if 'tax' in options:
        total *= (1 + options['tax'] / 100)
    
    # Optional: Shipping
    if 'shipping' in options:
        total += options['shipping']
    
    return total

# Usage
print(calculate_total_extended(100, 2))  # 200
print(calculate_total_extended(100, 2, discount=10))  # 180
print(calculate_total_extended(100, 2, discount=10, tax=5))  # 189
print(calculate_total_extended(100, 2, discount=10, tax=5, shipping=20))  # 209
```

### 2. Logging

```python
def log(*messages, level='INFO', **context):
    """
    Flexible logging
    
    *messages: any number of messages
    level: log level
    **context: additional context (user, ip, etc.)
    """
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    message = ' '.join(str(msg) for msg in messages)
    
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    if context:
        context_str = ', '.join(f"{k}={v}" for k, v in context.items())
        log_entry += f" | {context_str}"
    
    print(log_entry)

# Usage
log("Server started")
# [2026-01-12 18:00:00] [INFO] Server started

log("User logged in", level='INFO', user='john', ip='192.168.1.1')
# [2026-01-12 18:00:00] [INFO] User logged in | user=john, ip=192.168.1.1

log("Database error", "Connection timeout", level='ERROR', retry=3)
# [2026-01-12 18:00:00] [ERROR] Database error Connection timeout | retry=3
```

### 3. Function Composition

```python
def compose(*functions):
    """
    Compose multiple functions
    
    compose(f, g, h)(x) = f(g(h(x)))
    """
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner

# Example functions
def add_10(x):
    return x + 10

def multiply_2(x):
    return x * 2

def square(x):
    return x ** 2

# Compose
pipeline = compose(add_10, multiply_2, square)

print(pipeline(3))
# square(3) = 9
# multiply_2(9) = 18
# add_10(18) = 28
```

---

## Best Practices

### 1. Use Descriptive Names

```python
# Good - Clear purpose
def create_user(*roles, **profile_data):
    pass

def send_notification(*recipients, **options):
    pass

# Bad - Not clear
def func(*args, **kwargs):
    pass
```

### 2. Document Your Functions

```python
def process_data(*data_sources, **processing_options):
    """
    Process data from multiple sources.
    
    Args:
        *data_sources: Variable number of data source paths
        **processing_options: Processing configuration
            - format (str): Output format ('json', 'csv')
            - validate (bool): Whether to validate data
            - verbose (bool): Print progress
    
    Returns:
        Processed data
    
    Example:
        process_data('file1.csv', 'file2.csv', 
                    format='json', validate=True)
    """
    pass
```

### 3. Validate Arguments

```python
def create_record(*fields, **metadata):
    """Create database record"""
    # Validate args
    if not fields:
        raise ValueError("At least one field required")
    
    # Validate kwargs
    required_keys = {'table', 'user_id'}
    if not required_keys.issubset(metadata.keys()):
        missing = required_keys - metadata.keys()
        raise ValueError(f"Missing required metadata: {missing}")
    
    # Process...
```

### 4. Don't Overuse

```python
# Good - Clear parameters
def create_user(username, email, password):
    pass

# Bad - Overusing kwargs when parameters are known
def create_user(**user_data):
    # Now you have to validate everything!
    pass

# Good use of kwargs - truly variable options
def create_user(username, email, password, **preferences):
    # preferences can be anything: theme, language, etc.
    pass
```

---

## Summary

### Quick Reference:

```python
# *args - Variable positional arguments (tuple)
def func(*args):
    for arg in args:
        print(arg)

func(1, 2, 3)  # args = (1, 2, 3)

# **kwargs - Variable keyword arguments (dict)
def func(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

func(a=1, b=2)  # kwargs = {'a': 1, 'b': 2}

# Both together
def func(*args, **kwargs):
    pass

func(1, 2, 3, a=4, b=5)
# args = (1, 2, 3)
# kwargs = {'a': 4, 'b': 5}

# Unpacking
numbers = [1, 2, 3]
func(*numbers)  # Same as func(1, 2, 3)

data = {'a': 1, 'b': 2}
func(**data)  # Same as func(a=1, b=2)
```

### Key Points:

- ✅ `*args` = tuple of positional arguments
- ✅ `**kwargs` = dict of keyword arguments
- ✅ Order matters: regular → *args → keyword-only → **kwargs
- ✅ Use `*` to unpack lists/tuples
- ✅ Use `**` to unpack dicts
- ✅ Great for flexible functions and decorators
- ✅ Document what arguments are expected
- ✅ Don't overuse - be explicit when possible

**Args & Kwargs = Flexible, powerful functions!** 🚀
