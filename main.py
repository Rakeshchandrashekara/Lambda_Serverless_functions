# main.py
from fastapi import FastAPI, HTTPException
from models import FunctionCreate, FunctionResponse, FunctionUpdate
from crud import create_function, get_functions, get_function, update_function, delete_function
from typing import List

app = FastAPI()

@app.post("/functions", response_model=dict)
async def create_func(func: FunctionCreate):
    func_id = create_function(func)
    return {"id": func_id}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
