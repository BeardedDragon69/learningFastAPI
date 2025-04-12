from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import sessionLocal, engine
import models
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .auth import get_current_user

import os

oauth2Bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")





router = APIRouter(
       prefix='/users',
       tags=['users']
)


models.Base.metadata.create_all(bind= engine)

def getDb():
       db = sessionLocal()

       try: 
              yield db
       finally:
              db.close


dbDependencyInjection = Annotated[(Session, Depends(getDb))]


@router.get("/currentUserDetails", status_code=status.HTTP_202_ACCEPTED)
async def getUserDetails(db: dbDependencyInjection,token: Annotated[str, Depends(oauth2Bearer)]):
       currentUser = await get_current_user(token)

       payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       username: str = payload.get('sub')
       userId: str = payload.get('id')
       userRole: str = payload.get('role')




       if currentUser is None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is either not logged in or not found")
       
       else:
              print("The user is found and logged in")

              return {"username":username, 
                      "userId": userId,
                      "userRole": userRole}
       









