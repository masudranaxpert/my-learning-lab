# Python Deep Dive - Metaclasses

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Metaclass কী এবং কেন?](#metaclass-কী-এবং-কেন)
3. [type() Function](#type-function)
4. [How Classes are Created](#how-classes-are-created)
5. [Creating Metaclasses](#creating-metaclasses)
6. [__new__ vs __init__](#__new__-vs-__init__)
7. [Real-World Examples](#real-world-examples)
8. [When to Use Metaclasses](#when-to-use-metaclasses)
9. [Best Practices](#best-practices)

---

## পরিচিতি

Metaclasses হলো Python এর সবচেয়ে advanced concept - "classes যা classes তৈরি করে"।

### মনে রাখুন:

```
Everything in Python is an object!

5 is an object → type: int
"hello" is an object → type: str
my_function is an object → type: function

MyClass is also an object! → type: type
```

---

## Metaclass কী এবং কেন?

### Metaclass কী?

**সহজ ভাষায়:** Metaclass হলো "class এর class" - যা classes তৈরি করে।

```python
# Normal relationship
instance = MyClass()  # MyClass creates instance

# Metaclass relationship
MyClass = MetaClass()  # MetaClass creates MyClass!
```

### Hierarchy:

```
Object Hierarchy:
instance → class → metaclass → type

Example:
john → Person → type → type
(object) (class) (metaclass) (base metaclass)
```

### কেন Metaclass প্রয়োজন?

**Warning:** 99% সময় metaclass লাগে না! শুধু খুব advanced cases এ।

**Use cases:**
1. **Class Validation** - Class তৈরির সময় validation
2. **Auto-registration** - Classes automatically register করা
3. **API Frameworks** - Django ORM, SQLAlchemy
4. **Singleton Pattern** - শুধু একটা instance
5. **Attribute Modification** - Class attributes modify করা

### Real-World তুলনা:

```
Metaclass = Factory যা Factories তৈরি করে

Normal Factory (Class):
- Products তৈরি করে (instances)
- Car factory → cars

Meta Factory (Metaclass):
- Factories তৈরি করে (classes)
- Factory builder → car factory, bike factory
```

---

## type() Function

### type() এর দুটো কাজ:

#### 1. Check Type:

```python
# Check object type
print(type(5))        # <class 'int'>
print(type("hello"))  # <class 'str'>
print(type([1, 2]))   # <class 'list'>

# Check class type
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
print(type(MyClass()))  # <class '__main__.MyClass'>
```

#### 2. Create Classes Dynamically:

```python
# Normal class definition
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, I'm {self.name}"

# Same thing using type()!
def __init__(self, name):
    self.name = name

def greet(self):
    return f"Hello, I'm {self.name}"

Person = type('Person', (), {
    '__init__': __init__,
    'greet': greet
})

# Both work the same!
person = Person("John")
print(person.greet())  # Hello, I'm John
```

### type() Syntax:

```python
type(name, bases, dict)

# name: Class name (string)
# bases: Tuple of parent classes
# dict: Dictionary of attributes and methods
```

### Examples:

```python
# Simple class
MyClass = type('MyClass', (), {})

# With attributes
MyClass = type('MyClass', (), {
    'x': 10,
    'y': 20
})

# With methods
def my_method(self):
    return "Hello"

MyClass = type('MyClass', (), {
    'my_method': my_method
})

# With inheritance
class Parent:
    pass

MyClass = type('MyClass', (Parent,), {
    'x': 10
})
```

---

## How Classes are Created

### Normal Class Creation:

```python
class MyClass:
    x = 10
```

### কী হচ্ছে Step by Step:

```
1. Python sees 'class' keyword
   ↓
2. Collects class body (x = 10)
   ↓
3. Determines metaclass (default: type)
   ↓
4. Calls metaclass to create class
   → type('MyClass', (), {'x': 10})
   ↓
5. MyClass created and assigned
```

### With Custom Metaclass:

```python
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=MyMeta):
    x = 10

# Output: Creating class MyClass
```

---

## Creating Metaclasses

### Basic Metaclass:

```python
class MyMeta(type):
    """
    Custom metaclass
    
    Inherits from type
    """
    
    def __new__(cls, name, bases, attrs):
        """
        Called to create the class
        
        cls: Metaclass itself
        name: Name of class being created
        bases: Parent classes
        attrs: Class attributes/methods
        """
        print(f"Creating class: {name}")
        print(f"Parents: {bases}")
        print(f"Attributes: {list(attrs.keys())}")
        
        # Create and return the class
        return super().__new__(cls, name, bases, attrs)

# Use metaclass
class MyClass(metaclass=MyMeta):
    x = 10
    
    def method(self):
        pass

# Output:
# Creating class: MyClass
# Parents: ()
# Attributes: ['__module__', '__qualname__', 'x', 'method']
```

### Modifying Class Attributes:

```python
class UpperAttrMeta(type):
    """
    Convert all attribute names to uppercase
    """
    
    def __new__(cls, name, bases, attrs):
        # Create new dict with uppercase keys
        uppercase_attrs = {}
        
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith('__'):
                # Convert to uppercase
                uppercase_attrs[attr_name.upper()] = attr_value
            else:
                # Keep magic methods as is
                uppercase_attrs[attr_name] = attr_value
        
        return super().__new__(cls, name, bases, uppercase_attrs)

class MyClass(metaclass=UpperAttrMeta):
    x = 10
    y = 20
    
    def method(self):
        return "Hello"

# Attributes are now uppercase!
obj = MyClass()
print(obj.X)  # 10
print(obj.Y)  # 20
print(obj.METHOD())  # Hello
# print(obj.x)  # AttributeError!
```

---

## __new__ vs __init__

### In Metaclass:

```python
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        """
        Create the class
        
        কখন: Class definition এর সময়
        কাজ: Class object তৈরি করা
        Return: Class object
        """
        print(f"__new__ called for {name}")
        return super().__new__(cls, name, bases, attrs)
    
    def __init__(cls, name, bases, attrs):
        """
        Initialize the class
        
        কখন: Class তৈরি হওয়ার পরে
        কাজ: Additional initialization
        Return: None
        """
        print(f"__init__ called for {name}")
        super().__init__(name, bases, attrs)

class MyClass(metaclass=MyMeta):
    pass

# Output:
# __new__ called for MyClass
# __init__ called for MyClass
```

### Execution Order:

```
1. __new__ called
   → Creates class object
   ↓
2. __init__ called
   → Initializes class object
   ↓
3. Class ready to use
```

---

## Real-World Examples

### 1. Singleton Pattern:

```python
class SingletonMeta(type):
    """
    Ensure only one instance of class exists
    """
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        Called when creating instance: MyClass()
        """
        if cls not in cls._instances:
            # Create instance for first time
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Database initialized")

# Test
db1 = Database()  # Database initialized
db2 = Database()  # No output (same instance!)

print(db1 is db2)  # True
```

### 2. Auto-Registration:

```python
class RegistryMeta(type):
    """
    Automatically register all classes
    """
    registry = {}
    
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Register class
        if name != 'Base':  # Don't register base class
            cls.registry[name] = new_class
        
        return new_class

class Base(metaclass=RegistryMeta):
    pass

class Plugin1(Base):
    pass

class Plugin2(Base):
    pass

# All plugins automatically registered!
print(RegistryMeta.registry)
# {'Plugin1': <class 'Plugin1'>, 'Plugin2': <class 'Plugin2'>}
```

### 3. Attribute Validation:

```python
class ValidatedMeta(type):
    """
    Validate class attributes
    """
    
    def __new__(cls, name, bases, attrs):
        # Check for required attributes
        required = ['name', 'version']
        
        for attr in required:
            if attr not in attrs:
                raise TypeError(
                    f"Class {name} must have '{attr}' attribute"
                )
        
        return super().__new__(cls, name, bases, attrs)

# This works
class GoodPlugin(metaclass=ValidatedMeta):
    name = "MyPlugin"
    version = "1.0"

# This fails
try:
    class BadPlugin(metaclass=ValidatedMeta):
        name = "BadPlugin"
        # Missing 'version'!
except TypeError as e:
    print(e)  # Class BadPlugin must have 'version' attribute
```

### 4. Method Injection:

```python
class AddMethodsMeta(type):
    """
    Automatically add methods to class
    """
    
    def __new__(cls, name, bases, attrs):
        # Add a method to all classes
        def to_dict(self):
            """Convert instance to dict"""
            return {
                k: v for k, v in self.__dict__.items()
                if not k.startswith('_')
            }
        
        attrs['to_dict'] = to_dict
        
        return super().__new__(cls, name, bases, attrs)

class Person(metaclass=AddMethodsMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("John", 25)
print(person.to_dict())  # {'name': 'John', 'age': 25}
# to_dict() automatically added!
```

### 5. Django-style ORM:

```python
class Field:
    """Represents a database field"""
    def __init__(self, field_type):
        self.field_type = field_type

class ModelMeta(type):
    """
    Metaclass for ORM models (simplified Django ORM)
    """
    
    def __new__(cls, name, bases, attrs):
        # Collect fields
        fields = {}
        
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                # Remove from class attributes
                attrs.pop(key)
        
        # Store fields in class
        attrs['_fields'] = fields
        
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    """Base model class"""
    pass

class User(Model):
    name = Field('varchar')
    age = Field('integer')
    email = Field('varchar')

# Fields are now in _fields
print(User._fields)
# {'name': <Field>, 'age': <Field>, 'email': <Field>}

# Can create instances normally
user = User()
user.name = "John"  # Works!
```

---

## When to Use Metaclasses

### ✅ Good Use Cases:

1. **Framework Development** - Django, SQLAlchemy
2. **API Design** - Automatic registration, validation
3. **Singleton Pattern** - One instance only
4. **Attribute Modification** - Auto-add methods/attributes
5. **Class Validation** - Enforce rules at class creation

### ❌ When NOT to Use:

```python
# Bad - Metaclass for simple task
class SimpleMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['x'] = 10
        return super().__new__(cls, name, bases, attrs)

# Good - Use class decorator or inheritance
def add_x(cls):
    cls.x = 10
    return cls

@add_x
class MyClass:
    pass

# Or simple inheritance
class Base:
    x = 10

class MyClass(Base):
    pass
```

### Tim Peters' Quote:

> "Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't."

---

## Best Practices

### 1. Use Alternatives First:

```python
# Instead of metaclass, try:

# 1. Class Decorator
def my_decorator(cls):
    cls.x = 10
    return cls

@my_decorator
class MyClass:
    pass

# 2. Inheritance
class Base:
    x = 10

class MyClass(Base):
    pass

# 3. __init_subclass__ (Python 3.6+)
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.x = 10

class MyClass(Base):
    pass
```

### 2. Document Metaclasses:

```python
class MyMeta(type):
    """
    Custom metaclass that does X, Y, Z.
    
    Usage:
        class MyClass(metaclass=MyMeta):
            pass
    
    Effects:
        - Adds attribute 'x'
        - Validates 'y'
        - Registers class
    """
    pass
```

### 3. Keep It Simple:

```python
# Good - Simple and clear
class SimpleMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, attrs)

# Bad - Too complex
class ComplexMeta(type):
    def __new__(cls, name, bases, attrs):
        # 100 lines of complex logic
        # Hard to understand and maintain
        pass
```

---

## Summary

### Quick Reference:

```python
# Define metaclass
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        # Modify class before creation
        return super().__new__(cls, name, bases, attrs)

# Use metaclass
class MyClass(metaclass=MyMeta):
    pass

# Create class dynamically
MyClass = type('MyClass', (), {'x': 10})
```

### Key Points:

- ✅ Metaclass = class যা classes তৈরি করে
- ✅ Default metaclass হলো `type`
- ✅ `type()` can create classes dynamically
- ✅ `__new__` creates class, `__init__` initializes
- ✅ Use for framework development, validation
- ✅ 99% সময় metaclass লাগে না!
- ✅ Try decorators/inheritance first
- ✅ Keep metaclasses simple

### Hierarchy:

```
instance → class → metaclass → type

john → Person → type → type
```

**Metaclasses = Advanced magic + Rarely needed!** 🚀

---

## Final Note

Metaclasses খুবই powerful কিন্তু complex। বেশিরভাগ সময় এগুলো লাগে না। 

**Remember:**
- Simple problems → Simple solutions
- Class decorators often enough
- Inheritance usually sufficient
- Metaclasses = last resort!

শুধু framework বা library তৈরি করলে metaclasses দরকার হতে পারে। Normal applications এ লাগে না।
