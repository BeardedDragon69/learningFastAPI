from database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


Base.metadata.create_all(bind=engine)

class Users(Base):
       __tablename__ = 'users' 

       id = Column(Integer, primary_key=True, index= True)
       username = Column(String, unique=True)
       email = Column(String, unique=True)
       firstName = Column(String)
       lastName = Column(String)
       hashedPassword = Column(String)
       isActive = Column(Boolean, default=True)
       role = Column(String)





class Todos(Base):
       __tablename__ = 'todos' #names the table



       id = Column(Integer, primary_key=True, index=True)
       title = Column(String)
       description = Column(String)
       priority = Column(Integer)
       complete = Column(Boolean, default = False)
       ownerId = Column(Integer, ForeignKey("users.id"))
       



