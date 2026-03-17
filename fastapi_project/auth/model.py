from sqlalchemy import Column, Integer, String
from .auth_database import Base

class User(Base):
    __tablename__ = "users"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    username = Column(String(255), unique=True, nullable=False)  # Username of the user
    email = Column(String(255), unique=True, nullable=False)     # Email of the user
    hashed_password = Column(String(255), nullable=False)        # Hashed password of the user
    role = Column(String(50), nullable=False)                   # Role of the user (e.g., "user", "admin")