class Config:
    SECRET_KEY = "your_secret_key"
    DB_USER = "dbproject"
    DB_PASSWORD = "dbproject"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "dbproject"

    # Status codes
    STATUS_CODES = {
        'success': 200,
        'api_error': 400,
        'internal_error': 500
    }