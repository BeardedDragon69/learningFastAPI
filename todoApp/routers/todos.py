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



router = APIRouter()


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






class TodoRequest(BaseModel):
       title: str = Field(min_length= 3)
       description: str = Field(min_length = 3)
       priority: int= Field(gt=0 , lt= 6)
       complete: bool


@router.get("/",status_code=status.HTTP_200_OK)

async def readAll(user: userDependency, db: dbDependencyInjection):

       if user is None:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail =" User not authenticated")


       return db.query(Todos).filter(Todos.ownerId == user.get('id')).all()



@router.get("/getTodo/{todoId}", status_code=status.HTTP_200_OK)
async def getTodo(user: userDependency, db: dbDependencyInjection, todoId:int = Path(gt=0)):
        
       if user is None:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "user not found/authenticated")
       else:
              todo = db.query(Todos).filter(Todos.ownerId == user.get('id')).filter(Todos.id == todoId).first()

       if todo is not None:
               return todo
       raise HTTPException(status_code=404, detail= "Todo not found")
       

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def createTodo(user: userDependency,
                     db: dbDependencyInjection,
                       todoRequest: TodoRequest):
      if user is None:
          raise HTTPException(status_code=401, detail="authentication failed")   
      todoModel = Todos(**todoRequest.model_dump(), ownerId = user.get('id'))

      db.add(todoModel) 
      db.commit()


@router.put("/todo/updateTodo/{todoId}", status_code=status.HTTP_202_ACCEPTED)
async def updateTodo(
                     user: userDependency,
                     todoRequest: TodoRequest,
                     db: dbDependencyInjection,
                     todoId:int = Path(gt =0)
                     ):
       
       if user is None:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "user not found/authenticated")
       #first get the todo
       todoModel = db.query(Todos).filter(Todos.ownerId == user.get('id')).filter(Todos.id == todoId).first()
       if todoModel is None:
              raise HTTPException(status_code=404, detail="Not found")
       
       todoModel.title = todoRequest.title
       todoModel.description = todoRequest.description
       todoModel.priority = todoRequest.priority
       todoModel.complete = todoRequest.complete

       db.add(todoModel)
       db.commit()


@router.delete("/todo/deleteTodo/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(user: userDependency,db: dbDependencyInjection, todoId: int = Path(gt=0)):
       if user is None:
              raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")


       foundTodo = db.query(Todos).filter(Todos.ownerId == user.get('id')).filter(Todos.id == todoId).first()

       if foundTodo is None:
              raise HTTPException(status_code=404, detail="Todo not found")
       db.delete(foundTodo)
       db.commit()     
