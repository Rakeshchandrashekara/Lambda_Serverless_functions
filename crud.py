# crud.py
from database import get_db
from models import FunctionCreate, FunctionUpdate
from fastapi import HTTPException

def create_function(func: FunctionCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO functions (name, route, language, timeout, code)
                VALUES (?, ?, ?, ?, ?)
                """,
                (func.name, func.route, func.language, func.timeout, func.code),
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Route already exists")

def get_functions():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM functions")
        return [
            {
                "id": row[0],
                "name": row[1],
                "route": row[2],
                "language": row[3],
                "timeout": row[4],
                "code": row[5],
            }
            for row in cursor.fetchall()
        ]

def get_function(id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM functions WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Function not found")
        return {
            "id": row[0],
            "name": row[1],
            "route": row[2],
            "language": row[3],
            "timeout": row[4],
            "code": row[5],
        }

def update_function(id: int, func: FunctionUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        updates = {k: v for k, v in func.dict().items() if v is not None}
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [id]
        try:
            cursor.execute(f"UPDATE functions SET {set_clause} WHERE id = ?", values)
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Function not found")
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Route already exists")

def delete_function(id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM functions WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Function not found")
