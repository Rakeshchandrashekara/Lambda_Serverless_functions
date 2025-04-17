# models.py
from pydantic import BaseModel, Field
from typing import Literal

class FunctionCreate(BaseModel):
    name: str
    route: str
    language: Literal["python", "javascript"]
    timeout: int = Field(..., gt=0, le=30)  # Timeout between 1 and 30 seconds
    code: str

class FunctionResponse(BaseModel):
    id: int
    name: str
    route: str
    language: str
    timeout: int
    code: str

class FunctionUpdate(BaseModel):
    name: str | None = None
    route: str | None = None
    language: Literal["python", "javascript"] | None = None
    timeout: int | None = None
    code: str | None = None
