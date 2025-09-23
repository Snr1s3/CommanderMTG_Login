from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from typing import List
from typing import List
from ..models import User, AuthRequest, UpdateRequest
import bcrypt

def get_all_Users() -> List[User]:
    Users = general.select_all("User")
    return [User(**p) for p in Users]

def get_User_by_id(id: int) -> User:
    p = general.select_by_id("User", id)
    if p:
        return User(**p)
    else:
        raise HTTPException(status_code=404, detail="User not found")

def delete_User_by_id(id: int) -> dict:
    return general.delete_by_id("User", id)

def create_User(name: str, mail: str, pwd: str) -> User:
    if not check_unique_name(name):
        raise HTTPException(status_code=400, detail="User name already exists")
    hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO User (name,mail, hash)
            VALUES (%s, %s)
            RETURNING *;
        """, (name, mail, hash))
        new_User = cursor.fetchone()
        conn.commit()
        return User(**new_User)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_unique_name(name: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM User WHERE name = %s;", (name,))
        existing_User = cursor.fetchone()
        return existing_User is None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def authenticate_User(name: str, pwd: str) -> User:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM User WHERE name = %s;", (name,))
        results = cursor.fetchone()
        if bcrypt.checkpw(pwd.encode('utf-8'), results['hash'].encode('utf-8')):
            return User(**results)
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update_User_hash(name: str, pwd: str) -> User:
    if not check_unique_name(name):
        raise HTTPException(status_code=400, detail="User name already exists")
    hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            UPDATE User
            SET hash = %s
            WHERE name = %s
            RETURNING *;
        """, (hash, name))
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
        