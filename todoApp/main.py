from fastapi import FastAPI

import models

from database import engine

from routers import auth, todos, admin, user


# from todoApp.routers import auth



app = FastAPI(
       title="My todoApp Api",
       description="Adding dark mode to swagger ui",
       version= "1.0",
       swagger_ui_parameters={"theme": "dark"}
)



models.Base.metadata.create_all(bind= engine)


 #auth file name router is the name of the variable
app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)




              