<style> h1 { color: #fff; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 25px; border-radius: 10px; text-align: center; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); } h2 { color: #fff; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px 20px; border-radius: 8px; border-left: 5px solid #ff1744; box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3); } h3 { color: #667eea; border-left: 4px solid #667eea; padding-left: 15px; } li { color: #444; margin: 12px 0; } li::marker { color: #f5576c; font-weight: bold; } strong { color: #f5576c; font-weight: 600; } code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; color: #c7254e; } pre { background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; } table { border-collapse: collapse; width: 100%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); } th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-bottom: 3px solid #f5576c; } td { padding: 12px 15px; border-bottom: 1px solid #e0e0e0; } tr:hover { background: #f9f9f9; } hr { border: none; height: 3px; background: linear-gradient(to right, #667eea, #764ba2, #f5576c); border-radius: 2px; } blockquote { background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%); border-left: 5px solid #667eea; padding: 20px 25px; border-radius: 8px; } </style>

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

