from fastapi import FastAPI

import models

from database import engine

from routers import auth, todos
# from todoApp.routers import auth



app = FastAPI()


models.Base.metadata.create_all(bind= engine)


# app.include_router(auth.router) #auth file name router is the name of the variable
app.include_router(todos.router)
app.include_router(auth.router)





              