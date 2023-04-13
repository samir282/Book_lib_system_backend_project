from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from .schema import book_data, update_data
from .model import Book
from author.model import Author

def create_book(request : book_data, db : Session):
    try:
        author = db.query(Author).filter(Author.id == request.author_id).first()
        if not author:
            author = Author(name=request.author_name)
            db.add(author)
            db.commit()
            db.refresh(author)

        db_book = db.query(Book).filter(Book.title == request.title).first()
        if db_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Book already exist')
        
        new_book = Book(
            title=request.title,
            ratings=request.ratings,
            authorId=author.id,
            createdAt=date.today(),
            updatedAt=date.today(),
            body=request.body
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return {'details' : 'book created'}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
    
    
def update_book_data(book_id: int, request: update_data, db: Session):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

        db_book.title = request.title
        db_book.ratings = request.rating
        db_book.body = request.body
        db_book.updatedAt = date.today()

        db.commit()
        db.refresh(db_book)

        return {'details': 'book updated'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
    
def delete_book_data(book_id : int, db : Session):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()

        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

        db.delete(db_book)
        db.commit()
        return {'details': 'Book deleted'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
    
def get_book_data(book_id : int, db : Session):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()

        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        
        return db_book
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
    
    
def get_all_books(db: Session):
    try:
        books = db.query(Book).all()
        if not books:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'No data found')
        return books
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'an error occured: {e}')