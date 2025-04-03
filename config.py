import os

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Natz0418'
MYSQL_DB = 'MentalBalance'
MYSQL_CURSORCLASS = 'DictCursor'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-temporal-compleja-y-segura'