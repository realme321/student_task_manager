import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'ssl_ca': os.path.join(BASE_DIR, 'ca.pem'),
    'ssl_verify_cert': True
}