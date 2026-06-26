import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'indian_art_collective_secret_2025')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root123')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'indian_art_collective')
    MYSQL_CURSORCLASS = 'DictCursor'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    JWT_EXPIRY_HOURS = 24
