from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from .schema import book_data, update_data
from router.apirouter import book_router
from server.database import get_db
from .helper import create_book, update_book_data, delete_book_data, get_book_data, get_all_books


@book_router.post('/create', status_code= status.HTTP_201_CREATED)
def upload_book(request : book_data, db: Session = Depends(get_db)):
    return create_book(request, db)

@book_router.put('/update/{book_id}', status_code= status.HTTP_201_CREATED)
def update_book(book_id: int, request: update_data, db: Session = Depends(get_db)):
    return update_book_data(book_id, request, db)

@book_router.delete('/delete/{book_id}', status_code= status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return delete_book_data(book_id, db)

@book_router.get('/get/{book_id}', status_code= status.HTTP_200_OK)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return get_book_data(book_id, db)

@book_router.get('/get_all', status_code= status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return get_all_books(db)