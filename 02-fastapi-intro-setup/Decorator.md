## What is a Decorator in Python?

A **decorator** in Python is a special function that is used to **modify or enhance another function without changing its original code**.

In simple words:

> A decorator wraps a function and adds extra behavior before or after it runs.

Decorators are commonly used for:

* Logging
* Authentication
* Validation
* Measuring execution time
* Caching
* Access control

---

# 1️⃣ Why Do We Need Decorators?

Suppose you want to print a message before and after every function call.

Instead of writing the same code again and again inside multiple functions, you can use a decorator to reuse that logic.

This makes your code:

* Clean
* Reusable
* Maintainable

---

# 2️⃣ Functions Are First-Class Objects

In Python:

* Functions can be stored in variables
* Functions can be passed as arguments
* Functions can be returned from other functions

Example:

```python
def greet():
    print("Hello")

say_hello = greet
say_hello()
```

Because of this feature, decorators are possible.

---

# 3️⃣ Basic Structure of a Decorator

A decorator has 3 layers:

```python
def my_decorator(func):          # Step 1: Accept function
    def wrapper():               # Step 2: Create wrapper
        print("Before function")
        func()
        print("After function")
    return wrapper               # Step 3: Return wrapper
```

Using it:

```python
@my_decorator
def say_hi():
    print("Hi")

say_hi()
```

### Output:

```
Before function
Hi
After function
```

---

# 4️⃣ What Does @ Symbol Mean?

This:

```python
@my_decorator
def say_hi():
```

Is same as writing:

```python
say_hi = my_decorator(say_hi)
```

The `@` symbol is just a shortcut.

---

# 5️⃣ Decorator With Arguments

If the original function has parameters, the wrapper must also accept them.

```python
def my_decorator(func):
    def wrapper(name):
        print("Before")
        func(name)
        print("After")
    return wrapper

@my_decorator
def greet(name):
    print("Hello", name)

greet("Vinod")
```

---

# 6️⃣ Using *args and **kwargs (Best Practice)

To handle any number of arguments:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper
```

This makes your decorator flexible.

---

# 7️⃣ Real Example – Measuring Execution Time

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Execution time:", end - start)
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    print("Done")

slow_function()
```

---

# 8️⃣ Decorator With Arguments (Advanced)

Sometimes the decorator itself needs parameters.

Example:

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi")

say_hi()
```

---

# 9️⃣ Built-in Decorators in Python

Python provides built-in decorators like:

* `@staticmethod`
* `@classmethod`
* `@property`

Example:

```python
class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return self._age
```

Now we can access `age` like a variable instead of calling a function.

---

# 🔟 Decorators in FastAPI

Since you are learning FastAPI, decorators are very important.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

Here:

```python
@app.get("/")
```

Is a decorator.

It tells FastAPI:

> When someone sends a GET request to "/", run this function.

---

# 1️⃣1️⃣ Flow Diagram (How Decorator Works)

```
Original Function
        ↓
Passed into Decorator
        ↓
Wrapped inside Wrapper
        ↓
New Modified Function Returned
        ↓
Function Call Executes Wrapper
```

---

# 1️⃣2️⃣ Important Interview Points

* Decorators modify functions without changing original code.
* They use nested functions.
* They return a wrapper function.
* `@decorator` is syntactic sugar.
* Always use `*args, **kwargs` in real projects.
* Use `functools.wraps` to preserve original function metadata.

Example:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

# ✅ Final Summary

A decorator is:

* A function
* That takes another function as input
* Adds extra behavior
* Returns a new function
* Without modifying the original function code

---

If you want, I can next explain:

* Decorators deeply with memory diagram
* Closures concept
* Or FastAPI decorator internals
* Or Interview-focused notes

Tell me which level you want (basic / intermediate / advanced).
