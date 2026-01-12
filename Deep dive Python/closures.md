# Python Deep Dive - Closures

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Closure কী এবং কেন?](#closure-কী-এবং-কেন)
3. [Nested Functions](#nested-functions)
4. [Variable Scope](#variable-scope)
5. [Creating Closures](#creating-closures)
6. [Closure vs Global Variables](#closure-vs-global-variables)
7. [Real-World Examples](#real-world-examples)
8. [nonlocal Keyword](#nonlocal-keyword)
9. [Best Practices](#best-practices)

---

## পরিচিতি

Closures হলো Python এর একটি powerful concept যেখানে inner function outer function এর variables remember করে রাখে।

### সহজ উদাহরণ:

```python
def outer_function(message):
    # Outer function এর variable
    
    def inner_function():
        # Inner function outer এর variable access করতে পারে
        print(message)
    
    return inner_function

# Create closure
my_func = outer_function("Hello!")

# Call it later - still remembers "Hello!"
my_func()  # Output: Hello!
```

---

## Closure কী এবং কেন?

### Closure কী?

**সহজ ভাষায়:** Closure হলো একটা function যা তার surrounding environment এর variables remember করে রাখে।

**Technical:** Closure হলো একটা function object যা তার enclosing scope এর variables এর reference রাখে।

### কেন Closure প্রয়োজন?

1. **Data Encapsulation** - Private variables তৈরি করা
2. **Factory Functions** - Customized functions তৈরি করা
3. **Callbacks** - State maintain করা
4. **Decorators** - Decorators closures ব্যবহার করে

### Real-World তুলনা:

```
Closure = Backpack with Memory

Outer Function = Packing the backpack
- জিনিসপত্র রাখা (variables)

Inner Function = Taking the backpack
- Backpack নিয়ে যাওয়া
- ভিতরের জিনিস access করা
- যেখানে যান সাথে থাকে!

Closure:
- Inner function = backpack
- Outer variables = জিনিসপত্র
- সবসময় সাথে থাকে!
```

---

## Nested Functions

### Basic Nested Function:

```python
def outer():
    """Outer function"""
    print("Outer function")
    
    def inner():
        """Inner function"""
        print("Inner function")
    
    # Call inner function
    inner()

outer()
# Output:
# Outer function
# Inner function
```

### Returning Inner Function:

```python
def outer():
    """Return inner function"""
    
    def inner():
        print("Inner function")
    
    # Return function object (not calling it!)
    return inner

# Get the inner function
my_func = outer()

# Now call it
my_func()  # Output: Inner function
```

### কী হচ্ছে:

```
1. outer() call করা
   → outer function execute হয়
   → inner function define হয় (execute না!)
   → inner function object return হয়
   
2. my_func = outer()
   → my_func এখন inner function

3. my_func() call করা
   → inner function execute হয়
   → "Inner function" print হয়
```

---

## Variable Scope

### LEGB Rule:

Python variables খোঁজে এই order এ:

1. **L**ocal - Current function
2. **E**nclosing - Outer function(s)
3. **G**lobal - Module level
4. **B**uilt-in - Python built-ins

```python
# Built-in
# len, print, etc.

# Global
global_var = "Global"

def outer():
    # Enclosing
    enclosing_var = "Enclosing"
    
    def inner():
        # Local
        local_var = "Local"
        
        # Can access all!
        print(local_var)      # Local
        print(enclosing_var)  # Enclosing
        print(global_var)     # Global
        print(len([1, 2, 3])) # Built-in
    
    inner()

outer()
```

### Accessing Outer Variables:

```python
def outer():
    x = 10  # Outer variable
    
    def inner():
        # Can read outer variable
        print(x)  # 10
    
    inner()

outer()
```

### কী হচ্ছে:

```
1. outer() call
   → x = 10 (outer এর local variable)
   
2. inner() define হয়
   → inner function x access করতে পারবে
   
3. inner() call
   → x খোঁজে:
     - Local scope এ নেই
     - Enclosing scope এ আছে! (x = 10)
   → print(x) → 10
```

---

## Creating Closures

### Simple Closure:

```python
def make_multiplier(n):
    """
    Create a function that multiplies by n
    
    n is "captured" by the inner function
    """
    def multiplier(x):
        return x * n  # Uses n from outer scope!
    
    return multiplier

# Create different multipliers
times_2 = make_multiplier(2)
times_3 = make_multiplier(3)
times_5 = make_multiplier(5)

# Use them
print(times_2(10))  # 20 (10 * 2)
print(times_3(10))  # 30 (10 * 3)
print(times_5(10))  # 50 (10 * 5)
```

### কী হচ্ছে:

```
1. times_2 = make_multiplier(2)
   → n = 2
   → multiplier function তৈরি হয়
   → multiplier "remembers" n = 2
   → multiplier function return হয়

2. times_2(10) call
   → multiplier(10) execute হয়
   → x = 10
   → return x * n
   → return 10 * 2  (n still remembers 2!)
   → return 20
```

### Closure with Multiple Variables:

```python
def make_counter(start, step):
    """
    Create a counter function
    
    Captures both start and step
    """
    count = start
    
    def counter():
        nonlocal count  # Modify outer variable
        current = count
        count += step
        return current
    
    return counter

# Create counters
count_by_1 = make_counter(0, 1)
count_by_5 = make_counter(0, 5)

print(count_by_1())  # 0
print(count_by_1())  # 1
print(count_by_1())  # 2

print(count_by_5())  # 0
print(count_by_5())  # 5
print(count_by_5())  # 10
```

---

## Closure vs Global Variables

### Global Variables (Bad):

```python
# Global variable - accessible everywhere
counter = 0

def increment():
    global counter
    counter += 1
    return counter

print(increment())  # 1
print(increment())  # 2

# Problem: Anyone can modify counter!
counter = 100  # Oops!
print(increment())  # 101 (unexpected!)
```

### Closure (Good):

```python
def make_counter():
    """Encapsulated counter"""
    counter = 0  # Private!
    
    def increment():
        nonlocal counter
        counter += 1
        return counter
    
    return increment

# Create counter
my_counter = make_counter()

print(my_counter())  # 1
print(my_counter())  # 2

# Can't access counter directly!
# counter = 100  # This won't affect my_counter
print(my_counter())  # 3 (safe!)
```

### Comparison:

| Feature | Global Variables | Closures |
|---------|-----------------|----------|
| **Encapsulation** | ❌ No | ✅ Yes |
| **Safety** | ❌ Can be modified anywhere | ✅ Protected |
| **Multiple Instances** | ❌ Only one | ✅ Multiple independent |
| **Namespace Pollution** | ❌ Yes | ✅ No |

---

## Real-World Examples

### 1. Function Factory:

```python
def make_greeting(greeting):
    """
    Create customized greeting functions
    """
    def greet(name):
        return f"{greeting}, {name}!"
    
    return greet

# Create different greeters
say_hello = make_greeting("Hello")
say_hi = make_greeting("Hi")
say_namaste = make_greeting("Namaste")

print(say_hello("John"))    # Hello, John!
print(say_hi("Jane"))       # Hi, Jane!
print(say_namaste("Raj"))   # Namaste, Raj!
```

### 2. Data Validator:

```python
def make_validator(min_value, max_value):
    """
    Create range validator
    """
    def validate(value):
        if value < min_value:
            return f"Too small! Minimum: {min_value}"
        elif value > max_value:
            return f"Too large! Maximum: {max_value}"
        else:
            return "Valid"
    
    return validate

# Create validators
age_validator = make_validator(0, 120)
percentage_validator = make_validator(0, 100)

print(age_validator(25))      # Valid
print(age_validator(-5))      # Too small! Minimum: 0
print(age_validator(150))     # Too large! Maximum: 120

print(percentage_validator(75))   # Valid
print(percentage_validator(150))  # Too large! Maximum: 100
```

### 3. Private Variables:

```python
def create_account(initial_balance):
    """
    Bank account with private balance
    """
    balance = initial_balance  # Private!
    
    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
            return f"Deposited {amount}. Balance: {balance}"
        return "Invalid amount"
    
    def withdraw(amount):
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            return f"Withdrew {amount}. Balance: {balance}"
        return "Insufficient funds or invalid amount"
    
    def get_balance():
        return balance
    
    # Return interface (not balance directly!)
    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance
    }

# Create account
account = create_account(1000)

print(account['balance']())        # 1000
print(account['deposit'](500))     # Deposited 500. Balance: 1500
print(account['withdraw'](200))    # Withdrew 200. Balance: 1300
print(account['balance']())        # 1300

# Can't access balance directly!
# print(balance)  # Error! balance is private
```

### 4. Memoization (Caching):

```python
def memoize(func):
    """
    Cache function results
    """
    cache = {}  # Closure variable
    
    def wrapper(*args):
        if args in cache:
            print(f"Cache hit for {args}")
            return cache[args]
        
        print(f"Computing for {args}")
        result = func(*args)
        cache[args] = result
        return result
    
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))
# Output:
# Computing for (5,)
# Computing for (4,)
# Computing for (3,)
# Computing for (2,)
# Computing for (1,)
# Computing for (0,)
# Cache hit for (1,)
# Cache hit for (2,)
# Cache hit for (3,)
# 5
```

### 5. Event Handlers:

```python
def create_button(label):
    """
    Create button with click handler
    """
    click_count = 0
    
    def on_click():
        nonlocal click_count
        click_count += 1
        print(f"{label} clicked {click_count} times")
    
    return on_click

# Create buttons
save_button = create_button("Save")
cancel_button = create_button("Cancel")

save_button()    # Save clicked 1 times
save_button()    # Save clicked 2 times
cancel_button()  # Cancel clicked 1 times
save_button()    # Save clicked 3 times
```

---

## nonlocal Keyword

### Problem: Can't Modify Outer Variable:

```python
def outer():
    x = 10
    
    def inner():
        # This creates a NEW local variable!
        x = 20  # Doesn't modify outer x
        print(f"Inner x: {x}")
    
    inner()
    print(f"Outer x: {x}")  # Still 10!

outer()
# Output:
# Inner x: 20
# Outer x: 10
```

### Solution: nonlocal Keyword:

```python
def outer():
    x = 10
    
    def inner():
        nonlocal x  # Modify outer x
        x = 20
        print(f"Inner x: {x}")
    
    inner()
    print(f"Outer x: {x}")  # Changed to 20!

outer()
# Output:
# Inner x: 20
# Outer x: 20
```

### When to Use nonlocal:

```python
def make_counter():
    count = 0
    
    def increment():
        nonlocal count  # Need this to modify count
        count += 1
        return count
    
    def decrement():
        nonlocal count
        count -= 1
        return count
    
    def reset():
        nonlocal count
        count = 0
    
    return increment, decrement, reset

inc, dec, reset = make_counter()

print(inc())   # 1
print(inc())   # 2
print(dec())   # 1
reset()
print(inc())   # 1
```

### nonlocal vs global:

```python
x = 0  # Global

def outer():
    x = 10  # Enclosing
    
    def use_global():
        global x  # Refers to global x (0)
        x += 1
        print(f"Global x: {x}")
    
    def use_nonlocal():
        nonlocal x  # Refers to enclosing x (10)
        x += 1
        print(f"Nonlocal x: {x}")
    
    use_global()    # Global x: 1
    use_nonlocal()  # Nonlocal x: 11
    print(f"Outer x: {x}")  # 11

outer()
print(f"Module x: {x}")  # 1
```

---

## Best Practices

### 1. Use Closures for Encapsulation:

```python
# Good - Encapsulated
def create_counter():
    count = 0  # Private
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    return increment

# Bad - Global variable
count = 0

def increment():
    global count
    count += 1
    return count
```

### 2. Keep Closures Simple:

```python
# Good - Simple closure
def make_adder(n):
    def add(x):
        return x + n
    return add

# Bad - Too complex
def complex_closure(a, b, c):
    def inner1(x):
        def inner2(y):
            def inner3(z):
                return a + b + c + x + y + z
            return inner3
        return inner2
    return inner1
# Too nested! Hard to understand
```

### 3. Document Closure Behavior:

```python
def make_multiplier(factor):
    """
    Create a multiplier function.
    
    Args:
        factor: The multiplication factor (captured by closure)
    
    Returns:
        A function that multiplies its argument by factor
    
    Example:
        >>> times_3 = make_multiplier(3)
        >>> times_3(10)
        30
    """
    def multiply(x):
        return x * factor
    
    return multiply
```

### 4. Be Careful with Loops:

```python
# Bad - All functions reference same i!
functions = []
for i in range(3):
    def func():
        return i  # References i, not value!
    functions.append(func)

for f in functions:
    print(f())  # All print 2! (last value of i)

# Good - Capture value with default argument
functions = []
for i in range(3):
    def func(x=i):  # Capture current value
        return x
    functions.append(func)

for f in functions:
    print(f())  # Prints 0, 1, 2 (correct!)

# Better - Use closure properly
def make_func(i):
    def func():
        return i
    return func

functions = [make_func(i) for i in range(3)]
for f in functions:
    print(f())  # Prints 0, 1, 2
```

---

## Summary

### Quick Reference:

```python
# Basic closure
def outer(x):
    def inner(y):
        return x + y  # Uses x from outer
    return inner

add_5 = outer(5)
print(add_5(10))  # 15

# With nonlocal
def make_counter():
    count = 0
    
    def increment():
        nonlocal count  # Modify outer variable
        count += 1
        return count
    
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

### Key Points:

- ✅ Closure = inner function + captured variables
- ✅ Inner function remembers outer variables
- ✅ Use for data encapsulation
- ✅ Use `nonlocal` to modify outer variables
- ✅ Great for factory functions
- ✅ Decorators use closures
- ✅ Better than global variables
- ✅ Each closure has independent state

**Closures = Function + Memory + Encapsulation!** 🚀
