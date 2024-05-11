from fastapi import FastAPI, HTTPException, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
import crud, models, schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind = engine)

origins = [
    "http://localhost:5173",
    "localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

todos = {}

# To do methods
# - fetch all todos
@app.get('/getalltodos')
def get_all_todos(db: Session = Depends(get_db)):
    return crud.get_all_todos(db)

# - fetch by id
@app.get('/todos/{todo_id}')
def get_todo(todo_id: int,db: Session = Depends(get_db)):
    return crud.get_todo(db,todo_id)

# - post new todo
@app.post('/todos/new')
def post_todo(todo: schemas.Todo,db: Session = Depends(get_db)):
    return crud.create_todo(db,todo)

# - remove all todos
@app.delete('/deletealltodos')
def delete_all_todos(db: Session = Depends(get_db)):
    return crud.delete_all_todos(db)

# - remove todo

@app.delete("/todos/delete/{todo_id}")
def delete_todo(todo_id: int,db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)

# - updates todo
@app.put("/updateTodo/{todo_id}")
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    updated_todo = crud.update_todo(db, todo_id, todo_update)
    return updated_todo
