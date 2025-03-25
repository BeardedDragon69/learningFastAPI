# from datetime import datetime, timedelta, timezone
# from typing import Annotated
# from fastapi import Depends, APIRouter, status, HTTPException
# from pydantic import BaseModel
# from models import Users
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from database import sessionLocal
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from jose import jwt, JWTError
# import jwt

# # app = FastAPI() instead of this we have to write the line below 

# router = APIRouter(
#        prefix='/auth',
#        tags=['auth']
# )

# # For the JWT to work, create a secret key and algorithm
# secretKey = 'a7a0dcb6a3adea2df22260da47d3db09f57994762022083150a4c21daa4497c1'
# Algorithm = 'HS256'

# # Database session dependency
# def getDb():
#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# dbDependencyInjection = Annotated[Session, Depends(getDb)]

# # Password hashing setup
# bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

# # OAuth2 token authentication
# oAuth2Bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

# # Create a user BaseModel for input validation
# class CreateUser(BaseModel):
#     username: str
#     firstName: str
#     lastName: str
#     password: str
#     email: str
#     role: str

# class Token(BaseModel):
#     accessToken: str
#     tokenName: str

# # Function to authenticate a user
# def authenticateUser(username: str, password: str, db: Session):
#     user = db.query(Users).filter(Users.username == username).first()
#     if not user or not bcryptContext.verify(password, user.hashedPassword):
#         return False
#     return user



# # Function to create a JWT access token
# def createAccessToken(userName: str, userId: int, expiresDelta: timedelta):
#     encode = {
#         'sub': userName,
#         'id': userId,
#         'exp': int((datetime.now(timezone.utc) + expiresDelta).timestamp())  # ✅ FIXED: exp is already an int
#     }
#     return jwt.encode(encode, secretKey, algorithm=Algorithm)  # ✅ FIXED: Ensure 'algorithm' is lowercase

# # Function to create a JWT access token using PyJWT
# def createNewAccessToken(userName: str, userId: int, expiresDelta: timedelta):
#     payload = {
#         'sub': userName,
#         'id': userId,
#         'exp': int((datetime.now(timezone.utc) + expiresDelta).timestamp())  # ✅ FIXED: exp is already an int
#     }
#     return jwt.encode(payload, secretKey, algorithm=Algorithm)  # ✅ FIXED: Ensure 'algorithm' is lowercase


# # Function to get the current authenticated user
# async def getCurrentUser(token: Annotated[str, Depends(oAuth2Bearer)]):
# #     try:
#         payload = jwt.decode(token, secretKey, algorithms=[Algorithm])
#         userName: str = payload.get('sub')
#         userId: int = payload.get('id')

#         if userName is None or userId is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="User cannot be verified")
#         return {'username': userName, 'id': userId}

# #     except JWTError:  # ✅ FIX: Catch and handle JWT errors properly
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
# #                             detail="Invalid token or expired session")

# # Endpoint to create a new user
# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def createUser(createUser: CreateUser, db: dbDependencyInjection):
#     newUser = Users(
#         email=createUser.email,
#         username=createUser.username,
#         firstName=createUser.firstName,
#         lastName=createUser.lastName,
#         role=createUser.role,
#         hashedPassword=bcryptContext.hash(createUser.password),
#         isActive=True
#     )

#     db.add(newUser)
#     db.commit()
#     db.refresh(newUser)  # ✅ FIX: Ensure user data is refreshed after commit

#     return {"message": "User created successfully"}

# # Endpoint to log in and get an access token
# @router.post("/token", response_model=Token)
# async def loginAcessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependencyInjection):
#     user = authenticateUser(formData.username, formData.password, db)
#     if not user:
#         raise HTTPException(status_code=400, detail='Invalid username or password')

#     token = createAccessToken(user.username, user.id, timedelta(minutes=5))
#     print("Generated Token:", token)  # ✅ DEBUG: Print generated token for verification

#     return {'accessToken': token, 'tokenName': 'bearer'}

# # Endpoint to fetch the currently authenticated user
# @router.get("/me")
# async def getCurrentUserDetails(currentUser: Annotated[dict, Depends(getCurrentUser)], db: dbDependencyInjection):
#     """Fetch the currently authenticated user using the getCurrentUser function."""
#     user = db.query(Users).filter(Users.username == currentUser["username"]).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     return {
#         "username": user.username,
#         "userId": user.id,
#         "email": user.email,
#         "firstName": user.firstName,
#         "lastName": user.lastName,
#         "role": user.role
#     }

# # Endpoint to get user details by username
# @router.get("/getuser/{userName}")
# async def getUser(userName: str, db: dbDependencyInjection):
#     foundUser = db.query(Users).filter(Users.username == userName).first()

#     if foundUser:
#         return foundUser
#     else:
#         raise HTTPException(status_code=404, detail="User not found")  # ✅ FIX: Use HTTPException for consistency


''' Version 2 from Chatgpt'''

# from datetime import datetime, timedelta, timezone
# from typing import Annotated
# from fastapi import Depends, APIRouter, status, HTTPException
# from pydantic import BaseModel
# from models import Users
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from database import sessionLocal
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from jose import jwt, JWTError  # ✅ Ensure only python-jose is used

# # Setup FastAPI Router
# router = APIRouter(
#        prefix='/auth',
#        tags=['auth']
# )

# # JWT Configuration
# SECRET_KEY = 'a7a0dcb6a3adea2df22260da47d3db09f57994762022083150a4c21daa4497c1'
# ALGORITHM = 'HS256'

# # Database session dependency
# def getDb():
#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# dbDependencyInjection = Annotated[Session, Depends(getDb)]

# # Password Hashing
# bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

# # OAuth2 Authentication
# oAuth2Bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

# # User Input Models
# class CreateUser(BaseModel):
#     username: str
#     firstName: str
#     lastName: str
#     password: str
#     email: str
#     role: str

# class Token(BaseModel):
#     accessToken: str
#     tokenName: str

# # Authenticate User
# def authenticateUser(username: str, password: str, db: Session):
#     user = db.query(Users).filter(Users.username == username).first()
#     if not user or not bcryptContext.verify(password, user.hashedPassword):
#         return False
#     return user

# # ✅ FIX: Create JWT Access Token (python-jose)
# def createAccessToken(userName: str, userId: int, expiresDelta: timedelta):
#     expiration = datetime.now(timezone.utc) + expiresDelta  # ✅ FIX: Use datetime directly
#     encode = {
#         'sub': userName,
#         'id': userId,
#         'exp': expiration
#     }
#     token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)  # ✅ FIX: Use SECRET_KEY
#     print("Generated Token:", token)  # ✅ DEBUG: Print to check if token is generated correctly
#     return token

# # ✅ FIX: Improved Function to Get Current User
# async def getCurrentUser(token: Annotated[str, Depends(oAuth2Bearer)]):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # ✅ FIX: Use SECRET_KEY
#         userName: str = payload.get('sub')
#         userId: int = payload.get('id')

#         if userName is None or userId is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
#         return {'username': userName, 'id': userId}
#     except JWTError as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")

# # ✅ FIX: Create User Endpoint
# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def createUser(createUser: CreateUser, db: dbDependencyInjection):
#     newUser = Users(
#         email=createUser.email,
#         username=createUser.username,
#         firstName=createUser.firstName,
#         lastName=createUser.lastName,
#         role=createUser.role,
#         hashedPassword=bcryptContext.hash(createUser.password),
#         isActive=True
#     )

#     db.add(newUser)
#     db.commit()
#     db.refresh(newUser)  # ✅ Ensure user data is refreshed after commit

#     return {"message": "User created successfully"}

# # ✅ FIX: Login Endpoint
# @router.post("/token", response_model=Token)
# async def loginAcessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependencyInjection):
#     user = authenticateUser(formData.username, formData.password, db)
#     if not user:
#         raise HTTPException(status_code=400, detail='Invalid username or password')

#     token = createAccessToken(user.username, user.id, timedelta(minutes=5))
#     print("Generated Token:", token)  # ✅ DEBUG: Print generated token

#     return {'accessToken': token, 'tokenName': 'bearer'}

# # ✅ FIX: Fetch Current User
# @router.get("/me")
# async def getCurrentUserDetails(currentUser: Annotated[dict, Depends(getCurrentUser)], db: dbDependencyInjection):
#     user = db.query(Users).filter(Users.username == currentUser["username"]).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     return {
#         "username": user.username,
#         "userId": user.id,
#         "email": user.email,
#         "firstName": user.firstName,
#         "lastName": user.lastName,
#         "role": user.role
#     }

# # ✅ FIX: Get User by Username
# @router.get("/getuser/{userName}")
# async def getUser(userName: str, db: dbDependencyInjection):
#     foundUser = db.query(Users).filter(Users.username == userName).first()

#     if foundUser:
#         return foundUser
#     else:
#         raise HTTPException(status_code=404, detail="User not found")  # ✅ FIX: Use HTTPException

'''My Version with the role added in jwt'''


from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter, status, HTTPException, Path
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import sessionLocal
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

# app = FastAPI() instead of this we have to write the line below 

router = APIRouter(
       prefix='/auth',
       tags=['auth']

)


#for the jwt to work create a secret key and algorithm

secretKey = 'a7a0dcb6a3adea2df22260da47d3db09f57994762022083150a4c21daa4497c1'
algorithm = 'HS256'

def getDb():
       db = sessionLocal()

       try:
              yield db
       finally:
              db.close()

       
dbDependencyInjection =  Annotated[Session, Depends(getDb)]

bcryptContext = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oAuth2Bearer = OAuth2PasswordBearer(tokenUrl='auth/token')





#create a user basemodel for input validation

class CreateUser(BaseModel):
       username: str
       firstName: str
       lastName: str
       password: str
       email: str
       role: str

class Token(BaseModel):
       accessToken: str
       tokenName: str

def authenticateUser(username:str, password: str, db):
       user = db.query(Users).filter(Users.username == username).first()
       if not user: 
              return False
       if not bcryptContext.verify(password,user.hashedPassword):
              return False
       return user


def createAcessToken(userName: str, userId: int, role: str, expiresDelta: timedelta):
       encode = {'sub': userName, 'id': userId, 'role':role}
       expires = datetime.now(timezone.utc) + expiresDelta
       encode.update({'exp':expires})
       return jwt.encode(encode,secretKey,algorithm=algorithm)


async def getCurrentUser(token: Annotated[str, Depends(oAuth2Bearer)]):
       # try:
              payload = jwt.decode(token, secretKey, algorithms=algorithm)
              userName: str = payload.get('sub')
              userId : int = payload.get('id')

              if userName is None or userId is None:
                     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="User cannot be verified")
              return{'username':userName, 'id':userId}
              
       # except JWTError:
       #        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
       #                                   detail="User cannot be verified")



@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(createUser: CreateUser, db: dbDependencyInjection):
       createUser = Users(
              email = createUser.email,
              username = createUser.username,
              firstName =  createUser.firstName,
              lastName = createUser.lastName,
              role = createUser.role,
              hashedPassword = bcryptContext.hash(createUser.password),
              isActive = True
       )

       db.add(createUser)
       db.commit()



@router.post("/token", response_model= Token)
async def loginAcessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()],
                          db: dbDependencyInjection):
       

       user = authenticateUser(formData.username, formData.password, db)
       if not user:
              raise HTTPException(status_code=400, detail='Invalid Username or password')
       
       token = createAcessToken(user.username,user.id, user.role, timedelta(minutes=5))
       print ("Generated Token:", token)

       return {'accessToken':token,'tokenName':'bearer'}


@router.get("/me")
async def getCurrentUserDetails(currentUser: Annotated[str, Depends(getCurrentUser)], db: dbDependencyInjection):
    """Fetch the currently authenticated user using the getCurrentUser function."""
    user = db.query(Users).filter(Users.username == currentUser["username"]).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "username": user.username,
        "userId": user.id,
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "role": user.role
    }










@router.get("/getuser/{userName}")
async def getUser(userName: str, db:dbDependencyInjection):
       foundUser = db.query(Users).filter(Users.username == userName).first()

       if foundUser:
              return foundUser
       else:
              return "user not found"