from database import engine, Base
from model import Book

# Create all tables in the database based on the defined models
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")

