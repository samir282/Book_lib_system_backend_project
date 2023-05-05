from fastapi import status, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from .schema import Book_details, Books_by_name_and_rating
from server.database import get_db
from .helper import create_book, update_book_data, delete_book_data, download_book, download_books_file,get_book_details


book_router = APIRouter()

#take the inputs directly instead of making schema as UploadFile is not supporting in schema input class
@book_router.post('/create_book', status_code= status.HTTP_201_CREATED)
async def upload_book(author_id: UUID, title: str, rating: float, body: UploadFile = File(...), db: Session = Depends(get_db)): #104857600 = 100MB
    return await create_book(title, rating, author_id, body, db)

#take the inputs directly instead of making schema as UploadFile is not supporting in schema input class
@book_router.put('/update/{book_id}', status_code= status.HTTP_201_CREATED)
async def update_book(book_id: UUID, title: str, rating: float,body : UploadFile | None = None, db: Session = Depends(get_db)):
    return await update_book_data(book_id, title, rating,body, db)

@book_router.delete('/delete/{book_id}', status_code= status.HTTP_200_OK)
def delete_book(book_id:UUID, db: Session = Depends(get_db)):
    return delete_book_data(book_id, db)

@book_router.get('/get/{book_id}', status_code= status.HTTP_200_OK)
def get_book(book_id: UUID, db: Session = Depends(get_db)):
    return download_book(book_id, db)

@book_router.get('/get_all', status_code= status.HTTP_200_OK)
def get_all_books(page: int = 1, limit : int = 10, db: Session = Depends(get_db)):
    return download_books_file(page, limit, db)

@book_router.post('/get_books', status_code= status.HTTP_200_OK, response_model = List[Book_details])
def get_books_by_name(request : Books_by_name_and_rating, db : Session = Depends(get_db)):
    return get_book_details(request.author_or_title, request.min_rating, db)