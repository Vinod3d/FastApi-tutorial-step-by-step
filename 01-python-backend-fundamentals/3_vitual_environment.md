

# 🚀 Chapter 1.3 Virtual Environment, Package Management & Project Structure


## 1. Why Virtual Environment is Needed?

When working on backend projects:

* Project A may need FastAPI 0.95
* Project B may need FastAPI 0.110
* Some project needs older version of a library

If everything is installed globally → version conflicts happen.

### Solution → Virtual Environment

A virtual environment creates an isolated Python environment for each project.



## 2. Creating Virtual Environment (venv)

### Create venv

```bash
python -m venv venv
```

### Activate (Windows)

```bash
venv\Scripts\activate
```

### Activate (Mac/Linux)

```bash
source venv/bin/activate
```

### Deactivate

```bash
deactivate
```

## 3. What Happens Internally?

When you create venv:

* It copies Python interpreter
* Creates separate site-packages folder
* Installs packages only inside that environment

This prevents global pollution.


## 4. pip (Package Installer for Python)

### Install package

```bash
pip install fastapi
```

### Uninstall

```bash
pip uninstall fastapi
```

### Check installed packages

```bash
pip list
```

---

## 5. requirements.txt

To share project with others:

```bash
pip freeze > requirements.txt
```

To install dependencies:

```bash
pip install -r requirements.txt
```

### Interview Question:

Why requirements.txt is important?

It ensures reproducibility of project dependencies.




## 6. How Python Executes a File

When you run:

```bash
python main.py
```

Python:

1. Compiles to bytecode (.pyc)
2. Executes line by line
3. Creates global namespace



## 7. Python Project Structure (Backend Standard)

Small project:

```
project/
│
├── main.py
├── requirements.txt
└── venv/
```



Production-level FastAPI project:

```
project/
│
├── app/
│   ├── main.py
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── core/
│
├── tests/
├── requirements.txt
└── venv/
```

Why structured project is important?

* Clean architecture
* Separation of concerns
* Maintainability
* Scalability

## 🎯 Interview Rapid Fire Questions

1. Why do we need virtual environment?
2. Difference between pip and poetry?
3. What is requirements.txt?
4. What is **name**?
5. How does Python import system work?
6. What happens when we run python file?
7. What is PYTHONPATH?

You must answer these confidently.

