# CI/CD: GitHub Actions

## What you will learn
- What Continuous Integration (CI) and Continuous Deployment (CD) mean
- Automating your unit tests using GitHub Actions
- Preventing broken code from ever being deployed
- Writing a production-ready `.yml` workflow

## Concept (Simple Explanation)
Imagine you write some code, it works on your laptop, and you push it to GitHub. You tell the server to pull the code and restart. Suddenly, the entire company goes down because you forgot a single comma.

**CI/CD** is a robotic QA tester. Every time you push code to GitHub:
1. GitHub intercepts the code.
2. It spins up a temporary virtual server.
3. It runs `pytest`.
4. If the tests pass, the code is allowed to merge. 
5. If a test fails, a giant red X appears, and the deployment is physically blocked.

## Code Example
**`.github/workflows/tests.yml`**
Create this file in your repository to automatically run tests on every push to the `main` branch.

```yaml
name: FastAPI Automated Tests

# 1. When should this run?
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    # 2. What OS should the GitHub robot use?
    runs-on: ubuntu-latest

    # 3. What steps should the robot take?
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v3

    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        # Install pytest explicitly if it isn't in your requirements
        pip install pytest pytest-cov 

    - name: Run Pytest Coverage
      run: |
        # Tells pytest to test everything and fail if coverage is under 80%
        pytest --cov=app --cov-fail-under=80 tests/
```

## Best Practices
- **Add Linting (Ruff / Flake8):** Before running Pytest, you should run a Linter. A linter checks your code for badly formatted lines, unused imports, or syntax errors, and blocks the merge before tests even execute.
- **Fail strict on Coverage:** Adding `--cov-fail-under=80` forces developers on your team to actually write tests for their new features. If they push a massive new API route without testing it, the GitHub Action will fail the build immediately.

## Common Mistakes
- **Putting secret `.env` variables in GitHub Actions:** Never paste real database passwords into your `tests.yml`. If your tests require secure secrets to run, you must inject them securely using GitHub Repository Secrets (`${{ secrets.DATABASE_URL }}`).

## Interview Questions
**Q: How does Continuous Integration (CI) differ from Continuous Deployment (CD)?**
A: **CI** is the automated process of frequently merging code from multiple developers into a central repository, instantly building and running test suites to ensure the integration didn't break existing functionality. **CD** takes the successfully integrated code and automatically deploys it directly to staging or production servers (or automatically builds and pushes the Docker container) without human intervention.
