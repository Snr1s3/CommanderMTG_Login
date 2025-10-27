from fastapi import HTTPException
from SRC.services.checks import *
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from typing import List
from typing import List
from ..models.usuaris import Usuari
import bcrypt


class UsuariService:
    
    def get_all_Usuaris(self) -> List[Usuari]:
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

    def get_Usuari_by_id(self, id: int) -> Usuari:
        validate_id(id)
    
        if not check_id("usuari", id):
            raise HTTPException(status_code=404, detail=f"Record with id {id} not found")
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM usuari WHERE id = %s;", (id,))
            results = cursor.fetchone()
            if results is None:
                raise HTTPException(status_code=404, detail=f"Usuari with id {id} not found")
            return Usuari(**results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            release_db_connection(conn)

    def create_Usuari(self, name: str, mail: str, hash: str) -> Usuari:
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Username cannot be empty")
        if not mail or not mail.strip():
            raise HTTPException(status_code=400, detail="Email cannot be empty")
        if not hash or not hash.strip():
            raise HTTPException(status_code=400, detail="Password cannot be empty")
            
        if not is_valid_email(mail):
            raise HTTPException(status_code=400, detail="Invalid email format")
        if not is_strong_password(hash):
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character")
        if not check_fields_unique(name=name.strip(), mail=mail.strip()):
            raise HTTPException(status_code=409, detail="Username or email already exists")
        
        try:
            hashed_password = bcrypt.hashpw(hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to encrypt password")
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                INSERT INTO usuari (name, mail, hash)
                VALUES (%s, %s, %s)
                RETURNING *;
            """, (name.strip(), mail.strip(), hashed_password))
            conn.commit()
            new_Usuari = cursor.fetchone()
            return Usuari(**new_Usuari)
        except Exception as e:
            conn.rollback()
            error_str = str(e).lower()
            if 'unique constraint' in error_str or 'duplicate key' in error_str:
                raise HTTPException(status_code=409, detail="Username or email already exists")
            elif 'foreign key constraint' in error_str:
                raise HTTPException(status_code=400, detail="Referenced record does not exist")
            elif 'not null constraint' in error_str:
                raise HTTPException(status_code=400, detail="Required field is missing")
            elif 'check constraint' in error_str:
                raise HTTPException(status_code=400, detail="Data validation failed")
            elif 'value too long' in error_str:
                raise HTTPException(status_code=400, detail="Input data too long")
            else:
                raise HTTPException(status_code=500, detail="Failed to create user")
        finally:
            cursor.close()
            release_db_connection(conn)

    def authenticate_Usuari(self, name: str, hash: str) -> Usuari:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM usuari WHERE name = %s;", (name,))
            results = cursor.fetchone()
            if bcrypt.checkpw(hash.encode('utf-8'), results['hash'].encode('utf-8')):
                return Usuari(**results)
            else:
                raise HTTPException(status_code=400, detail="Invalid credentials")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            release_db_connection(conn)

    def delete_Usuari_by_id(self, id: int) -> dict:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("DELETE FROM usuari WHERE id = %s;", (id,))
            rows_affected = cursor.rowcount
            conn.commit()
            if rows_affected == 0:
                raise HTTPException(status_code=404, detail=f"Usuari with id {id} not found")
            return {"message": f"Record with id {id} deleted from Usuari."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            release_db_connection(conn)

def update_Usuari(self, id: int, update_data) -> Usuari:
    if id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    name = getattr(update_data, 'name', None)
    mail = getattr(update_data, 'mail', None)
    hash = getattr(update_data, 'hash', None)
    
    if name is not None and (not name.strip() or len(name.strip()) > 255):
        raise HTTPException(status_code=400, detail="Invalid username")
    if mail is not None and (not mail.strip() or len(mail.strip()) > 255):
        raise HTTPException(status_code=400, detail="Invalid email")
    if hash is not None and not hash.strip():
        raise HTTPException(status_code=400, detail="Password cannot be empty")
        
    if mail and not is_valid_email(mail):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if hash and not is_strong_password(hash):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character")
    
    # Check uniqueness for fields being updated
    fields_to_check = {}
    if name:
        fields_to_check['name'] = name.strip()
    if mail:
        fields_to_check['mail'] = mail.strip()
    
    if fields_to_check and not check_fields_unique(**fields_to_check):
        raise HTTPException(status_code=409, detail="Username or email already exists")
    
    # Hash password if provided
    hashed_password = None
    if hash:
        try:
            hashed_password = bcrypt.hashpw(hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        except Exception:
            raise HTTPException(status_code=500, detail="Password encryption failed")
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        update_fields = []
        values = []
        
        if name:
            update_fields.append("name = %s")
            values.append(name.strip())
        if mail:
            update_fields.append("mail = %s") 
            values.append(mail.strip())
        if hashed_password:
            update_fields.append("hash = %s")
            values.append(hashed_password)
            
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")
            
        values.append(id)
        
        query = f"UPDATE usuari SET {', '.join(update_fields)} WHERE id = %s RETURNING *;"
        cursor.execute(query, values)
        
        updated_Usuari = cursor.fetchone()
        conn.commit()
        
        if updated_Usuari:    
            return Usuari(**updated_Usuari)
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        error_str = str(e).lower()
        if 'unique constraint' in error_str or 'duplicate key' in error_str:
            raise HTTPException(status_code=409, detail="Username or email already exists")
        else:
            raise HTTPException(status_code=500, detail="Failed to update user")
    finally:
        cursor.close()
        release_db_connection(conn)