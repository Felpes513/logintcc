from contextlib import contextmanager
import pymysql

# CONFIGURAÇÕES DO BANCO (idealmente virão de variáveis de ambiente)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1404",
    "database": "db_uscs_ic",
}

@contextmanager
def db_connection():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def get_db_conn():
    with db_connection() as conn:
        yield conn