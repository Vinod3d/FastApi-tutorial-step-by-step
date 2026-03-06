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

Encapsulation means wrapping data (variables) and behavior (methods) together inside a single unit called a class, and restricting direct access to some of the object's components.

In simple words:

We protect the data and allow access only through controlled methods.

Encapsulation helps:

- `Protect sensitive data`

- `Prevent accidental modification`

- `Improve security`

- `Maintain clean code structure`

### 🔹 Real-Life Example

Think about an **ATM machine.**

You cannot directly access your bank balance stored inside the bank system.

You must use options like:

- Withdraw
- Deposit
- Check Balance

The internal database is hidden from you. That is Encapsulation.

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

__balance is a private variable.

In Python:

- Single underscore _var → protected (convention)
- Double underscore __var → private (name mangling)

Name mangling means Python internally changes:
```py
__balance → _Bank__balance
```

This prevents direct access from outside the class.

---

### 2️⃣ Abstraction

Abstraction means Hiding internal implementation details and showing only essential features to the user.

User knows what to do, not how it works internally.

### 🔹 Real-Life Example

When you drive a car:

- You press the accelerator.

- You don’t know how the engine, fuel injection, or combustion system works.

You only know the interface.

That is Abstraction.

Python provides abstraction using the abc module:
```python
from abc import ABC, abstractmethod
```

Example:

```python
from abc import ABC, abstractmethod

class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class UPI(Payment):
    def pay(self, amount):
        print(f"Paying {amount} using UPI")

class Card(Payment):
    def pay(self, amount):
        print(f"Paying {amount} using Card")


```

Here:

- Payment is an abstract class.

- pay() is an abstract method.

Child class MUST implement it.

```
p = UPI()
p.pay(500)

Paying 500 using UPI
```

## 3️⃣ Inheritance

A child class to acquire properties and methods of a parent class.

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
class Employee:
    def calculate_salary(self):
        pass


class FullTimeEmployee(Employee):
    def calculate_salary(self):
        return 50000


class Freelancer(Employee):
    def calculate_salary(self):
        return 1000 * 20   # 20 hours


class Intern(Employee):
    def calculate_salary(self):
        return 10000

```
### Use Case
```
employees = [
    FullTimeEmployee(),
    Freelancer(),
    Intern()
]

for emp in employees:
    print(emp.calculate_salary())

```
Output
```
50000
20000
10000

```

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

Magic methods (also called **dunder methods**) are special methods that start and end with double underscores:

```
__methodname__()
```

They allow you to define how objects behave with:

* Built-in functions (`print()`, `len()`)
* Operators (`+`, `-`)
* Object creation
* String representation
* Comparisons

👉 In simple words:
**They control how your object behaves like built-in types.**



### 1️⃣ `__init__` (Constructor)


`__init__` is a special method that runs automatically when an object is created.
It is used to initialize (set up) the object's data.



When you create a new bank account:

* Name is assigned
* Initial balance is set

That setup process = `__init__`



```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("Vinod", 25)
```

Here:

* `__init__` runs automatically.
* `name` and `age` are stored in the object.

---

### 2️⃣ `__str__` (User-Friendly String)


`__str__` defines what should be displayed when you use `print(object)`.

It gives a **readable, user-friendly representation** of the object.


Think of it like an ID card display:
Instead of showing object memory address, it shows meaningful information.


```python
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

p = Person("Vinod")
print(p)
```

Output:

```
Person: Vinod
```

Without `__str__`, it would print:

```
<__main__.Person object at 0x...>
```

---

### 3️⃣ `__repr__` (Developer Representation)

`__repr__` defines the official string representation of an object.
It is mainly used for debugging and development.

It should ideally return a string that can recreate the object.

 ✅ Difference Between `__str__` and `__repr__`

| `__str__`       | `__repr__`      |
| --------------- | --------------- |
| For users       | For developers  |
| Readable format | Detailed format |



```python
class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person('{self.name}')"

p = Person("Vinod")
print(repr(p))
```

Output:

```
Person('Vinod')
```

---

### 4️⃣ `__len__` (Length Control)


`__len__` defines what happens when `len(object)` is called.

It must return an integer.

If you create a Library class, `len(library)` can return total number of books.


```python
class Library:
    def __init__(self, books):
        self.books = books

    def __len__(self):
        return len(self.books)

lib = Library(["Book1", "Book2", "Book3"])
print(len(lib))
```

Output:

```
3
```

---

### 5️⃣ `__add__` (Operator Overloading)


`__add__` defines what happens when `+` operator is used with objects.

This is called **Operator Overloading**.

If you add two money objects:
Money(100) + Money(200)
Result should be Money(300)


```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Money(self.amount + other.amount)

    def __str__(self):
        return f"{self.amount} Rs"

m1 = Money(100)
m2 = Money(200)

result = m1 + m2
print(result)
```

Output:

```
300 Rs
```


## 9. Static Method & Class Method


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