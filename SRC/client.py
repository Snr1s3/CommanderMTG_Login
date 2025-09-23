from psycopg2 import pool
from .settings import db_config
# Configura la connexió a PostgreSQL

# Pool de connexions
db_pool = pool.SimpleConnectionPool(1, 30, **db_config)
def get_db_connection():
    conn = db_pool.getconn()
    return conn

def release_db_connection(conn):
    db_pool.putconn(conn)
