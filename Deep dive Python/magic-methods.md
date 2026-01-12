# Python Deep Dive - Magic Methods (Dunder Methods)

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Magic Methods কী এবং কেন?](#magic-methods-কী-এবং-কেন)
3. [Object Representation](#object-representation)
4. [Comparison Methods](#comparison-methods)
5. [Arithmetic Operations](#arithmetic-operations)
6. [Container Methods](#container-methods)
7. [Attribute Access](#attribute-access)
8. [Callable Objects](#callable-objects)
9. [Context Managers](#context-managers)
10. [Complete Example](#complete-example)

---

## পরিচিতি

Magic Methods (বা Dunder Methods) হলো Python এর special methods যা `__` দিয়ে শুরু এবং শেষ হয়।

### সহজ উদাহরণ:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name}, {age} years old"

person = Person("John", 25)
print(person)  # John, 25 years old
# __str__() automatically called!
```

---

## Magic Methods কী এবং কেন?

### Magic Methods কী?

**সহজ ভাষায়:** Magic methods হলো special methods যা Python automatically call করে যখন আপনি operators বা built-in functions ব্যবহার করেন।

**Also called:** 
- Dunder methods (Double UNDERscore)
- Special methods

### কেন Magic Methods প্রয়োজন?

1. **Operator Overloading** - Custom objects এ +, -, *, / ইত্যাদি কাজ করানো
2. **Built-in Functions** - len(), str(), repr() ইত্যাদি support করা
3. **Pythonic Code** - Objects কে built-in types এর মতো behave করানো
4. **Custom Behavior** - Objects এর behavior customize করা

### Real-World তুলনা:

```
Magic Methods = Remote Control Buttons

TV Remote:
- Power button → __init__() (start)
- Volume + → __add__() (increase)
- Channel up → __next__() (next item)

Python automatically জানে কোন button press করলে কী হবে!
```

---

## Object Representation

### 1. `__init__()` - Constructor:

```python
class Person:
    def __init__(self, name, age):
        """
        Called when object is created
        
        কখন: person = Person("John", 25)
        """
        print("__init__ called")
        self.name = name
        self.age = age

person = Person("John", 25)
# Output: __init__ called
```

### 2. `__str__()` - String Representation:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        """
        Called by str() and print()
        
        কখন: print(person) or str(person)
        Return: User-friendly string
        """
        return f"{self.name}, {self.age} years old"

person = Person("John", 25)
print(person)      # John, 25 years old
print(str(person)) # John, 25 years old
```

### 3. `__repr__()` - Developer Representation:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        """
        Called by repr()
        
        কখন: repr(person) or in interactive shell
        Return: Unambiguous representation (ideally recreatable)
        """
        return f"Person('{self.name}', {self.age})"

person = Person("John", 25)
print(repr(person))  # Person('John', 25)

# In interactive shell:
>>> person
Person('John', 25)
```

### `__str__` vs `__repr__`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        # User-friendly
        return f"Point at ({self.x}, {self.y})"
    
    def __repr__(self):
        # Developer-friendly (recreatable)
        return f"Point({self.x}, {self.y})"

point = Point(3, 4)

print(str(point))   # Point at (3, 4)
print(repr(point))  # Point(3, 4)

# If only __repr__ is defined, it's used for both
# If only __str__ is defined, __repr__ uses default
```

---

## Comparison Methods

### Comparison Operators:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        """
        Equal: ==
        
        কখন: person1 == person2
        """
        return self.age == other.age
    
    def __ne__(self, other):
        """
        Not equal: !=
        
        কখন: person1 != person2
        """
        return self.age != other.age
    
    def __lt__(self, other):
        """
        Less than: <
        
        কখন: person1 < person2
        """
        return self.age < other.age
    
    def __le__(self, other):
        """
        Less than or equal: <=
        
        কখন: person1 <= person2
        """
        return self.age <= other.age
    
    def __gt__(self, other):
        """
        Greater than: >
        
        কখন: person1 > person2
        """
        return self.age > other.age
    
    def __ge__(self, other):
        """
        Greater than or equal: >=
        
        কখন: person1 >= person2
        """
        return self.age >= other.age

# Usage
person1 = Person("John", 25)
person2 = Person("Jane", 30)

print(person1 == person2)  # False
print(person1 < person2)   # True (25 < 30)
print(person1 > person2)   # False
```

### Sorting with Comparison:

```python
people = [
    Person("John", 25),
    Person("Jane", 30),
    Person("Bob", 20)
]

# Can now sort!
sorted_people = sorted(people)
for person in sorted_people:
    print(person.name, person.age)
# Output:
# Bob 20
# John 25
# Jane 30
```

---

## Arithmetic Operations

### Basic Arithmetic:

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """
        Addition: +
        
        কখন: v1 + v2
        """
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """
        Subtraction: -
        
        কখন: v1 - v2
        """
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """
        Multiplication: *
        
        কখন: v * 2
        """
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """
        Division: /
        
        কখন: v / 2
        """
        return Vector(self.x / scalar, self.y / scalar)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

# Usage
v1 = Vector(2, 3)
v2 = Vector(1, 4)

print(v1 + v2)  # Vector(3, 7)
print(v1 - v2)  # Vector(1, -1)
print(v1 * 2)   # Vector(4, 6)
print(v1 / 2)   # Vector(1.0, 1.5)
```

### More Operators:

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __mod__(self, other):
        """Modulo: %"""
        return Number(self.value % other.value)
    
    def __pow__(self, other):
        """Power: **"""
        return Number(self.value ** other.value)
    
    def __floordiv__(self, other):
        """Floor division: //"""
        return Number(self.value // other.value)
    
    def __str__(self):
        return str(self.value)

n1 = Number(10)
n2 = Number(3)

print(n1 % n2)   # 1 (10 % 3)
print(n1 ** n2)  # 1000 (10 ** 3)
print(n1 // n2)  # 3 (10 // 3)
```

---

## Container Methods

### 1. `__len__()` - Length:

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __len__(self):
        """
        Called by len()
        
        কখন: len(playlist)
        """
        return len(self.songs)
    
    def add_song(self, song):
        self.songs.append(song)

playlist = Playlist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")

print(len(playlist))  # 2
```

### 2. `__getitem__()` - Indexing:

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __getitem__(self, index):
        """
        Called for indexing and slicing
        
        কখন: playlist[0] or playlist[1:3]
        """
        return self.songs[index]
    
    def add_song(self, song):
        self.songs.append(song)

playlist = Playlist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")
playlist.add_song("Song 3")

print(playlist[0])     # Song 1
print(playlist[1:3])   # ['Song 2', 'Song 3']

# Can also iterate!
for song in playlist:
    print(song)
```

### 3. `__setitem__()` - Assignment:

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __setitem__(self, index, value):
        """
        Called for item assignment
        
        কখন: playlist[0] = "New Song"
        """
        self.songs[index] = value
    
    def add_song(self, song):
        self.songs.append(song)

playlist = Playlist()
playlist.add_song("Song 1")
playlist[0] = "Updated Song"  # Calls __setitem__
```

### 4. `__delitem__()` - Deletion:

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __delitem__(self, index):
        """
        Called for item deletion
        
        কখন: del playlist[0]
        """
        del self.songs[index]

playlist = Playlist()
playlist.add_song("Song 1")
del playlist[0]  # Calls __delitem__
```

### 5. `__contains__()` - Membership:

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __contains__(self, song):
        """
        Called by 'in' operator
        
        কখন: "Song 1" in playlist
        """
        return song in self.songs

playlist = Playlist()
playlist.add_song("Song 1")

print("Song 1" in playlist)  # True
print("Song 2" in playlist)  # False
```

---

## Attribute Access

### 1. `__getattr__()` - Get Missing Attribute:

```python
class DynamicObject:
    def __init__(self):
        self.existing = "I exist"
    
    def __getattr__(self, name):
        """
        Called when attribute not found
        
        কখন: obj.missing_attribute
        """
        return f"'{name}' not found, returning default"

obj = DynamicObject()
print(obj.existing)  # I exist (normal attribute)
print(obj.missing)   # 'missing' not found, returning default
```

### 2. `__setattr__()` - Set Attribute:

```python
class ValidatedObject:
    def __setattr__(self, name, value):
        """
        Called when setting attribute
        
        কখন: obj.name = value
        """
        if name == "age" and value < 0:
            raise ValueError("Age cannot be negative")
        
        # Must use __dict__ to avoid infinite recursion
        self.__dict__[name] = value

obj = ValidatedObject()
obj.age = 25  # OK
# obj.age = -5  # ValueError!
```

### 3. `__delattr__()` - Delete Attribute:

```python
class ProtectedObject:
    def __init__(self):
        self.protected = "Can't delete me"
        self.normal = "Can delete me"
    
    def __delattr__(self, name):
        """
        Called when deleting attribute
        
        কখন: del obj.attribute
        """
        if name == "protected":
            raise AttributeError(f"Can't delete {name}")
        
        del self.__dict__[name]

obj = ProtectedObject()
del obj.normal     # OK
# del obj.protected  # AttributeError!
```

---

## Callable Objects

### `__call__()` - Make Object Callable:

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        """
        Make object callable like a function
        
        কখন: obj(5)
        """
        return x * self.factor

# Create callable object
times_3 = Multiplier(3)

# Call it like a function!
print(times_3(10))  # 30
print(times_3(5))   # 15

# It's an object but acts like a function!
```

### Practical Example - Counter:

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        """Increment and return count"""
        self.count += 1
        return self.count

counter = Counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

---

## Context Managers

### `__enter__` and `__exit__`:

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """
        Called when entering 'with' block
        
        কখন: with FileManager(...) as f:
        """
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when exiting 'with' block
        
        কখন: with block শেষ হলে
        """
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        return False

# Usage
with FileManager('test.txt', 'w') as f:
    f.write("Hello, World!")
# File automatically closed!
```

---

## Complete Example

### Full-Featured Class:

```python
class BankAccount:
    """
    Complete example with multiple magic methods
    """
    
    def __init__(self, owner, balance=0):
        """Constructor"""
        self.owner = owner
        self.balance = balance
        self.transactions = []
    
    def __str__(self):
        """User-friendly string"""
        return f"{self.owner}'s account: ${self.balance}"
    
    def __repr__(self):
        """Developer-friendly string"""
        return f"BankAccount('{self.owner}', {self.balance})"
    
    def __len__(self):
        """Number of transactions"""
        return len(self.transactions)
    
    def __getitem__(self, index):
        """Get transaction by index"""
        return self.transactions[index]
    
    def __add__(self, amount):
        """Deposit money: account + 100"""
        self.balance += amount
        self.transactions.append(f"Deposit: +${amount}")
        return self
    
    def __sub__(self, amount):
        """Withdraw money: account - 50"""
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount}")
        else:
            raise ValueError("Insufficient funds")
        return self
    
    def __eq__(self, other):
        """Compare balances"""
        return self.balance == other.balance
    
    def __lt__(self, other):
        """Compare balances"""
        return self.balance < other.balance
    
    def __call__(self):
        """Get balance when called"""
        return self.balance
    
    def __contains__(self, keyword):
        """Check if keyword in transactions"""
        return any(keyword in t for t in self.transactions)

# Usage
account = BankAccount("John", 1000)

# __str__
print(account)  # John's account: $1000

# __repr__
print(repr(account))  # BankAccount('John', 1000)

# __add__ and __sub__
account + 500  # Deposit
account - 200  # Withdraw

# __len__
print(len(account))  # 2 transactions

# __getitem__
print(account[0])  # Deposit: +$500

# __call__
print(account())  # 1300 (current balance)

# __contains__
print("Deposit" in account)  # True

# __eq__ and __lt__
account2 = BankAccount("Jane", 1300)
print(account == account2)  # True (same balance)
print(account < account2)   # False
```

---

## Common Magic Methods Reference

### Object Lifecycle:
- `__init__(self, ...)` - Constructor
- `__del__(self)` - Destructor

### Representation:
- `__str__(self)` - str() and print()
- `__repr__(self)` - repr() and interactive shell
- `__format__(self, format_spec)` - format()

### Comparison:
- `__eq__(self, other)` - ==
- `__ne__(self, other)` - !=
- `__lt__(self, other)` - <
- `__le__(self, other)` - <=
- `__gt__(self, other)` - >
- `__ge__(self, other)` - >=

### Arithmetic:
- `__add__(self, other)` - +
- `__sub__(self, other)` - -
- `__mul__(self, other)` - *
- `__truediv__(self, other)` - /
- `__floordiv__(self, other)` - //
- `__mod__(self, other)` - %
- `__pow__(self, other)` - **

### Container:
- `__len__(self)` - len()
- `__getitem__(self, key)` - obj[key]
- `__setitem__(self, key, value)` - obj[key] = value
- `__delitem__(self, key)` - del obj[key]
- `__contains__(self, item)` - item in obj
- `__iter__(self)` - for item in obj

### Callable:
- `__call__(self, ...)` - obj()

### Context Manager:
- `__enter__(self)` - with obj:
- `__exit__(self, ...)` - End of with block

---

## Summary

### Key Points:

- ✅ Magic methods start and end with `__`
- ✅ Called automatically by Python
- ✅ Enable operator overloading
- ✅ Make custom objects behave like built-ins
- ✅ `__str__` for users, `__repr__` for developers
- ✅ Implement comparison for sorting
- ✅ Implement arithmetic for math operations
- ✅ Implement container methods for indexing
- ✅ `__call__` makes objects callable

**Magic Methods = Custom behavior + Pythonic code!** 🚀
