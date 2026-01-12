# Python Deep Dive - Lambda Functions

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Lambda কী এবং কেন?](#lambda-কী-এবং-কেন)
3. [Basic Syntax](#basic-syntax)
4. [Lambda vs Regular Functions](#lambda-vs-regular-functions)
5. [Common Use Cases](#common-use-cases)
6. [Lambda with Built-in Functions](#lambda-with-built-in-functions)
7. [Limitations](#limitations)
8. [Best Practices](#best-practices)

---

## পরিচিতি

Lambda functions হলো Python এর anonymous (নামহীন) functions যা একটা line এ লেখা যায়।

### সহজ উদাহরণ:

```python
# Regular function
def square(x):
    return x ** 2

# Lambda function - same thing!
square = lambda x: x ** 2

print(square(5))  # 25
```

---

## Lambda কী এবং কেন?

### Lambda কী?

**সহজ ভাষায়:** Lambda হলো একটা ছোট anonymous function যা একটা line এ লেখা যায়।

**Syntax:**
```python
lambda arguments: expression
```

### কেন Lambda ব্যবহার করবেন?

1. **Concise** - ছোট functions এর জন্য perfect
2. **Anonymous** - নাম দেওয়ার দরকার নেই
3. **Inline** - যেখানে দরকার সেখানেই লিখুন
4. **Functional Programming** - map, filter, reduce এর সাথে ব্যবহার

### কখন ব্যবহার করবেন?

```python
# Good use - Simple, one-time function
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))

# Bad use - Complex logic (use regular function!)
# lambda x: x if x > 0 else -x if x < 0 else 0  # Too complex!
```

### Real-World তুলনা:

```
Regular Function = Named Tool
- Screwdriver নাম দিয়ে রাখা
- বারবার ব্যবহার করবেন

Lambda = Disposable Tool
- একবার ব্যবহার করবেন
- নাম দেওয়ার দরকার নেই
- কাজ শেষে ফেলে দিবেন
```

---

## Basic Syntax

### Simple Lambda:

```python
# Syntax
lambda arguments: expression

# Example 1: Single argument
square = lambda x: x ** 2
print(square(5))  # 25

# Example 2: Multiple arguments
add = lambda x, y: x + y
print(add(3, 4))  # 7

# Example 3: No arguments
greet = lambda: "Hello!"
print(greet())  # Hello!

# Example 4: Multiple arguments
multiply = lambda x, y, z: x * y * z
print(multiply(2, 3, 4))  # 24
```

### কী হচ্ছে:

```python
square = lambda x: x ** 2

# Equivalent to:
def square(x):
    return x ** 2

# Breakdown:
# lambda    → keyword
# x         → parameter
# :         → separator
# x ** 2    → expression (automatically returned)
```

### Immediate Execution:

```python
# Call lambda immediately
result = (lambda x: x ** 2)(5)
print(result)  # 25

# Multiple arguments
result = (lambda x, y: x + y)(3, 4)
print(result)  # 7

# Useful for one-time calculations
price_with_tax = (lambda price, tax: price * (1 + tax))(100, 0.15)
print(price_with_tax)  # 115.0
```

---

## Lambda vs Regular Functions

### Comparison:

```python
# Regular function
def add(x, y):
    return x + y

# Lambda function
add_lambda = lambda x, y: x + y

# Both work the same
print(add(3, 4))         # 7
print(add_lambda(3, 4))  # 7
```

### Differences:

| Feature | Regular Function | Lambda |
|---------|-----------------|--------|
| **Name** | Must have name | Anonymous |
| **Lines** | Multiple lines | Single line |
| **Statements** | Multiple statements | Single expression |
| **Annotations** | ✅ Yes | ❌ No |
| **Docstring** | ✅ Yes | ❌ No |
| **Complexity** | Any | Simple only |

### When to Use Each:

```python
# Use regular function when:
# - Complex logic
# - Multiple statements
# - Need docstring
# - Reuse multiple times

def calculate_discount(price, discount_percent):
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage
    
    Returns:
        Discounted price
    """
    if discount_percent > 100:
        raise ValueError("Discount cannot exceed 100%")
    
    discount = price * (discount_percent / 100)
    return price - discount

# Use lambda when:
# - Simple expression
# - One-time use
# - Inline with map/filter/sorted

# Good lambda use
sorted_prices = sorted(prices, key=lambda x: x['price'])
```

---

## Common Use Cases

### 1. Sorting:

```python
# Sort by custom key
students = [
    {'name': 'Alice', 'age': 25, 'grade': 85},
    {'name': 'Bob', 'age': 22, 'grade': 92},
    {'name': 'Charlie', 'age': 23, 'grade': 78}
]

# Sort by age
sorted_by_age = sorted(students, key=lambda x: x['age'])
print([s['name'] for s in sorted_by_age])  # ['Bob', 'Charlie', 'Alice']

# Sort by grade (descending)
sorted_by_grade = sorted(students, key=lambda x: x['grade'], reverse=True)
print([s['name'] for s in sorted_by_grade])  # ['Bob', 'Alice', 'Charlie']

# Sort by name length
words = ['python', 'is', 'awesome', 'language']
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)  # ['is', 'python', 'awesome', 'language']
```

### 2. Filtering:

```python
# Filter with condition
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# Numbers > 5
greater_than_5 = list(filter(lambda x: x > 5, numbers))
print(greater_than_5)  # [6, 7, 8, 9, 10]

# Strings longer than 3 characters
words = ['hi', 'hello', 'hey', 'goodbye']
long_words = list(filter(lambda x: len(x) > 3, words))
print(long_words)  # ['hello', 'goodbye']
```

### 3. Mapping:

```python
# Transform each element
numbers = [1, 2, 3, 4, 5]

# Square each number
squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

# Convert to strings
strings = list(map(lambda x: str(x), numbers))
print(strings)  # ['1', '2', '3', '4', '5']

# Multiple iterables
numbers1 = [1, 2, 3]
numbers2 = [4, 5, 6]
sums = list(map(lambda x, y: x + y, numbers1, numbers2))
print(sums)  # [5, 7, 9]
```

### 4. Default Arguments:

```python
# Lambda with default arguments
greet = lambda name="Guest": f"Hello, {name}!"
print(greet())        # Hello, Guest!
print(greet("John"))  # Hello, John!

# Multiple defaults
calculate = lambda x, y=10, z=5: x + y + z
print(calculate(1))        # 16 (1 + 10 + 5)
print(calculate(1, 2))     # 8 (1 + 2 + 5)
print(calculate(1, 2, 3))  # 6 (1 + 2 + 3)
```

---

## Lambda with Built-in Functions

### 1. map():

```python
# Apply function to each element
numbers = [1, 2, 3, 4, 5]

# Double each number
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10]

# Convert Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(fahrenheit)  # [32.0, 50.0, 68.0, 86.0, 104.0]
```

### 2. filter():

```python
# Filter elements
numbers = range(-5, 6)

# Positive numbers only
positives = list(filter(lambda x: x > 0, numbers))
print(positives)  # [1, 2, 3, 4, 5]

# Even numbers only
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [-4, -2, 0, 2, 4]
```

### 3. sorted():

```python
# Custom sorting
points = [(1, 2), (3, 1), (5, 4), (2, 3)]

# Sort by second element
sorted_points = sorted(points, key=lambda p: p[1])
print(sorted_points)  # [(3, 1), (1, 2), (2, 3), (5, 4)]

# Sort by distance from origin
sorted_by_distance = sorted(points, key=lambda p: p[0]**2 + p[1]**2)
print(sorted_by_distance)  # [(1, 2), (3, 1), (2, 3), (5, 4)]
```

### 4. reduce():

```python
from functools import reduce

# Reduce list to single value
numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# Product of all numbers
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120

# Find maximum
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(maximum)  # 5
```

### 5. max() / min():

```python
# Find max/min with custom key
students = [
    {'name': 'Alice', 'grade': 85},
    {'name': 'Bob', 'grade': 92},
    {'name': 'Charlie', 'grade': 78}
]

# Student with highest grade
top_student = max(students, key=lambda s: s['grade'])
print(top_student)  # {'name': 'Bob', 'grade': 92}

# Student with lowest grade
bottom_student = min(students, key=lambda s: s['grade'])
print(bottom_student)  # {'name': 'Charlie', 'grade': 78}
```

---

## Limitations

### 1. Single Expression Only:

```python
# ❌ Can't do this - multiple statements
# lambda x: 
#     y = x * 2
#     return y + 1

# ✅ Must be single expression
lambda x: (x * 2) + 1

# ❌ Can't use statements (if/for/while as statements)
# lambda x: if x > 0: return x

# ✅ Can use conditional expression
lambda x: x if x > 0 else 0
```

### 2. No Annotations:

```python
# ❌ Can't add type hints
# lambda x: int -> int: x ** 2

# ✅ Use regular function for type hints
def square(x: int) -> int:
    return x ** 2
```

### 3. No Docstring:

```python
# ❌ Can't add docstring
# lambda x: """Square a number""" x ** 2

# ✅ Use regular function for documentation
def square(x):
    """Square a number"""
    return x ** 2
```

### 4. Hard to Debug:

```python
# Lambda - hard to debug
result = (lambda x: x / 0)(5)  # Error: <lambda> in line X

# Regular function - clear error message
def divide_by_zero(x):
    return x / 0

result = divide_by_zero(5)  # Error: divide_by_zero in line X
```

---

## Best Practices

### 1. Keep It Simple:

```python
# Good - Simple expression
square = lambda x: x ** 2

# Bad - Too complex
complex_lambda = lambda x: x if x > 0 else -x if x < 0 else 0

# Better - Use regular function
def absolute_value(x):
    if x > 0:
        return x
    elif x < 0:
        return -x
    else:
        return 0
```

### 2. Use for Short-Lived Functions:

```python
# Good - One-time use with sorted
sorted_names = sorted(names, key=lambda x: x.lower())

# Bad - Reused multiple times (use regular function!)
process = lambda x: x.strip().lower().replace(' ', '_')
result1 = process(text1)
result2 = process(text2)
result3 = process(text3)

# Better
def process_text(text):
    return text.strip().lower().replace(' ', '_')
```

### 3. Don't Assign to Variable (Usually):

```python
# Bad - Defeats purpose of lambda
square = lambda x: x ** 2

# Good - Use def
def square(x):
    return x ** 2

# Exception - OK for very simple cases
# But regular function is still better
```

### 4. Prefer List Comprehension:

```python
# Bad - Lambda with map
squared = list(map(lambda x: x ** 2, numbers))

# Good - List comprehension (more Pythonic)
squared = [x ** 2 for x in numbers]

# Bad - Lambda with filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Good - List comprehension
evens = [x for x in numbers if x % 2 == 0]
```

### 5. Use When Appropriate:

```python
# Good use cases:
# 1. Sorting key
sorted(items, key=lambda x: x['price'])

# 2. max/min key
max(items, key=lambda x: x['value'])

# 3. Callback functions
button.on_click(lambda: print("Clicked!"))

# 4. Simple transformations with map/filter
list(map(lambda x: x * 2, numbers))
```

---

## Summary

### Quick Reference:

```python
# Basic syntax
lambda arguments: expression

# Examples
square = lambda x: x ** 2
add = lambda x, y: x + y
greet = lambda name="Guest": f"Hello, {name}!"

# Common uses
sorted(items, key=lambda x: x['key'])
list(map(lambda x: x * 2, numbers))
list(filter(lambda x: x > 0, numbers))
max(items, key=lambda x: x['value'])
```

### Key Points:

- ✅ Lambda = anonymous function
- ✅ Single expression only
- ✅ Perfect for simple, one-time functions
- ✅ Great with map, filter, sorted, max, min
- ✅ Keep it simple and readable
- ❌ No multiple statements
- ❌ No docstrings or annotations
- ❌ Don't use for complex logic
- ❌ Prefer list comprehensions when possible

**Lambda = Quick + Anonymous + Simple!** 🚀
