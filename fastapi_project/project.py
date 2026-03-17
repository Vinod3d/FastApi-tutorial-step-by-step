from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

app = FastAPI()

class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    description: str = None
    published_date: str = None

@app.post("/books/")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    db_book = model.Book(
        id=book.id,
        title=book.title,
        author=book.author,
        description=book.description,
        published_date=book.published_date
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books}")
def get_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books