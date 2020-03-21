import secrets

SECRET_KEY = secrets.token_hex(16)
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = 'postgres://souhaib:123456@localhost:5432/evento'
