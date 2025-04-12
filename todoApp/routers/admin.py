from fastapi import APIRouter

router = APIRouter()

from fastapi import FastAPI, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine, sessionLocal
from typing import Annotated
from routers import auth
from .auth import get_current_user



router = APIRouter(
       prefix='/admin',
       tags=["admin"]
)


models.Base.metadata.create_all(bind= engine)





#creating db dependency 
'''
Basically creating a dependency is nothing but creating a function 
which will handle something recurring so that i do not have to manually
do it evertime i call an endpoint . In this case create a session with 
the database.
'''

def getDb():
       db = sessionLocal()

       try:
              yield db
       finally:
              db.close()

       
dbDependencyInjection =  Annotated[Session, Depends(getDb)]

#creating a dependency injection for getting the current user of the session
userDependency =  Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def getAllTodos(user: userDependency, db: dbDependencyInjection):
       if user is None and user.get('user_role') != 'admin':
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not an admin")
       print(user.get('user_role'))
       if user.get('user_role') == 'admin':
              return db.query(Todos).all()
       else:
              return f"You are not an admin"
       


@router.delete("/todo/{todoId}", status_code=status.HTTP_202_ACCEPTED)
async def deleteTodo(user: userDependency, db: dbDependencyInjection, todoId:int = Path(gt=0)):
       if user is None and user.get('user_role') != 'admin':
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not an admin")
       print(user.get('user_role'))
       if user.get('user_role') == 'admin':
              foundTodo = db.query(Todos).filter(todoId == Todos.id).first()
       
       if foundTodo is None:
              raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "todo not found")
       
       db.delete(foundTodo)
       db.commit()








