from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from typing import List
from typing import List
from ..models import User, AuthRequest, UpdateUsuari
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
        cursor.execute(f"SELECT * FROM usuari WHERE id = {id};")
        results = cursor.fetchone()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_User_by_id(id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"DELETE FROM usuari WHERE id = {id};")
        conn.commit()
        return {"message": f"Record with id {id} deleted from User."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def create_User(name: str, mail: str, hash: str) -> User:
    if not check_unique_name(name):
        raise HTTPException(status_code=400, detail="User name already exists")
    hash = bcrypt.hashpw(hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO usuari (name,mail, hash)
            VALUES (%s,%s, %s)
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
        cursor.execute("SELECT * FROM usuari WHERE name = %s;", (name,))
        existing_User = cursor.fetchone()
        return existing_User is None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
    if not check_unique_name(name):
        raise HTTPException(status_code=400, detail="User name already exists")
    hash = bcrypt.hashpw(hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        string = "UPDATE usuari SET "
        if name:
            string += f"name = '{name}', "
        if mail:
            string += f"mail = '{mail}', "
        if hash:
            string += f"hash = '{hash}', "
        string = string[:-2] 
        string += f" WHERE id = {id} RETURNING *;"
        cursor.execute(string)
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


        