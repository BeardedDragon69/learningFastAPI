# to start a fastapi application we need to use this command:
# uvicorn books:app --reload

from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get('/allBooks') #this is a decorative which makes sure that this is an endpoint
async def readAllBooks():
       return BOOKS

''' 
important note put all of your static methods first 
then followed by the dynamic parameters. 

This is because python is interpreter based so if we put 


if you want to use space in url use %20 it is the encoding for space in urls
'''


@app.get('/books/{book_title}')
async def readBooks(book_title: str):
       for book in BOOKS:
              if book.get('title').casefold() == book_title.casefold():
                     return book
              

#adding query parameters now

@app.get('/books/')
async def getBook(category:str):
       booksToReturn=[]
       for book in BOOKS:
              if book.get('category').casefold() == category.casefold():
                     booksToReturn.append(book)
       return booksToReturn


@app.get('/books/{bookTitle}')
async def getBooks(category: str, bookTitle: str):
    booksToReturn = []
    for book in BOOKS:
        if (book.get('title').casefold() == bookTitle.casefold() and 
            book.get('category').casefold() == category.casefold()):  
            booksToReturn.append(book)
    
    return booksToReturn

#adding post requests

@app.post('/books/createBook')
async def creatBook(newBook = Body()):
      BOOKS.append(newBook)


@app.put('/books/updateBook')
async def updateBook(updatedBook = Body()):
      for i in range(len(BOOKS)):
            if BOOKS[i].get('title').casefold() == updatedBook.get('title').casefold():
                  BOOKS[i] = updatedBook
      

#delete request methods

@app.delete('/books/deleteBooks/{bookTitle}')
async def deleteBooks(bookTitle:str):
      for i in range(len(BOOKS)):
            if BOOKS[i].get('title').casefold() == bookTitle.casefold():
                  BOOKS.pop(i)
                  break
      
@app.get('/books/getBooks/{authorName}')
async def getBooksByAuthor(authorName:str):
      booksToReturn = []
      for book in BOOKS:
            if book.get('author').casefold() == authorName.casefold():
                  booksToReturn.append(book)
      return booksToReturn





