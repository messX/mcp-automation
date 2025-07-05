import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
    JSON_SORT_KEYS = False