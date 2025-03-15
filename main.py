from fastapi import FastAPI,HTTPException
import uvicorn
from pydantic import BaseModel,Field,ConfigDict,EmailStr
# fastapi dev main.py
# uvicorn main:app --reload
app = FastAPI()

class New_Book(BaseModel):
    title:str=Field(max_length=30)
    author:str | None = Field(max_length=20)
    author_email:EmailStr
    model_config = ConfigDict(extra='forbid')

class New_Book_With_id(New_Book):
    id:int=Field(ge=1,le=10000)   


books=[ 
{
    "id":1,
    "title":"Асинхронность в python",
    "author":"мэттью", 
    "author_email":"dmi5@gmail.com",
    
},
{
     "id":2,
    "title":"Backend в python",
    "author":"Артем",
    "author_email":"vasya@gmail.com",
},
]

@app.get("/books",summary=['Получить все книги 📚'],tags=['Получение данных 📊']) 
def read_books()->list[New_Book_With_id]:
    allbooks = list(map(lambda l: New_Book_With_id(**l),books))
    print(allbooks)
    return allbooks

@app.get("/books/{id}",summary=['Получить книгу 🔎📗'],tags=['Получение данных 📊'])
def get_book(id:int)->dict:
    for book in books:
        if book['id'] == id:
            return book
    raise HTTPException(status_code=404,detail="Book wasn't found")

@app.post("/book/add",summary=["Добавить книгу"],tags=['Добавление данных 📥'])
def add_book(book:New_Book):
    new_book ={
    "book_id":len(books)+1,
    "title" : book.title,
    "author" : book.author,
    "author_email":book.author_email
    }
    books.append(new_book)
    return {"success":True,"message":"книга успешно добавлена"}


if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)