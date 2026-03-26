# Pytest Basics

## What you will learn
- Why `pytest` is the absolute standard for Python testing
- How to structure your tests directory
- Writing your first test functions and asserting values
- Understanding Pytest Fixtures

## Concept (Simple Explanation)
When you build a car, you don't just put it on the highway and hope the brakes work. You put it in a factory simulator, spin the wheels, and hit the brakes programmatically 10,000 times to prove they work.

**Testing** is writing code that runs your *actual* code to prove it behaves exactly as expected. `pytest` is the most popular framework for running these tests in Python. It automatically finds any file starting with `test_` and runs every function inside it starting with `test_`.

## Code Example
**1. Running your first test (`tests/test_math.py`)**
```python
# A simple function simulating your app logic
def add_numbers(a: int, b: int) -> int:
    return a + b

# Pytest will automatically discover this function because it starts with 'test_'
def test_add_numbers_success():
    # 1. Arrange (Setup the data)
    num1 = 5
    num2 = 10
    
    # 2. Act (Run the function)
    result = add_numbers(num1, num2)
    
    # 3. Assert (Prove the result matches reality)
    assert result == 15

def test_add_numbers_negative():
    result = add_numbers(-5, -5)
    assert result == -10
```

**2. Pytest Fixtures**
Sometimes, you need to set up identical data for 50 different tests. Instead of copying and pasting the data setup, you use a **Fixture**. A fixture is a function that gives your test the exact tools it needs to run.

```python
import pytest

# Define the fixture
@pytest.fixture
def mock_user_data():
    return {"id": 1, "username": "vinod", "role": "admin"}

# Simply request the fixture by its exact function name in the arguments!
def test_user_is_admin(mock_user_data):
    # Pytest automatically injects the dictionary into `mock_user_data`
    assert mock_user_data["role"] == "admin"
```

## Best Practices
- **Never put tests inside your `app` folder:** Always keep your tests in a dedicated `tests/` directory at the absolute root of your project. This prevents test files from being deployed to production.
- **Isolate your tests:** If `test_A` requires `test_B` to run first, your tests are broken. Every test should be 100% independent. If you run them in random order, they must all pass.

## Common Mistakes
- **Forgetting the `test_` prefix:** If you name your file `testing_math.py` or your function `verify_addition()`, Pytest will ignore it completely. It strictly looks for `test_` strings.

## Interview Questions
**Q: What is a Pytest Fixture, and why is it useful?**
A: A fixture is a reusable piece of setup logic that Pytest injects into your test functions. It is incredibly useful for setting up complex dependencies (like creating a temporary database or an HTTP client) once, and transparently passing it into dozens of test files without boilerplate code.

**Q: Explain the *Arrange, Act, Assert* pattern.**
A: It is the standard structure for writing tests. *Arrange* sets up the initial variables and conditions. *Act* executes the specific function being tested. *Assert* validates that the output perfectly matches the expected outcome.
