# Python Deep Dive - Generators

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Generator কী এবং কেন?](#generator-কী-এবং-কেন)
3. [yield Keyword](#yield-keyword)
4. [Generator vs Regular Function](#generator-vs-regular-function)
5. [Generator Expressions](#generator-expressions)
6. [Generator Methods](#generator-methods)
7. [Real-World Examples](#real-world-examples)
8. [Memory Efficiency](#memory-efficiency)
9. [Best Practices](#best-practices)

---

## পরিচিতি

Generators হলো Python এর একটি powerful feature যা memory-efficient iteration করতে দেয়।

### সমস্যা:

```python
# Regular function - সব data memory তে রাখে
def get_numbers():
    numbers = []
    for i in range(1000000):
        numbers.append(i)
    return numbers  # 1 million numbers in memory!

# Memory: ~40MB!
numbers = get_numbers()
```

### সমাধান:

```python
# Generator - একবারে একটা value দেয়
def get_numbers():
    for i in range(1000000):
        yield i  # One at a time!

# Memory: ~100 bytes!
numbers = get_numbers()
```

---

## Generator কী এবং কেন?

### Generator কী?

**সহজ ভাষায়:** Generator হলো একটি special function যা values একবারে একটা করে produce করে, সব একসাথে না।

**Technical:** Generator হলো একটি iterator যা `yield` keyword ব্যবহার করে values generate করে।

### কেন Generator প্রয়োজন?

1. **Memory Efficiency** - সব data memory তে রাখতে হয় না
2. **Lazy Evaluation** - যখন দরকার তখন calculate হয়
3. **Infinite Sequences** - অসীম data handle করা যায়
4. **Performance** - Large datasets এর জন্য fast

### Real-World তুলনা:

```
Regular Function = Restaurant Buffet
- সব খাবার একসাথে table এ
- সব জায়গা নেয়
- অনেক waste হতে পারে

Generator = À la carte Service
- যখন order করবেন তখন তৈরি হবে
- কম জায়গা লাগে
- কোনো waste নেই
```

---

## yield Keyword

### Basic Usage:

```python
def simple_generator():
    """
    Generator function with yield
    """
    print("First yield")
    yield 1
    
    print("Second yield")
    yield 2
    
    print("Third yield")
    yield 3
    
    print("Generator finished")

# Create generator
gen = simple_generator()

# Get values one by one
print(next(gen))
# Output:
# First yield
# 1

print(next(gen))
# Output:
# Second yield
# 2

print(next(gen))
# Output:
# Third yield
# 3

print(next(gen))
# Output:
# Generator finished
# StopIteration error!
```

### কী হচ্ছে Step by Step:

```
1. gen = simple_generator()
   → Generator object তৈরি হলো
   → কোনো code execute হয়নি এখনো!
   
2. next(gen) - First call
   → Function শুরু হলো
   → "First yield" print হলো
   → yield 1 এ পৌঁছালো
   → 1 return করলো
   → Function pause হলো (state save হলো!)
   
3. next(gen) - Second call
   → Function resume হলো (যেখানে pause ছিল)
   → "Second yield" print হলো
   → yield 2 এ পৌঁছালো
   → 2 return করলো
   → আবার pause
   
4. next(gen) - Third call
   → Resume
   → "Third yield" print হলো
   → yield 3
   → 3 return করলো
   → Pause
   
5. next(gen) - Fourth call
   → Resume
   → "Generator finished" print হলো
   → Function শেষ
   → StopIteration exception raise হলো
```

### yield vs return:

```python
# return - function শেষ হয়ে যায়
def with_return():
    return 1
    return 2  # Never executed!
    return 3  # Never executed!

print(with_return())  # Output: 1

# yield - function pause হয়, শেষ হয় না
def with_yield():
    yield 1
    yield 2
    yield 3

gen = with_yield()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

---

## Generator vs Regular Function

### Comparison:

```python
# Regular Function
def regular_squares(n):
    """
    Returns list of squares
    Memory: O(n)
    """
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# Generator Function
def generator_squares(n):
    """
    Yields squares one by one
    Memory: O(1)
    """
    for i in range(n):
        yield i ** 2

# Usage
# Regular - সব memory তে
squares_list = regular_squares(1000000)
print(type(squares_list))  # <class 'list'>
print(len(squares_list))   # 1000000
# Memory: ~40MB

# Generator - একবারে একটা
squares_gen = generator_squares(1000000)
print(type(squares_gen))   # <class 'generator'>
# print(len(squares_gen))  # Error! Generators don't have length
# Memory: ~100 bytes

# Iterate
for square in squares_gen:
    print(square)  # One at a time
```

### Performance Comparison:

```python
import time
import sys

# Regular function
def regular_range(n):
    return list(range(n))

# Generator function
def generator_range(n):
    for i in range(n):
        yield i

n = 1000000

# Memory usage
regular = regular_range(n)
print(f"List size: {sys.getsizeof(regular)} bytes")
# Output: List size: ~8000000 bytes (8MB)

gen = generator_range(n)
print(f"Generator size: {sys.getsizeof(gen)} bytes")
# Output: Generator size: ~112 bytes

# Time comparison
start = time.time()
regular = regular_range(n)
print(f"List creation: {time.time() - start:.4f}s")

start = time.time()
gen = generator_range(n)
print(f"Generator creation: {time.time() - start:.4f}s")
# Generator creation: Almost instant!
```

---

## Generator Expressions

List comprehension এর মতো, কিন্তু generator তৈরি করে।

### Syntax:

```python
# List comprehension - [] brackets
squares_list = [x**2 for x in range(10)]
print(type(squares_list))  # <class 'list'>
print(squares_list)        # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Generator expression - () parentheses
squares_gen = (x**2 for x in range(10))
print(type(squares_gen))   # <class 'generator'>
print(squares_gen)         # <generator object>

# Iterate
for square in squares_gen:
    print(square)
```

### Memory Comparison:

```python
import sys

# List comprehension
list_comp = [x for x in range(1000000)]
print(f"List: {sys.getsizeof(list_comp)} bytes")
# Output: ~8MB

# Generator expression
gen_exp = (x for x in range(1000000))
print(f"Generator: {sys.getsizeof(gen_exp)} bytes")
# Output: ~112 bytes
```

### When to Use:

```python
# Use list comprehension when:
# - Need to access multiple times
# - Need length
# - Need indexing
numbers = [x for x in range(10)]
print(numbers[5])  # Indexing works
print(len(numbers))  # Length works

# Use generator expression when:
# - Iterate once
# - Large dataset
# - Memory matters
numbers = (x for x in range(1000000))
total = sum(numbers)  # Iterate once
# numbers is now exhausted!
```

---

## Generator Methods

### 1. send() - Send value to generator

```python
def echo_generator():
    """Generator that echoes sent values"""
    while True:
        received = yield
        print(f"Received: {received}")

gen = echo_generator()
next(gen)  # Prime the generator

gen.send("Hello")  # Output: Received: Hello
gen.send("World")  # Output: Received: World
```

### 2. close() - Stop generator

```python
def infinite_counter():
    """Infinite counter"""
    count = 0
    while True:
        yield count
        count += 1

gen = infinite_counter()
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2

gen.close()  # Stop generator
# print(next(gen))  # Error! StopIteration
```

### 3. throw() - Throw exception

```python
def resilient_generator():
    """Handle exceptions"""
    try:
        yield 1
        yield 2
        yield 3
    except ValueError:
        yield "Error handled!"

gen = resilient_generator()
print(next(gen))  # 1
print(gen.throw(ValueError))  # Error handled!
```

---

## Real-World Examples

### 1. File Reading (Large Files)

```python
def read_large_file(file_path):
    """
    Read large file line by line
    Memory efficient!
    """
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Usage
for line in read_large_file('huge_file.txt'):
    process(line)  # Process one line at a time
    # Memory: Only one line at a time!
```

### 2. Fibonacci Sequence

```python
def fibonacci(n):
    """
    Generate first n Fibonacci numbers
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Usage
for num in fibonacci(10):
    print(num)
# Output: 0 1 1 2 3 5 8 13 21 34
```

### 3. Infinite Sequences

```python
def infinite_sequence():
    """
    Infinite number generator
    """
    num = 0
    while True:
        yield num
        num += 1

# Usage
gen = infinite_sequence()
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2
# ... can go forever!
```

### 4. Data Pipeline

```python
def read_data(filename):
    """Step 1: Read data"""
    with open(filename) as f:
        for line in f:
            yield line

def parse_data(lines):
    """Step 2: Parse data"""
    for line in lines:
        yield line.strip().split(',')

def filter_data(rows):
    """Step 3: Filter data"""
    for row in rows:
        if len(row) > 2:
            yield row

def process_data(rows):
    """Step 4: Process data"""
    for row in rows:
        yield {'name': row[0], 'age': int(row[1])}

# Pipeline - memory efficient!
pipeline = process_data(
    filter_data(
        parse_data(
            read_data('data.csv')
        )
    )
)

for item in pipeline:
    print(item)
# Only one item in memory at a time!
```

### 5. Batch Processing

```python
def batch_generator(data, batch_size):
    """
    Generate batches of data
    """
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

# Usage
data = list(range(100))
for batch in batch_generator(data, 10):
    process_batch(batch)  # Process 10 items at a time
```

---

## Memory Efficiency

### Example: Processing Large Dataset

```python
# Bad - Loads everything in memory
def process_all_at_once(filename):
    with open(filename) as f:
        lines = f.readlines()  # All lines in memory!
    
    processed = []
    for line in lines:
        processed.append(process(line))
    
    return processed

# Good - Generator approach
def process_with_generator(filename):
    with open(filename) as f:
        for line in f:  # One line at a time
            yield process(line)

# Usage
# Bad
results = process_all_at_once('huge_file.txt')
# Memory: Entire file + processed data

# Good
results = process_with_generator('huge_file.txt')
for result in results:
    save(result)  # Process and save one by one
# Memory: Only one line at a time!
```

### Chaining Generators:

```python
def numbers():
    """Generate numbers"""
    for i in range(1000000):
        yield i

def squares(nums):
    """Square each number"""
    for num in nums:
        yield num ** 2

def even_only(nums):
    """Filter even numbers"""
    for num in nums:
        if num % 2 == 0:
            yield num

# Chain generators - memory efficient!
result = even_only(squares(numbers()))

# Only one number processed at a time!
for num in result:
    print(num)
```

---

## Best Practices

### 1. Use Generators for Large Data

```python
# Good - Generator
def get_users():
    for user in User.objects.all():
        yield user

# Bad - List (if many users)
def get_users():
    return list(User.objects.all())
```

### 2. Generator Expressions for Simple Cases

```python
# Good - Generator expression
sum_of_squares = sum(x**2 for x in range(1000000))

# Bad - List comprehension (wastes memory)
sum_of_squares = sum([x**2 for x in range(1000000)])
```

### 3. Document Generator Behavior

```python
def my_generator(n):
    """
    Generate squares of numbers.
    
    Args:
        n: Number of values to generate
    
    Yields:
        int: Square of each number
    
    Example:
        >>> for num in my_generator(3):
        ...     print(num)
        0
        1
        4
    """
    for i in range(n):
        yield i ** 2
```

### 4. Handle StopIteration

```python
# Good - Use for loop (handles StopIteration)
gen = my_generator()
for value in gen:
    print(value)

# Bad - Manual next() without handling
gen = my_generator()
print(next(gen))
print(next(gen))
# ... might raise StopIteration!
```

---

## Summary

### Quick Reference:

```python
# Generator function
def my_generator():
    yield 1
    yield 2
    yield 3

# Generator expression
gen = (x**2 for x in range(10))

# Usage
gen = my_generator()
print(next(gen))  # 1
print(next(gen))  # 2

# Or iterate
for value in my_generator():
    print(value)
```

### Key Points:

- ✅ Generators use `yield` instead of `return`
- ✅ Memory efficient - values generated on demand
- ✅ Can only iterate once (unless recreated)
- ✅ Perfect for large datasets
- ✅ Use `()` for generator expressions
- ✅ Use `[]` for list comprehensions
- ✅ Generators are lazy - computed when needed
- ✅ Can represent infinite sequences

**Generators = Memory efficient + Lazy evaluation!** 🚀
