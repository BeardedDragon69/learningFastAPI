from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()



class Books:
       id:int
       title:str
       author: str
       desc: str
       rating: int

       def __init__(self, id, title, author, desc, rating):
              self.id = id
              self.title = title
              self.author = author
              self.desc = desc
              self.rating = rating
              pass


class BookRequest(BaseModel):
       id: Optional[int] = None # adding an optional field
       title: str=Field(min_length=3)
       author: str = Field(min_length=1)
       desc: str= Field (min_length=1, max_length=100)
       rating: int= Field(gt=-1, lt=6)
       
       pass


BOOKS =[
       Books(1,"Book1","Author1", "Desc1", 5),
       Books(2,"Book2","Author2", "Desc2", 4),
       Books(3,"Book3","Author3", "Desc3", 3),
       Books(4,"Book4","Author4", "Desc4", 2),
       Books(5,"Book5","Author5", "Desc5", 1)
]



@app.get('/books')
async def getAllBooks():
       return BOOKS

@app.post('/addNewBook')
async def createBook(bookRequest: BookRequest):
       newBook = Books(**bookRequest.model_dump())
       print(type(newBook))
       BOOKS.append(findBookId(newBook))



def findBookId(book: Books):
       if len(BOOKS)>0:
              book.id = BOOKS[-1].id +1
       else:
              book.id = 1
       
       return book