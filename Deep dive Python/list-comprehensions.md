# Python Deep Dive - List Comprehensions

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [List Comprehension কী এবং কেন?](#list-comprehension-কী-এবং-কেন)
3. [Basic Syntax](#basic-syntax)
4. [Conditional Comprehensions](#conditional-comprehensions)
5. [Nested Comprehensions](#nested-comprehensions)
6. [Dict এবং Set Comprehensions](#dict-এবং-set-comprehensions)
7. [Advanced Patterns](#advanced-patterns)
8. [Performance](#performance)
9. [Best Practices](#best-practices)

---

## পরিচিতি

List Comprehensions হলো Python এর একটি powerful feature যা lists তৈরি করা সহজ এবং readable করে।

### সমস্যা:

```python
# Traditional way - verbose!
squares = []
for x in range(10):
    squares.append(x ** 2)
```

### সমাধান:

```python
# List comprehension - concise!
squares = [x ** 2 for x in range(10)]
```

---

## List Comprehension কী এবং কেন?

### List Comprehension কী?

**সহজ ভাষায়:** List comprehension হলো একটি concise way to create lists।

**Syntax:**
```python
[expression for item in iterable]
```

### কেন List Comprehension ব্যবহার করবেন?

1. **Concise** - কম code, same result
2. **Readable** - একবার বুঝলে পড়তে সহজ
3. **Fast** - Traditional loops থেকে faster
4. **Pythonic** - Python এর idiomatic way

### Comparison:

```python
# Traditional loop - 4 lines
numbers = []
for x in range(10):
    if x % 2 == 0:
        numbers.append(x)

# List comprehension - 1 line!
numbers = [x for x in range(10) if x % 2 == 0]

# Both produce: [0, 2, 4, 6, 8]
```

### Real-World তুলনা:

```
Traditional Loop = Recipe Steps
1. নাও একটা bowl
2. প্রতিটা ingredient নাও
3. Process করো
4. Bowl এ রাখো

List Comprehension = One-Line Instruction
"সব ingredients নাও, process করো, bowl এ রাখো"
```

---

## Basic Syntax

### Simple List Comprehension:

```python
# Basic syntax
[expression for item in iterable]

# Example 1: Squares
squares = [x ** 2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# Example 2: Uppercase
words = ['hello', 'world', 'python']
upper_words = [word.upper() for word in words]
print(upper_words)  # ['HELLO', 'WORLD', 'PYTHON']

# Example 3: String lengths
lengths = [len(word) for word in words]
print(lengths)  # [5, 5, 6]
```

### কী হচ্ছে Step by Step:

```python
squares = [x ** 2 for x in range(5)]

# Equivalent to:
squares = []
for x in range(5):  # for x in range(5)
    squares.append(x ** 2)  # x ** 2

# Execution:
# x = 0 → 0 ** 2 = 0
# x = 1 → 1 ** 2 = 1
# x = 2 → 2 ** 2 = 4
# x = 3 → 3 ** 2 = 9
# x = 4 → 4 ** 2 = 16
# Result: [0, 1, 4, 9, 16]
```

### With Function Calls:

```python
# Apply function to each item
def double(x):
    return x * 2

numbers = [1, 2, 3, 4, 5]
doubled = [double(x) for x in numbers]
print(doubled)  # [2, 4, 6, 8, 10]

# Or use lambda
doubled = [(lambda x: x * 2)(x) for x in numbers]
```

---

## Conditional Comprehensions

### if Condition (Filter):

```python
# Syntax
[expression for item in iterable if condition]

# Example: Even numbers only
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# Example: Positive numbers only
numbers = [-2, -1, 0, 1, 2, 3]
positives = [x for x in numbers if x > 0]
print(positives)  # [1, 2, 3]

# Example: Long words only
words = ['hi', 'hello', 'hey', 'goodbye']
long_words = [word for word in words if len(word) > 3]
print(long_words)  # ['hello', 'goodbye']
```

### if-else (Transform):

```python
# Syntax
[expression_if_true if condition else expression_if_false for item in iterable]

# Example: Even/Odd labels
labels = ['even' if x % 2 == 0 else 'odd' for x in range(5)]
print(labels)  # ['even', 'odd', 'even', 'odd', 'even']

# Example: Positive/Negative/Zero
numbers = [-2, -1, 0, 1, 2]
signs = ['positive' if x > 0 else 'negative' if x < 0 else 'zero' 
         for x in numbers]
print(signs)  # ['negative', 'negative', 'zero', 'positive', 'positive']

# Example: Cap values
values = [1, 5, 10, 15, 20]
capped = [x if x <= 10 else 10 for x in values]
print(capped)  # [1, 5, 10, 10, 10]
```

### Multiple Conditions:

```python
# Multiple if conditions (AND)
numbers = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]
print(numbers)  # [0, 6, 12, 18] (divisible by both 2 and 3)

# Equivalent to:
numbers = [x for x in range(20) if x % 2 == 0 and x % 3 == 0]

# Complex conditions
words = ['hello', 'world', 'python', 'hi']
filtered = [word for word in words 
            if len(word) > 3 
            if word[0] in 'hp']
print(filtered)  # ['hello', 'python']
```

---

## Nested Comprehensions

### Nested Loops:

```python
# Syntax
[expression for item1 in iterable1 for item2 in iterable2]

# Example: Pairs
pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)
# [(0, 0), (0, 1), (0, 2), 
#  (1, 0), (1, 1), (1, 2), 
#  (2, 0), (2, 1), (2, 2)]

# Equivalent to:
pairs = []
for x in range(3):
    for y in range(3):
        pairs.append((x, y))
```

### কী হচ্ছে:

```python
[(x, y) for x in range(2) for y in range(3)]

# Execution order:
# x = 0:
#   y = 0 → (0, 0)
#   y = 1 → (0, 1)
#   y = 2 → (0, 2)
# x = 1:
#   y = 0 → (1, 0)
#   y = 1 → (1, 1)
#   y = 2 → (1, 2)

# Result: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
```

### Flattening Lists:

```python
# Nested list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten to single list
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalent to:
flat = []
for row in matrix:
    for num in row:
        flat.append(num)
```

### Matrix Operations:

```python
# Transpose matrix
matrix = [[1, 2, 3], [4, 5, 6]]

# Transpose
transposed = [[row[i] for row in matrix] for i in range(3)]
print(transposed)  # [[1, 4], [2, 5], [3, 6]]

# Create multiplication table
table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
for row in table:
    print(row)
# [1, 2, 3, 4, 5]
# [2, 4, 6, 8, 10]
# [3, 6, 9, 12, 15]
# [4, 8, 12, 16, 20]
# [5, 10, 15, 20, 25]
```

---

## Dict এবং Set Comprehensions

### Dictionary Comprehension:

```python
# Syntax
{key_expr: value_expr for item in iterable}

# Example 1: Square dictionary
squares = {x: x ** 2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Example 2: Swap keys and values
original = {'a': 1, 'b': 2, 'c': 3}
swapped = {v: k for k, v in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}

# Example 3: Filter dictionary
scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'David': 95}
high_scores = {name: score for name, score in scores.items() if score >= 90}
print(high_scores)  # {'Bob': 92, 'David': 95}

# Example 4: Transform values
prices = {'apple': 10, 'banana': 5, 'orange': 8}
discounted = {item: price * 0.9 for item, price in prices.items()}
print(discounted)  # {'apple': 9.0, 'banana': 4.5, 'orange': 7.2}
```

### Set Comprehension:

```python
# Syntax
{expression for item in iterable}

# Example 1: Unique squares
squares = {x ** 2 for x in range(-5, 6)}
print(squares)  # {0, 1, 4, 9, 16, 25} (duplicates removed!)

# Example 2: Unique first letters
words = ['hello', 'world', 'python', 'programming']
first_letters = {word[0] for word in words}
print(first_letters)  # {'h', 'w', 'p'}

# Example 3: Unique lengths
lengths = {len(word) for word in words}
print(lengths)  # {5, 6, 11}
```

---

## Advanced Patterns

### 1. Nested List Comprehension:

```python
# Create 2D matrix
matrix = [[i + j for j in range(3)] for i in range(3)]
print(matrix)
# [[0, 1, 2],
#  [1, 2, 3],
#  [2, 3, 4]]

# Filter 2D matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[num for num in row if num % 2 == 0] for row in matrix]
print(filtered)  # [[2], [4, 6], [8]]
```

### 2. Multiple Iterables (zip):

```python
# Combine two lists
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]

# Create dict
people = {name: age for name, age in zip(names, ages)}
print(people)  # {'Alice': 25, 'Bob': 30, 'Charlie': 35}

# Create tuples
pairs = [(name, age) for name, age in zip(names, ages)]
print(pairs)  # [('Alice', 25), ('Bob', 30), ('Charlie', 35)]
```

### 3. Conditional Expression in Key:

```python
# Different keys based on condition
numbers = [1, 2, 3, 4, 5]
categorized = {('even' if x % 2 == 0 else 'odd'): x for x in numbers}
print(categorized)  # {'odd': 5, 'even': 4} (last values win!)

# Better: Group by category
from collections import defaultdict
categorized = defaultdict(list)
[categorized['even' if x % 2 == 0 else 'odd'].append(x) for x in numbers]
print(dict(categorized))  # {'odd': [1, 3, 5], 'even': [2, 4]}
```

### 4. Walrus Operator (Python 3.8+):

```python
# Compute once, use multiple times
data = [1, 2, 3, 4, 5]

# Without walrus - computes twice
result = [y for x in data if (y := x ** 2) > 10]
print(result)  # [16, 25]

# Equivalent to:
result = []
for x in data:
    y = x ** 2
    if y > 10:
        result.append(y)
```

### 5. String Manipulation:

```python
# Remove vowels
text = "Hello World"
no_vowels = ''.join([char for char in text if char.lower() not in 'aeiou'])
print(no_vowels)  # "Hll Wrld"

# Extract digits
text = "abc123def456"
digits = ''.join([char for char in text if char.isdigit()])
print(digits)  # "123456"

# Title case each word
sentence = "hello world python"
title = ' '.join([word.capitalize() for word in sentence.split()])
print(title)  # "Hello World Python"
```

---

## Performance

### Speed Comparison:

```python
import time

# Method 1: List comprehension
start = time.time()
squares1 = [x ** 2 for x in range(1000000)]
time1 = time.time() - start
print(f"List comprehension: {time1:.4f}s")

# Method 2: Traditional loop
start = time.time()
squares2 = []
for x in range(1000000):
    squares2.append(x ** 2)
time2 = time.time() - start
print(f"Traditional loop: {time2:.4f}s")

# Method 3: map()
start = time.time()
squares3 = list(map(lambda x: x ** 2, range(1000000)))
time3 = time.time() - start
print(f"map(): {time3:.4f}s")

# List comprehension is usually fastest!
```

### Memory Consideration:

```python
# List comprehension - All in memory
squares_list = [x ** 2 for x in range(1000000)]
# Memory: ~8MB

# Generator expression - Lazy evaluation
squares_gen = (x ** 2 for x in range(1000000))
# Memory: ~100 bytes

# Use generator when:
# - Large dataset
# - Iterate once
# - Memory matters
```

---

## Best Practices

### 1. Keep It Simple:

```python
# Good - Simple and readable
evens = [x for x in range(10) if x % 2 == 0]

# Bad - Too complex
result = [x if x % 2 == 0 else y if y % 3 == 0 else z 
          for x in range(10) 
          for y in range(10) 
          for z in range(10) 
          if x + y + z < 15]
# Too hard to read! Use regular loop instead
```

### 2. Use Generator for Large Data:

```python
# Good - Generator for large data
sum_of_squares = sum(x ** 2 for x in range(1000000))

# Bad - List comprehension wastes memory
sum_of_squares = sum([x ** 2 for x in range(1000000)])
```

### 3. Don't Sacrifice Readability:

```python
# Good - Clear intent
positive_evens = [x for x in numbers if x > 0 if x % 2 == 0]

# Better - Even more clear
positive_evens = [x for x in numbers 
                  if x > 0 
                  if x % 2 == 0]

# Bad - Too clever
positive_evens = [x for x in numbers if x > 0 and not x & 1]
```

### 4. When NOT to Use:

```python
# Don't use for side effects
# Bad - List comprehension for side effects
[print(x) for x in range(10)]  # Creates unnecessary list!

# Good - Use regular loop
for x in range(10):
    print(x)

# Don't use for complex logic
# Bad - Too complex
result = [process(x) if condition1(x) else 
          transform(x) if condition2(x) else 
          default(x) 
          for x in data 
          if validate(x)]

# Good - Use regular loop with clear logic
result = []
for x in data:
    if not validate(x):
        continue
    
    if condition1(x):
        result.append(process(x))
    elif condition2(x):
        result.append(transform(x))
    else:
        result.append(default(x))
```

---

## Summary

### Quick Reference:

```python
# Basic
[x for x in iterable]

# With condition (filter)
[x for x in iterable if condition]

# With if-else (transform)
[x if condition else y for x in iterable]

# Nested loops
[x for item1 in iter1 for item2 in iter2]

# Dictionary
{k: v for item in iterable}

# Set
{x for x in iterable}

# Generator (not list!)
(x for x in iterable)
```

### Key Points:

- ✅ List comprehensions are concise and fast
- ✅ Use for simple transformations and filters
- ✅ `[...]` for lists, `{...}` for sets, `{k:v}` for dicts
- ✅ `(...)` creates generator, not list
- ✅ Keep comprehensions simple and readable
- ✅ Use regular loops for complex logic
- ✅ Use generators for large datasets
- ✅ Don't use for side effects

**List Comprehensions = Concise + Fast + Pythonic!** 🚀
