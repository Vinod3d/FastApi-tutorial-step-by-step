import secrets

SECRET_KEY = secrets.token_urlsafe(32)
print("Generated Secret Key:", SECRET_KEY)