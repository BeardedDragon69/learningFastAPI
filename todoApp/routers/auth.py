from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import sessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

import os
from dotenv import load_dotenv


# load all the env files

load_dotenv("key.env")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# print(SECRET_KEY)


if SECRET_KEY  is None:
    raise ValueError("Secret key is not set in environment variable")


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashedPassword):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + expires_delta
        }
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)






async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    # print(SECRET_KEY)
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  #, options={"verify_exp": False}    --you can add this to the jwt decode as an argument to decode stuff
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    
    except JWTError:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        firstName=create_user_request.first_name,
        lastName=create_user_request.last_name,
        role=create_user_request.role,
        hashedPassword=bcrypt_context.hash(create_user_request.password),
        isActive=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}