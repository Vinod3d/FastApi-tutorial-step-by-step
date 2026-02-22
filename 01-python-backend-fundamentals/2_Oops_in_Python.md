<style> h1 { color: #fff; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 25px; border-radius: 10px; text-align: center; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); } h2 { color: #fff; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px 20px; border-radius: 8px; border-left: 5px solid #ff1744; box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3); } h3 { color: #667eea; border-left: 4px solid #667eea; padding-left: 15px; } li { color: #444; margin: 12px 0; } li::marker { color: #f5576c; font-weight: bold; } strong { color: #f5576c; font-weight: 600; } code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; color: #c7254e; } pre { background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; } table { border-collapse: collapse; width: 100%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); } th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-bottom: 3px solid #f5576c; } td { padding: 12px 15px; border-bottom: 1px solid #e0e0e0; } tr:hover { background: #f9f9f9; } hr { border: none; height: 3px; background: linear-gradient(to right, #667eea, #764ba2, #f5576c); border-radius: 2px; } blockquote { background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%); border-left: 5px solid #667eea; padding: 20px 25px; border-radius: 8px; } </style>

# 🚀 Chapter 1.2 OOP in Python



## 1. What is OOP?

OOP (Object-Oriented Programming) is a programming paradigm where we organize code using **classes and objects**.

Instead of writing everything in functions, we model real-world entities as objects.

### Interview Definition:

Object-Oriented Programming is a programming approach that uses classes and objects to structure code, enabling reusability, scalability, and better organization.


## 2. Class and Object

### What is a Class?

A class is a blueprint for creating objects.

### What is an Object?

An object is an instance of a class.



### Example:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}"
```

Creating object:

```python
p1 = Person("Vinod", 25)
print(p1.greet())
```



### 📌 What is `__init__` 

* It is a constructor
* Automatically runs when object is created
* Used to initialize variables



## 3. self Keyword

`self` refers to the current object.

Without `self`, object variables cannot be accessed.

Example:

```python
class Test:
    def show(self):
        print("Hello")
```

Interview Question:
Why do we need self?

Because it represents the instance of the class and allows access to instance variables and methods.


## 4. Instance Variable vs Class Variable

### Instance Variable

Belongs to object

```python
class Person:
    def __init__(self, name):
        self.name = name
```

Each object has its own `name`.



### Class Variable

Shared by all objects

```python
class Person:
    country = "India"
```

All objects share same value.



## 5. Four Pillars of OOP



### 1️⃣ Encapsulation

Binding data and methods together.

Example:

```python
class Bank:
    def __init__(self, balance):
        self.__balance = balance   # private variable

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

### What is `__balance`?

Double underscore makes it private (name mangling).

Interview Question:
How do you achieve encapsulation in Python?
→ Using private variables and getter/setter methods.


## 2️⃣ Abstraction

Hiding internal implementation details.

Example:
User calls `deposit()`
User does not know how balance is stored internally.

In Python, abstraction is commonly implemented using:

```python
from abc import ABC, abstractmethod
```

Example:

```python
class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass
```

## 3️⃣ Inheritance

Child class inherits from parent class.

```python
class Animal:
    def speak(self):
        return "Animal sound"

class Dog(Animal):
    def bark(self):
        return "Woof"
```

Dog inherits speak().


### Types of Inheritance

* Single
* Multiple
* Multilevel
* Hierarchical



## 4️⃣ Polymorphism

Same function name, different behavior.

Example:

```python
class Dog:
    def sound(self):
        return "Woof"

class Cat:
    def sound(self):
        return "Meow"
```

Both have sound() method but different behavior.

## 6. Method Overriding

Child class changes parent method.

```python
class Animal:
    def speak(self):
        return "Sound"

class Dog(Animal):
    def speak(self):
        return "Woof"
```

## 7. super() Function

Used to call parent class method.

```python
class Dog(Animal):
    def speak(self):
        return super().speak()
```


## 8. Magic Methods (Dunder Methods)

Special methods starting and ending with `__`

Examples:

* `__init__`
* `__str__`
* `__repr__`
* `__len__`
* `__add__`

### Example:

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"
```

Now:

```python
p = Person("Vinod")
print(p)
```

Output:
Person: Vinod

## 9. Composition vs Inheritance

### Inheritance

IS-A relationship

Dog IS-A Animal

### Composition

HAS-A relationship

Car HAS-A Engine

Example:

```python
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()
```

Composition is preferred over inheritance in many real-world systems.

## 10. Static Method & Class Method


### Static Method

Does not access class or instance.

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b
```



### Class Method

Uses class variable.

```python
class Person:
    count = 0

    @classmethod
    def get_count(cls):
        return cls.count
```

## 🎯 Interview Coding Questions

1. Difference between class and object?
2. What is self?
3. What is encapsulation?
4. What is abstraction?
5. What is inheritance?
6. What is method overriding?
7. What is super()?
8. What is difference between static method and class method?
9. What are magic methods?
10. Composition vs Inheritance?

You must be confident answering these.