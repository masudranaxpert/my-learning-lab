# Python Deep Dive - Iterators

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Iterator কী এবং কেন?](#iterator-কী-এবং-কেন)
3. [Iterable vs Iterator](#iterable-vs-iterator)
4. [__iter__ এবং __next__](#__iter__-এবং-__next__)
5. [Creating Custom Iterators](#creating-custom-iterators)
6. [Iterator Protocol](#iterator-protocol)
7. [Real-World Examples](#real-world-examples)
8. [Best Practices](#best-practices)

---

## পরিচিতি

Iterators হলো Python এর একটি fundamental concept যা sequential data access করতে দেয়।

### সহজ উদাহরণ:

```python
# List হলো iterable
numbers = [1, 2, 3, 4, 5]

# for loop internally iterator ব্যবহার করে
for num in numbers:
    print(num)

# এটাই হচ্ছে internally:
iterator = iter(numbers)  # Get iterator
while True:
    try:
        num = next(iterator)  # Get next item
        print(num)
    except StopIteration:
        break  # No more items
```

---

## Iterator কী এবং কেন?

### Iterator কী?

**সহজ ভাষায়:** Iterator হলো একটি object যা একবারে একটা করে value দেয়।

**Technical:** Iterator হলো একটি object যার `__iter__()` এবং `__next__()` methods আছে।

### Iterable কী?

**Iterable:** যে object থেকে iterator পাওয়া যায়।

```python
# Iterables (iterator পাওয়া যায়)
numbers = [1, 2, 3]      # List
text = "hello"           # String
data = (1, 2, 3)        # Tuple
items = {1, 2, 3}       # Set
pairs = {'a': 1, 'b': 2} # Dict

# সবগুলো থেকে iterator পাওয়া যায়
iterator = iter(numbers)
```

### কেন Iterator প্রয়োজন?

1. **Memory Efficiency** - সব data একসাথে memory তে রাখতে হয় না
2. **Lazy Evaluation** - যখন দরকার তখন compute হয়
3. **Uniform Interface** - সব sequential data একইভাবে access করা যায়
4. **Infinite Sequences** - অসীম data represent করা যায়

### Real-World তুলনা:

```
Iterator = Playlist

Playlist (Iterable):
- গানের list আছে
- যেকোনো গান play করা যায়

Current Song (Iterator):
- এখন যে গান play হচ্ছে
- Next button → পরের গান
- শেষ হলে stop
```

---

## Iterable vs Iterator

### পার্থক্য:

```python
# Iterable - যেখান থেকে iterator পাওয়া যায়
numbers = [1, 2, 3, 4, 5]  # List is iterable

# Iterator - যা একবারে একটা value দেয়
iterator = iter(numbers)   # Get iterator from iterable

# Iterable: বারবার iterate করা যায়
for num in numbers:
    print(num)  # Works

for num in numbers:
    print(num)  # Works again!

# Iterator: শুধু একবার iterate করা যায়
for num in iterator:
    print(num)  # Works

for num in iterator:
    print(num)  # Nothing! Iterator exhausted
```

### Comparison Table:

| Feature | Iterable | Iterator |
|---------|----------|----------|
| **Definition** | যেখান থেকে iterator পাওয়া যায় | যা values দেয় |
| **Methods** | `__iter__()` | `__iter__()` + `__next__()` |
| **Reusable** | ✅ Yes | ❌ No (exhausted after use) |
| **Examples** | list, tuple, string, dict | iter(list), generator |
| **Memory** | সব data থাকে | একবারে একটা |

### কী হচ্ছে:

```python
# Iterable
numbers = [1, 2, 3]

# Get iterator
iterator = iter(numbers)  # Calls numbers.__iter__()

# Get values
print(next(iterator))  # Calls iterator.__next__() → 1
print(next(iterator))  # Calls iterator.__next__() → 2
print(next(iterator))  # Calls iterator.__next__() → 3
print(next(iterator))  # Calls iterator.__next__() → StopIteration!
```

---

## __iter__ এবং __next__

### Iterator Protocol:

```python
class MyIterator:
    """
    Custom iterator example
    """
    
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        """
        Return iterator object (self)
        
        কখন call হয়: iter(obj) বা for loop শুরুতে
        Return: Iterator object (usually self)
        """
        return self
    
    def __next__(self):
        """
        Return next value
        
        কখন call হয়: next(obj) বা for loop এ
        Return: Next value
        Raises: StopIteration when done
        """
        if self.current < self.max_num:
            self.current += 1
            return self.current
        else:
            raise StopIteration

# Usage
iterator = MyIterator(3)

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
# print(next(iterator))  # StopIteration!

# Or use for loop
iterator = MyIterator(3)
for num in iterator:
    print(num)
# Output: 1, 2, 3
```

### কী হচ্ছে Step by Step:

```
1. iterator = MyIterator(3)
   → Object তৈরি হলো
   → max_num = 3, current = 0

2. for num in iterator:
   → iter(iterator) call হয়
   → __iter__() call হয়
   → self return হয়

3. First iteration:
   → next(iterator) call হয়
   → __next__() call হয়
   → current < max_num? Yes (0 < 3)
   → current = 1
   → Return 1

4. Second iteration:
   → __next__() call হয়
   → current < max_num? Yes (1 < 3)
   → current = 2
   → Return 2

5. Third iteration:
   → __next__() call হয়
   → current < max_num? Yes (2 < 3)
   → current = 3
   → Return 3

6. Fourth iteration:
   → __next__() call হয়
   → current < max_num? No (3 < 3 is False)
   → raise StopIteration
   → Loop ends
```

---

## Creating Custom Iterators

### Example 1: Range Iterator

```python
class MyRange:
    """
    Custom range implementation
    """
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
    
    def __iter__(self):
        """Return iterator (self)"""
        return self
    
    def __next__(self):
        """Return next number"""
        if self.current < self.end:
            num = self.current
            self.current += 1
            return num
        else:
            raise StopIteration

# Usage
for num in MyRange(1, 5):
    print(num)
# Output: 1, 2, 3, 4
```

### Example 2: Reverse Iterator

```python
class ReverseIterator:
    """
    Iterate in reverse order
    """
    
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index > 0:
            self.index -= 1
            return self.data[self.index]
        else:
            raise StopIteration

# Usage
numbers = [1, 2, 3, 4, 5]
for num in ReverseIterator(numbers):
    print(num)
# Output: 5, 4, 3, 2, 1
```

### Example 3: Fibonacci Iterator

```python
class Fibonacci:
    """
    Generate Fibonacci numbers
    """
    
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count < self.max_count:
            self.count += 1
            
            # Current value
            current = self.a
            
            # Update for next iteration
            self.a, self.b = self.b, self.a + self.b
            
            return current
        else:
            raise StopIteration

# Usage
for num in Fibonacci(10):
    print(num)
# Output: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

---

## Iterator Protocol

### Iterable Class (Separate Iterator):

```python
class MyList:
    """
    Iterable class (not iterator itself)
    """
    
    def __init__(self, data):
        self.data = data
    
    def __iter__(self):
        """Return a NEW iterator each time"""
        return MyListIterator(self.data)

class MyListIterator:
    """
    Iterator class
    """
    
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

# Usage
my_list = MyList([1, 2, 3])

# Can iterate multiple times!
for num in my_list:
    print(num)  # 1, 2, 3

for num in my_list:
    print(num)  # 1, 2, 3 (works again!)
```

### কেন Separate Iterator?

```python
# With separate iterator - Reusable!
my_list = MyList([1, 2, 3])

iter1 = iter(my_list)  # New iterator
iter2 = iter(my_list)  # Another new iterator

print(next(iter1))  # 1
print(next(iter2))  # 1 (independent!)
print(next(iter1))  # 2
print(next(iter2))  # 2

# Without separate iterator - Not reusable!
class BadIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self  # Returns same object!
    
    def __next__(self):
        # ... same as before

bad = BadIterator([1, 2, 3])
for num in bad:
    print(num)  # Works

for num in bad:
    print(num)  # Nothing! Already exhausted
```

---

## Real-World Examples

### 1. File Line Iterator:

```python
class FileLineIterator:
    """
    Iterate over file lines
    """
    
    def __init__(self, filename):
        self.filename = filename
        self.file = None
    
    def __iter__(self):
        self.file = open(self.filename, 'r')
        return self
    
    def __next__(self):
        line = self.file.readline()
        if line:
            return line.strip()
        else:
            self.file.close()
            raise StopIteration

# Usage
for line in FileLineIterator('data.txt'):
    print(line)
```

### 2. Batch Iterator:

```python
class BatchIterator:
    """
    Iterate in batches
    """
    
    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            batch = self.data[self.index:self.index + self.batch_size]
            self.index += self.batch_size
            return batch
        else:
            raise StopIteration

# Usage
data = list(range(10))
for batch in BatchIterator(data, 3):
    print(batch)
# Output:
# [0, 1, 2]
# [3, 4, 5]
# [6, 7, 8]
# [9]
```

### 3. Infinite Counter:

```python
class InfiniteCounter:
    """
    Count infinitely
    """
    
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = self.current
        self.current += self.step
        return value

# Usage (be careful - infinite!)
counter = InfiniteCounter(1, 2)
for i, num in enumerate(counter):
    if i >= 5:
        break
    print(num)
# Output: 1, 3, 5, 7, 9
```

### 4. Cycle Iterator:

```python
class Cycle:
    """
    Cycle through items infinitely
    """
    
    def __init__(self, items):
        self.items = items
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.items:
            raise StopIteration
        
        value = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return value

# Usage
colors = Cycle(['red', 'green', 'blue'])
for i, color in enumerate(colors):
    if i >= 7:
        break
    print(color)
# Output: red, green, blue, red, green, blue, red
```

---

## Best Practices

### 1. Implement Both __iter__ and __next__:

```python
# Good - Complete iterator
class GoodIterator:
    def __iter__(self):
        return self
    
    def __next__(self):
        # Implementation
        pass

# Bad - Missing methods
class BadIterator:
    def __next__(self):
        # Only __next__, no __iter__
        pass
```

### 2. Raise StopIteration When Done:

```python
# Good - Proper termination
class GoodIterator:
    def __next__(self):
        if self.has_more():
            return self.get_next()
        else:
            raise StopIteration  # Proper!

# Bad - Returns None
class BadIterator:
    def __next__(self):
        if self.has_more():
            return self.get_next()
        else:
            return None  # Wrong! Should raise StopIteration
```

### 3. Make Iterables Reusable:

```python
# Good - Separate iterator
class GoodIterable:
    def __iter__(self):
        return MyIterator(self.data)  # New iterator each time

# Bad - Returns self
class BadIterable:
    def __iter__(self):
        return self  # Same object, not reusable!
```

### 4. Use Generators for Simple Cases:

```python
# Good - Generator (simple)
def simple_range(n):
    for i in range(n):
        yield i

# Overkill - Iterator class for simple case
class SimpleRange:
    def __init__(self, n):
        self.n = n
        self.i = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i < self.n:
            self.i += 1
            return self.i - 1
        raise StopIteration
```

---

## Summary

### Quick Reference:

```python
# Iterator class
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        raise StopIteration

# Usage
for item in MyIterator([1, 2, 3]):
    print(item)
```

### Key Points:

- ✅ Iterator has `__iter__()` and `__next__()`
- ✅ `__iter__()` returns self (or new iterator)
- ✅ `__next__()` returns next value or raises StopIteration
- ✅ Iterable has `__iter__()` that returns iterator
- ✅ Iterators are exhausted after use
- ✅ Use generators for simple iterators
- ✅ Separate iterator class for reusable iterables
- ✅ Always raise StopIteration when done

**Iterators = Sequential access + Memory efficient!** 🚀
