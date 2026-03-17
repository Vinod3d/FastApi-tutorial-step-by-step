# SQLAlchemy engine create karne ke liye
from sqlalchemy import create_engine

# Database session banane ke liye
from sqlalchemy.orm import sessionmaker

# Base class banane ke liye jisse sabhi models inherit karenge
from sqlalchemy.ext.declarative import declarative_base
import os


# MySQL database username
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root123")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fastapi_db")


# Database connection URL format
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


## Connection
# Engine database connection manager create karta hai
engine = create_engine(DATABASE_URL,
    echo= True,
    pool_pre_ping= True
)


## Session
# SessionLocal database session create karne ke liye factory hai
SessionLocal = sessionmaker(
    autocommit=False,   # changes manually commit karne padenge
    autoflush=False,    # queries automatic flush nahi hongi
    bind=engine         # session ko engine se connect karta hai
)


# Dependency function jo FastAPI routes ko database session provide karta hai
def get_db():
    db = SessionLocal()  # new database session create
    try:
        yield db         # session route ko provide karo
    finally:
        db.close()       # request complete hone par session close


# Base class jisse sabhi SQLAlchemy models inherit karenge
Base = declarative_base()