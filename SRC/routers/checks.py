import re
from fastapi import HTTPException
from SRC.client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_special = re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\?]', password) is not None
    
    return has_upper and has_lower and has_digit and has_special

def check_fields_unique(name: str = None, mail: str = None, hash: str = None) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        if name:
            cursor.execute("SELECT id FROM usuari WHERE name = %s;", (name,))
            if cursor.fetchone() is not None:
                return False
                
        if mail:
            cursor.execute("SELECT id FROM usuari WHERE mail = %s;", (mail,))
            if cursor.fetchone() is not None:
                return False
                
        if hash:
            cursor.execute("SELECT id FROM usuari WHERE hash = %s;", (hash,))
            if cursor.fetchone() is not None:
                return False
        
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)