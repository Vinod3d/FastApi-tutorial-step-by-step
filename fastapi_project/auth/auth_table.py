from .auth_database import engine, Base
from .model import User

# Create all tables in the database based on the defined models
Base.metadata.create_all(bind=engine)
print("auth table created successfully.")

