from fastapi import status, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from .schema import Book_data, Update_data, Book_details
from server.database import get_db
from .helper import create_book, update_book_data, delete_book_data, get_book_data, get_books,get_book_details


book_router = APIRouter()

#take the inputs directly instead of making schema as UploadFile is not supporting in schema input class
@book_router.post('/create_book', status_code= status.HTTP_201_CREATED)
async def upload_book(title: str, rating: float, author_id: int, body: UploadFile = File(...), db: Session = Depends(get_db)):
    return await create_book(title, rating, author_id, body, db)

#take the inputs directly instead of making schema as UploadFile is not supporting in schema input class
@book_router.put('/update/{book_id}', status_code= status.HTTP_201_CREATED)
async def update_book(book_id: int, title: str, rating: float,body : UploadFile | None = None, db: Session = Depends(get_db)):
    return await update_book_data(book_id, title, rating,body, db)

@book_router.delete('/delete/{book_id}', status_code= status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return delete_book_data(book_id, db)

@book_router.get('/get/{book_id}', status_code= status.HTTP_200_OK)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return get_book_data(book_id, db)

@book_router.get('/get_all', status_code= status.HTTP_200_OK)
def get_all_books(page: int = 1, limit : int = 10, db: Session = Depends(get_db)):
    return get_books(page, limit, db)

@book_router.get('/get_books/{author_or_title}', status_code= status.HTTP_200_OK, response_model = List[Book_details])
def get_books_by_name(author_or_title: str, db : Session = Depends(get_db)):
    return get_book_details(author_or_title, db)