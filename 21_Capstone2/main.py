from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message" : "Hello world"}

@app.get("/greet")
def greet():
    return {"Message" : "Hello Sam"}

@app.get("/greet/{name}")
def greet_name(name: str, age: Optional[int]=None):
    return {"Message": f"Hello {name} and you are {age} years old"}

class Student(BaseModel):
    name: str
    age: int
    roll: int

@app.post("/create_student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "roll": student.roll
    }

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )