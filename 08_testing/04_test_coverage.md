# Test Coverage

## What you will learn
- What "Test Coverage" actually means
- Installing and using `pytest-cov`
- Reading coverage reports to find untested lines
- The industry standard coverage percentage goal

## Concept (Simple Explanation)
You wrote 10 tests, and they all pass! But does that mean your app is 100% bug-free? No. Maybe your 10 tests only checked the `users` file, and entirely ignored the `products` file.

**Test Coverage** is a tool that watches your tests run and highlights exactly which physical lines of Python code were executed. If you have an `if / else` block in your code, and your tests only trigger the `if` condition, the coverage tool will literally highlight the `else` block in red and say: *"Warning: This code was never tested!"*

## Code Example
**1. Install Pytest Coverage**
```bash
pip install pytest-cov
```

**2. Run your tests with the Coverage Flag**
```bash
# --cov=app tells it to watch your "app" folder
pytest --cov=app tests/
```

**3. Output Example**
```text
Name                  Stmts   Miss  Cover
-----------------------------------------
app/main.py              20      0   100%
app/routers/users.py     40     10    75%
app/database.py          12      2    83%
-----------------------------------------
TOTAL                    72     12    83%
```
This tells you that your project is 83% tested. The `users.py` file missed 10 lines of code entirely during the test run!

**4. Generate an HTML Report (Visualizing the missing code)**
```bash
pytest --cov=app --cov-report=html tests/
```
This creates an `htmlcov/` folder. If you open `htmlcov/index.html` in your web browser, it will physically show your code, highlighting tested lines in green and untested lines in red!

## Best Practices
- **Aim for ~80% Coverage:** Getting 100% coverage often requires writing useless, time-wasting tests just to hit obscure lines of framework setup code. Targeting 80% ensures all core business logic is tested without wasting immense engineering hours.
- **Run Coverage in CI/CD:** When you push your code to GitHub, GitHub Actions should automatically run `pytest --cov`. If a developer submits a Pull Request that drops the coverage below 80%, GitHub should automatically reject the code.

## Common Mistakes
- **Assuming 100% Coverage means 0% Bugs:** You can write a test that executes a line of code, but you forgot to write an `assert` statement to prove the output was correct. The coverage tool marks the line as "tested," but you proved nothing. Coverage proves execution, not logical correctness.

## Interview Questions
**Q: What is a "Missed Statement" in a pytest-cov report?**
A: A missed statement is a line of executable code in the application that was never reached or executed during the entire execution lifecycle of the test suite.

**Q: Should you mandate 100% test coverage in a production application?**
A: Usually, no. The Pareto Principle applies: the last 15% of coverage often requires 80% of the testing effort (e.g., trying to force highly specific database connection timeouts). It is better to have 85% high-quality, logic-asserting coverage than 100% meaningless coverage.
