from typing import Union
from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, description="The updated title of the todo")
    completed: Optional[bool] = Field(None, description="The updated completion status of the todo")