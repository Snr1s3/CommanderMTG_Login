from fastapi import HTTPException
from SRC.routers.checks import check_fields_unique, is_strong_password, is_valid_email
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from typing import List
from typing import List
from ..models import User
import bcrypt

def get_all_Users() -> List[User]:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"SELECT * FROM usuari;")
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_User_by_id(id: int) -> User:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM usuari WHERE id = %s;", (id,))
        results = cursor.fetchone()
        if results is None:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found")
        return User(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def create_User(name: str, mail: str, hash: str) -> User:
    if not name.strip() or not mail.strip() or not hash.strip():
        raise HTTPException(status_code=400, detail="Username or email or password is empty")
    if not is_valid_email(mail):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not is_strong_password(hash):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character")
    if not check_fields_unique(name=name, mail=mail):
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = bcrypt.hashpw(hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO usuari (name, mail, hash)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (name, mail, hashed_password))
        new_User = cursor.fetchone()
        conn.commit()
        return User(**new_User)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def authenticate_User(name: str, hash: str) -> User:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM usuari WHERE name = %s;", (name,))
        results = cursor.fetchone()
        if bcrypt.checkpw(hash.encode('utf-8'), results['hash'].encode('utf-8')):
            return User(**results)
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update_User(id: int, name: str = None, mail: str = None, hash: str = None) -> User:
    if mail and not is_valid_email(mail):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if hash and not is_strong_password(hash):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character")
    
    fields_to_check = {}
    if name:
        fields_to_check['name'] = name
    if mail:
        fields_to_check['mail'] = mail
    
    if fields_to_check and not check_fields_unique(**fields_to_check):
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = None
    if hash:
        hashed_password = bcrypt.hashpw(hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        update_fields = []
        values = []
        
        if name:
            update_fields.append("name = %s")
            values.append(name)
        if mail:
            update_fields.append("mail = %s") 
            values.append(mail)
        if hashed_password:
            update_fields.append("hash = %s")
            values.append(hashed_password)
            
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")
            
        values.append(id)  # Add id for WHERE clause
        
        query = f"UPDATE usuari SET {', '.join(update_fields)} WHERE id = %s RETURNING *;"
        cursor.execute(query, values)
        
        updated_User = cursor.fetchone()
        conn.commit()
        
        if updated_User:    
            return User(**updated_User)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_User_by_id(id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("DELETE FROM usuari WHERE id = %s;", (id,))
        rows_affected = cursor.rowcount
        conn.commit()
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found")
        return {"message": f"Record with id {id} deleted from User."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)