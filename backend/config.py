from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', override=True)

class Config:
    DB_INFO = {
        'host': getenv('DB_HOST'),
        'user': getenv('DB_USER'),
        'password': getenv('DB_PASSWORD'),
        'database': getenv('DB_NAME')
    }
    
    COLD_STORAGE = {
        'host': getenv('COLD_STORAGE_HOST'),
        'user': getenv('COLD_STORAGE_USER'),
        'password': getenv('COLD_STORAGE_PASSWORD'),
        'database': getenv('COLD_STORAGE_DBNAME')
    }

