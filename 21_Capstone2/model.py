from sqlalchemy import VARCHAR, Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = "books"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    title = Column(String(255), nullable=False)         # Title of the book
    author = Column(String(255), nullable=False)        # Author of the book
    description = Column(String(500))                    # Description of the book (optional)
    published_date = Column(VARCHAR(10))                 # Published date in YYYY-MM-DD format (optional)