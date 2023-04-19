from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status, UploadFile
from fastapi.responses import StreamingResponse
from datetime import date
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import math

from .model import Book
from author.model import Author

async def create_book(title: str, rating: float, author_id: int, body: UploadFile, db : Session):
    try:
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Author doesn't exist. First update the author data")

        db_book = db.query(Book).filter(Book.title == title).first()
        if db_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Book already exist')
        if rating>10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='rating should be out of 10')
        
        content = await body.read()
        new_book = Book(
            title= title,
            rating=rating,
            authorId=author_id,
            createdAt=date.today(),
            updatedAt=date.today(),
            body=content
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return {'Message' : 'book created',
                'BookId' : new_book.id}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
    
    
async def update_book_data(book_id: int, title: str, rating: float,body:UploadFile, db: Session):
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        if rating>10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='rating should be out of 10')

        db_book.title = title
        db_book.rating = rating
        db_book.updatedAt = date.today()
        if body:
            content = await body.read()
            db_book.body = content
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
        book = db.query(Book).filter(Book.id == book_id).first()

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        
        file_data = BytesIO(book.body)
        return StreamingResponse(file_data, media_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="{}.pdf"'.format(book.title)})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
    
    
def get_books(page, limit, db: Session):
    try:
        books = db.query(Book).offset((page-1)*limit).limit(limit).all()
        total_books = db.query(Book).count()
        total_pages = math.ceil(total_books/limit)
        if page>total_pages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No more data available')
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No data found')

        zip_bytes = BytesIO()
        with ZipFile(zip_bytes, mode="w", compression=ZIP_DEFLATED) as zf:
            for book in books:
                zf.writestr(f"{book.title}.pdf", book.body)

        zip_bytes.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=books.zip"
        }
        respose = StreamingResponse(iter([zip_bytes.read()]), headers=headers, media_type="application/zip")
        # return {'response': respose,
        #         'total_page' : total_pages
        #         }
        return respose

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occurred: {str(e)}')
    
    
def get_book_details(author_or_title: str, db : Session):
    try:
        books = db.query(Book).join(Author).filter(
                text("authors.name LIKE :matching_str OR books.title LIKE :matching_str")).params(matching_str=f'%{author_or_title}%').all()
        if not books:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Book not found')
        return books
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occurred: {str(e)}')
