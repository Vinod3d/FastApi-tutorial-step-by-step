<style> h1 { color: #fff; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 25px; border-radius: 10px; text-align: center; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); } h2 { color: #fff; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px 20px; border-radius: 8px; border-left: 5px solid #ff1744; box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3); } h3 { color: #667eea; border-left: 4px solid #667eea; padding-left: 15px; } li { color: #444; margin: 12px 0; } li::marker { color: #f5576c; font-weight: bold; } strong { color: #f5576c; font-weight: 600; } code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; color: #c7254e; } pre { background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; } table { border-collapse: collapse; width: 100%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); } th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-bottom: 3px solid #f5576c; } td { padding: 12px 15px; border-bottom: 1px solid #e0e0e0; } tr:hover { background: #f9f9f9; } hr { border: none; height: 3px; background: linear-gradient(to right, #667eea, #764ba2, #f5576c); border-radius: 2px; } blockquote { background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%); border-left: 5px solid #667eea; padding: 20px 25px; border-radius: 8px; } </style>

# 🚀 Chapter 1.1 Python Basics


## 1. What is Python?


Python is a high-level, interpreted, dynamically typed programming language that supports multiple programming paradigms including procedural, object-oriented, and functional programming.



## 2. Variables in Python



A variable stores data in memory.

```python
name = "Vinod"
age = 25
salary = 25000.50
is_active = True
```

### Important Point:

Python is **dynamically typed**
👉 You don’t need to define data type explicitly.

```python
x = 10
x = "Hello"
```

This is allowed.


### 📌 Data Types in Python

#### 1️⃣ Primitive Types

| Type  | Example |
| ----- | ------- |
| int   | 10      |
| float | 10.5    |
| str   | "Hello" |
| bool  | True    |



#### 2️⃣ Collection Types

| Type  | Example           | Mutable? |
| ----- | ----------------- | -------- |
| list  | [1,2,3]           | ✅ Yes   |
| tuple | (1,2,3)           | ❌ No    |
| set   | {1,2,3}           | ✅ Yes   |
| dict  | {"name": "Vinod"} | ✅ Yes   |





## 3. Operators

### Arithmetic

```
+  -  *  /  //  %  **
```

### Comparison

```
==  !=  >  <  >=  <=
```

### Logical

```
and  or  not
```


## 4. Conditional Statements

```python
age = 18

if age >= 18:
    print("Adult")
elif age > 12:
    print("Teen")
else:
    print("Child")
```

### Interview Question:

Difference between `==` and `is`

- `==` → checks value
- `is` → checks memory location

```python
a = [1,2]
b = [1,2]

a == b  # True
a is b  # False
```



## 5. Loops in Python

### 1️⃣ for loop

```python
for i in range(5):
    print(i)
```

### 2️⃣ while loop

```python
i = 0
while i < 5:
    print(i)
    i += 1
```



### 📌 break, continue, pass

```python
for i in range(5):
    if i == 2:
        continue
    if i == 4:
        break
    print(i)
```

- `break` → stops loop
- `continue` → skips iteration
- `pass` → does nothing



## 6. Functions in Python

### Basic Function

```python
def greet(name):
    return f"Hello {name}"
```

### Default Argument

```python
def greet(name="Guest"):
    return f"Hello {name}"
```

### Keyword Arguments

```python
greet(name="Vinod")
```


### 📌 \*args and \*\*kwargs (Important for FastAPI & Decorators)

```python
def test(*args):
    print(args)

def test2(**kwargs):
    print(kwargs)
```

- `*args` → multiple positional arguments (tuple)
- `**kwargs` → multiple keyword arguments (dictionary)


## 📌 7. Scope of Variables

### Local Scope

```python
def test():
    x = 10
```

### Global Scope

```python
x = 10

def test():
    print(x)
```

### global keyword

```python
x = 5

def change():
    global x
    x = 10
```


## 8. List Comprehension

```python
numbers = [x for x in range(10)]
```

With condition:

```python
even = [x for x in range(10) if x % 2 == 0]
```


## 9. Exception Handling

```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Error")
finally:
    print("Done")
```

## 10. Importing Modules

```python
import math
from math import sqrt
```



## 🎯 Interview Rapid Fire Questions

1. What is difference between list and tuple?
2. What is mutable vs immutable?
3. What is dynamic typing?
4. What is difference between is and == ?
5. What is \*args and \*\*kwargs?
6. What is scope?
7. What is list comprehension?
8. What is try-except-finally?

You must be able to answer these without thinking.
