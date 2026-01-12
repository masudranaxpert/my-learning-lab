# Python Deep Dive - Context Managers

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Context Manager কী এবং কেন?](#context-manager-কী-এবং-কেন)
3. [with Statement](#with-statement)
4. [__enter__ এবং __exit__](#__enter__-এবং-__exit__)
5. [contextlib Module](#contextlib-module)
6. [Real-World Examples](#real-world-examples)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

---

## পরিচিতি

Context Managers হলো Python এর একটি feature যা resources (files, connections, locks) properly manage করতে দেয়।

### সমস্যা:

```python
# Without context manager - Risky!
file = open('data.txt', 'r')
data = file.read()
# যদি এখানে error হয় তাহলে file close হবে না!
file.close()  # Might not execute!
```

### সমাধান:

```python
# With context manager - Safe!
with open('data.txt', 'r') as file:
    data = file.read()
# File automatically closed, even if error occurs!
```

---

## Context Manager কী এবং কেন?

### Context Manager কী?

**সহজ ভাষায়:** Context Manager হলো একটি object যা resources এর setup এবং cleanup automatically করে।

**Technical:** Context Manager হলো একটি object যার `__enter__()` এবং `__exit__()` methods আছে।

### কেন Context Manager প্রয়োজন?

**সমস্যা: Resource Leak**

```python
# Bad - File might not close
def read_file():
    file = open('data.txt')
    data = file.read()
    # যদি এখানে exception হয়?
    result = process(data)  # Error হতে পারে!
    file.close()  # Execute নাও হতে পারে!
    return result

# Problem:
# - File open থেকে যাবে
# - Memory leak
# - Too many open files error
```

**সমাধান: Context Manager**

```python
# Good - File always closes
def read_file():
    with open('data.txt') as file:
        data = file.read()
        result = process(data)  # Error হলেও file close হবে!
        return result

# Benefits:
# - File automatically closes
# - No resource leak
# - Clean code
```

### Real-World তুলনা:

```
Context Manager = Hotel Room

__enter__: Check-in
- Room key পাওয়া
- Room ready করা

Your code: Room ব্যবহার করা
- যা করার করুন

__exit__: Check-out
- Room ছেড়ে দেওয়া
- Cleanup করা
- Error হলেও checkout হবে!
```

---

## with Statement

### Basic Syntax:

```python
with expression as variable:
    # Code block
    # variable ব্যবহার করুন
# Automatic cleanup হয়ে গেছে!
```

### কী হচ্ছে Step by Step:

```python
with open('file.txt', 'r') as file:
    data = file.read()
    print(data)
```

**Execution Flow:**

```
Step 1: open('file.txt', 'r') execute হয়
  → File object তৈরি হয়
  ↓
Step 2: File object এর __enter__() call হয়
  → File open হয়
  → File object return হয়
  → 'file' variable এ assign হয়
  ↓
Step 3: with block এর code execute হয়
  → data = file.read()
  → print(data)
  ↓
Step 4: Block শেষ হলে __exit__() call হয়
  → File automatically close হয়
  → Error হলেও close হবে!
```

### Without with (Manual):

```python
# এটাই হয় internally:
file = open('file.txt', 'r')
file.__enter__()  # Setup

try:
    data = file.read()
    print(data)
finally:
    file.__exit__(None, None, None)  # Cleanup
```

### Multiple Context Managers:

```python
# Method 1: Nested
with open('input.txt', 'r') as infile:
    with open('output.txt', 'w') as outfile:
        data = infile.read()
        outfile.write(data)

# Method 2: Single line (Python 3.1+)
with open('input.txt', 'r') as infile, \
     open('output.txt', 'w') as outfile:
    data = infile.read()
    outfile.write(data)
```

---

## __enter__ এবং __exit__

### Creating Custom Context Manager:

```python
class MyContextManager:
    """
    Custom context manager example
    """
    
    def __enter__(self):
        """
        Called when entering 'with' block
        
        কখন: with statement শুরু হলে
        কাজ: Setup/initialization
        Return: যা 'as' variable এ যাবে
        """
        print("Entering context")
        # Setup code here
        return self  # This goes to 'as' variable
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when exiting 'with' block
        
        কখন: with block শেষ হলে (error হলেও!)
        কাজ: Cleanup/finalization
        
        Parameters:
            exc_type: Exception type (if error occurred)
            exc_value: Exception value
            traceback: Traceback object
        
        Return:
            True: Suppress exception
            False/None: Propagate exception
        """
        print("Exiting context")
        # Cleanup code here
        
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        
        # Return True to suppress exception
        # Return False/None to propagate exception
        return False

# Usage
with MyContextManager() as manager:
    print("Inside with block")
    # Do something

# Output:
# Entering context
# Inside with block
# Exiting context
```

### কী হচ্ছে বিস্তারিত:

```python
class FileManager:
    def __init__(self, filename, mode):
        """Initialize with filename and mode"""
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """
        Open file and return file object
        
        কখন call হয়: with FileManager(...) as f:
                                          ↑ এখানে
        """
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file  # This becomes 'f'
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close file
        
        কখন call হয়: with block শেষ হলে
        """
        print(f"Closing {self.filename}")
        
        if self.file:
            self.file.close()
        
        # Handle exceptions
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}")
            print(f"Message: {exc_value}")
        
        # Return False to propagate exception
        return False

# Usage
with FileManager('test.txt', 'w') as f:
    f.write("Hello, World!")
    # File automatically closes after this block

# Output:
# Opening test.txt
# Closing test.txt
```

### Error Handling Example:

```python
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        """Connect to database"""
        print(f"Connecting to {self.db_name}")
        # Simulate connection
        self.connection = f"Connection to {self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Disconnect from database"""
        print(f"Disconnecting from {self.db_name}")
        
        if exc_type is not None:
            print(f"Error occurred: {exc_value}")
            # Log error, rollback transaction, etc.
        
        # Always disconnect
        self.connection = None
        
        # Return False to propagate exception
        return False

# Test with error
try:
    with DatabaseConnection('mydb') as conn:
        print(f"Using {conn}")
        raise ValueError("Something went wrong!")
except ValueError as e:
    print(f"Caught exception: {e}")

# Output:
# Connecting to mydb
# Using Connection to mydb
# Disconnecting from mydb
# Error occurred: Something went wrong!
# Caught exception: Something went wrong!
```

---

## contextlib Module

Python এর `contextlib` module context managers তৈরি করা সহজ করে।

### 1. @contextmanager Decorator

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    """
    Simple context manager using decorator
    
    yield এর আগে: __enter__ code
    yield: যা return হবে
    yield এর পরে: __exit__ code
    """
    # Setup (__enter__)
    print("Entering")
    resource = "My Resource"
    
    try:
        yield resource  # This goes to 'as' variable
    finally:
        # Cleanup (__exit__)
        print("Exiting")

# Usage
with my_context() as res:
    print(f"Using {res}")

# Output:
# Entering
# Using My Resource
# Exiting
```

### কী হচ্ছে:

```python
@contextmanager
def file_manager(filename, mode):
    """File manager using contextmanager"""
    
    # __enter__ part
    print(f"Opening {filename}")
    file = open(filename, mode)
    
    try:
        yield file  # Pause here, return file
        # with block executes
    finally:
        # __exit__ part
        print(f"Closing {filename}")
        file.close()

# Usage
with file_manager('test.txt', 'w') as f:
    f.write("Hello!")

# Equivalent to:
# 1. Open file (__enter__)
# 2. Pause at yield, return file
# 3. Execute with block
# 4. Resume after yield, close file (__exit__)
```

### 2. Error Handling with @contextmanager:

```python
from contextlib import contextmanager

@contextmanager
def error_handler():
    """Handle errors gracefully"""
    print("Starting operation")
    
    try:
        yield
    except Exception as e:
        print(f"Error caught: {e}")
        # Handle error
    finally:
        print("Cleanup done")

# Usage
with error_handler():
    print("Doing something")
    raise ValueError("Oops!")
    print("This won't execute")

# Output:
# Starting operation
# Doing something
# Error caught: Oops!
# Cleanup done
```

### 3. suppress() - Suppress Exceptions:

```python
from contextlib import suppress

# Without suppress
try:
    with open('nonexistent.txt') as f:
        data = f.read()
except FileNotFoundError:
    pass  # Ignore error

# With suppress - cleaner!
with suppress(FileNotFoundError):
    with open('nonexistent.txt') as f:
        data = f.read()
# Error suppressed automatically!
```

---

## Real-World Examples

### 1. Database Transaction:

```python
from contextlib import contextmanager

@contextmanager
def database_transaction(connection):
    """
    Database transaction context manager
    
    Commits on success, rolls back on error
    """
    print("Starting transaction")
    
    try:
        yield connection
        # If we reach here, commit
        connection.commit()
        print("Transaction committed")
    except Exception as e:
        # If error, rollback
        connection.rollback()
        print(f"Transaction rolled back: {e}")
        raise  # Re-raise exception
    finally:
        print("Transaction ended")

# Usage
with database_transaction(db_connection) as conn:
    conn.execute("INSERT INTO users VALUES (...)")
    conn.execute("UPDATE accounts SET ...")
    # If any error, both operations rolled back!
```

### 2. Timer Context Manager:

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(name):
    """Measure execution time"""
    start_time = time.time()
    print(f"[{name}] Starting...")
    
    try:
        yield
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"[{name}] Finished in {duration:.4f} seconds")

# Usage
with timer("Data Processing"):
    # Simulate work
    time.sleep(2)
    process_data()

# Output:
# [Data Processing] Starting...
# [Data Processing] Finished in 2.0001 seconds
```

### 3. Temporary Directory:

```python
import os
import shutil
from contextlib import contextmanager

@contextmanager
def temporary_directory(prefix='tmp'):
    """Create and cleanup temporary directory"""
    import tempfile
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix=prefix)
    print(f"Created temp directory: {temp_dir}")
    
    try:
        yield temp_dir
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"Removed temp directory: {temp_dir}")

# Usage
with temporary_directory('myapp_') as temp_dir:
    # Use temp directory
    file_path = os.path.join(temp_dir, 'data.txt')
    with open(file_path, 'w') as f:
        f.write("Temporary data")
# Directory automatically deleted!
```

### 4. Lock Manager:

```python
from contextlib import contextmanager
import threading

@contextmanager
def acquire_lock(lock):
    """Acquire and release lock"""
    print("Acquiring lock...")
    lock.acquire()
    print("Lock acquired")
    
    try:
        yield
    finally:
        lock.release()
        print("Lock released")

# Usage
lock = threading.Lock()

with acquire_lock(lock):
    # Critical section
    # Only one thread can be here
    shared_resource.modify()
```

### 5. Change Directory:

```python
import os
from contextlib import contextmanager

@contextmanager
def change_directory(path):
    """Temporarily change directory"""
    original_dir = os.getcwd()
    print(f"Changing directory to: {path}")
    os.chdir(path)
    
    try:
        yield
    finally:
        os.chdir(original_dir)
        print(f"Changed back to: {original_dir}")

# Usage
print(f"Current: {os.getcwd()}")

with change_directory('/tmp'):
    print(f"Inside with: {os.getcwd()}")
    # Do work in /tmp

print(f"After with: {os.getcwd()}")
# Back to original directory!
```

---

## Error Handling

### Suppressing Exceptions:

```python
class SuppressErrors:
    """Context manager that suppresses all errors"""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Suppressed error: {exc_value}")
            return True  # Suppress exception
        return False

# Usage
with SuppressErrors():
    print("Before error")
    raise ValueError("This error will be suppressed")
    print("This won't execute")

print("Program continues!")

# Output:
# Before error
# Suppressed error: This error will be suppressed
# Program continues!
```

### Logging Exceptions:

```python
import logging
from contextlib import contextmanager

@contextmanager
def log_errors(logger):
    """Log exceptions but don't suppress"""
    try:
        yield
    except Exception as e:
        logger.error(f"Exception occurred: {e}", exc_info=True)
        raise  # Re-raise exception

# Usage
logger = logging.getLogger(__name__)

with log_errors(logger):
    risky_operation()
```

---

## Best Practices

### 1. Always Use Context Managers for Resources:

```python
# Good - Context manager
with open('file.txt') as f:
    data = f.read()

# Bad - Manual management
f = open('file.txt')
data = f.read()
f.close()
```

### 2. Use contextlib for Simple Cases:

```python
from contextlib import contextmanager

# Good - Simple and clear
@contextmanager
def my_context():
    setup()
    try:
        yield
    finally:
        cleanup()

# Overkill - Too much code for simple case
class MyContext:
    def __enter__(self):
        setup()
        return self
    
    def __exit__(self, *args):
        cleanup()
```

### 3. Document Your Context Managers:

```python
@contextmanager
def my_context(param):
    """
    Context manager description.
    
    Args:
        param: Parameter description
    
    Yields:
        What is yielded
    
    Example:
        with my_context('value') as ctx:
            # Use ctx
            pass
    """
    # Implementation
```

### 4. Handle Cleanup in finally:

```python
@contextmanager
def safe_context():
    resource = acquire_resource()
    
    try:
        yield resource
    finally:
        # Always cleanup, even if error
        release_resource(resource)
```

---

## Summary

### Quick Reference:

```python
# Using built-in context manager
with open('file.txt') as f:
    data = f.read()

# Custom context manager (class)
class MyContext:
    def __enter__(self):
        # Setup
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup
        return False

# Custom context manager (decorator)
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup
    yield resource
    # Cleanup
```

### Key Points:

- ✅ Context managers ensure cleanup happens
- ✅ Use `with` statement for automatic resource management
- ✅ `__enter__()` for setup, `__exit__()` for cleanup
- ✅ `@contextmanager` decorator for simple cases
- ✅ Always cleanup in `finally` block
- ✅ Return `True` from `__exit__()` to suppress exceptions
- ✅ Perfect for files, locks, connections, transactions
- ✅ Prevents resource leaks

**Context Managers = Automatic cleanup + Safe resource management!** 🚀
