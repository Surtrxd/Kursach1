import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://user:password@localhost/education_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
