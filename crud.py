# crud.py
import sqlite3
import subprocess
import tempfile	
import os
from pydantic import BaseModel
import asyncio
from database import get_db
from models import FunctionCreate, FunctionUpdate
from fastapi import HTTPException

class Function(BaseModel):
    name: str
    route: str
    language: str
    timeout: int
    code: str

def get_db_connection():
    conn = sqlite3.connect("functions.db")
    conn.row_factory = sqlite3.Row
    return conn

async def create_function(function: Function):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO functions (name, route, language, timeout, code) VALUES (?, ?, ?, ?, ?)",
            (function.name, function.route, function.language, function.timeout, function.code)
        )
        conn.commit()
        function_id = cursor.lastrowid
        conn.close()
        return function_id
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Route '{function.route}' already exists")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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

async def execute_function_by_id(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM functions WHERE id = ?", (id,))
    func = cursor.fetchone()
    conn.close()

    if func is None:
        raise HTTPException(status_code=404, detail="Function not found")

    language = func["language"]
    code = func["code"]
    timeout = func["timeout"]

    temp_file_path = None
    try:
        if language == "python":
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name
            process = await asyncio.create_subprocess_exec(
                "python", temp_file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                if process.returncode != 0:
                    raise HTTPException(status_code=500, detail=f"Execution error: {stderr.decode()}")
                return {"result": stdout.decode()}
            except asyncio.TimeoutError:
                process.terminate()
                return {"detail": "Function execution timed out"}

        elif language == "javascript":
            with tempfile.NamedTemporaryFile(suffix=".js", delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name
            process = await asyncio.create_subprocess_exec(
                "node", temp_file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                if process.returncode != 0:
                    raise HTTPException(status_code=500, detail=f"Execution error: {stderr.decode()}")
                return {"result": stdout.decode()}
            except asyncio.TimeoutError:
                process.terminate()
                return {"detail": "Function execution timed out"}

        else:
            raise HTTPException(status_code=400, detail="Unsupported language")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass

async def execute_function_by_id(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM functions WHERE id = ?", (id,))
    func = cursor.fetchone()
    conn.close()

    if func is None:
        raise HTTPException(status_code=404, detail="Function not found")

    language = func["language"]
    code = func["code"]
    timeout = func["timeout"]

    temp_file_path = None
    try:
        if language == "python":
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name
            process = await asyncio.create_subprocess_exec(
                "python", temp_file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                if process.returncode != 0:
                    raise HTTPException(status_code=500, detail=f"Execution error: {stderr.decode()}")
                return {"result": stdout.decode()}
            except asyncio.TimeoutError:
                process.terminate()
                return {"detail": "Function execution timed out"}

        elif language == "javascript":
            with tempfile.NamedTemporaryFile(suffix=".js", delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name
            process = await asyncio.create_subprocess_exec(
                "node", temp_file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                if process.returncode != 0:
                    raise HTTPException(status_code=500, detail=f"Execution error: {stderr.decode()}")
                return {"result": stdout.decode()}
            except asyncio.TimeoutError:
                process.terminate()
                return {"detail": "Function execution timed out"}

        else:
            raise HTTPException(status_code=400, detail="Unsupported language")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass
