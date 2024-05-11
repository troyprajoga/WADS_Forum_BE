from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

# - fetch all todos
def get_all_todos(db:Session):
    todo = db.query(models.Todo)
    if todo:
        return todo
    else: raise HTTPException(status_code=404, detail="Todo not found")

# - fetch by id
def get_todo(db:Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if todo:
        return todo
    else: raise HTTPException(status_code=404, detail="Task not found")

# - create todo
def create_todo(db: Session, todo: schemas.Todo):
    db_todo = models.Todo(title = todo.title, completed = todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# - remove all todos
def delete_all_todos(db: Session):
    if db.query(models.Todo).delete():
        db.commit()
        return {"message":"Todos Deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task is empty") 
    
# - remove todo
def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)
    if todo:
        db.delete(todo)
        db.commit()
        return {"message":"Todo Deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for field, value in todo_update.model_dump().items():
        setattr(db_todo, field, value)
    db.commit()
    
    return {"message" : "Todo Updated Successfully"}