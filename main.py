# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import FunctionCreate, FunctionResponse, FunctionUpdate
from crud import create_function, get_functions, get_function, update_function, delete_function, execute_function_by_id
from typing import List

app = FastAPI()

class Function(BaseModel):
    name: str
    route: str
    language: str
    timeout: int
    code: str

@app.post("/functions", operation_id="create_function")
async def create_func(function: Function):
    try:
        function_id = await create_function(function)
        return {"id": function_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create function: {str(e)}")

@app.get("/functions", response_model=List[FunctionResponse])
async def list_funcs():
    return get_functions()

@app.get("/functions/{id}", response_model=FunctionResponse)
async def get_func(id: int):
    return get_function(id)

@app.put("/functions/{id}", response_model=dict)
async def update_func(id: int, func: FunctionUpdate):
    update_function(id, func)
    return {"message": "Function updated"}

@app.delete("/functions/{id}", response_model=dict)
async def delete_func(id: int):
    delete_function(id)
    return {"message": "Function deleted"}

@app.post("/functions/{id}/execute", operation_id="execute_function")
async def execute_func(id: int):
    try:
        result = await execute_function_by_id(id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
