from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import uuid
from uuid import UUID

from author.schema import Author_data
from author.model import Author

def add_author(request: Author_data, db : Session):
    try:
        db_author = db.query(Author).filter(Author.email == request.author_email).first()
        if db_author:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'author already exist')
        new_author = Author(
            uuid = uuid.uuid4(),
            name = request.author_name,
            email = request.author_email,
            bio = request.author_bio,
            created_at = datetime.now(),
        )
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return {'details' : 'author created',
                'id' : new_author.uuid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
    

def update_author_data(author_id : UUID, request : Author_data, db : Session):
    try:
        db_author = db.query(Author).filter(Author.uuid == author_id).first()
        if not db_author:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "author not exist")
        db_author.name = request.author_name
        db_author.email = request.author_email
        db_author.bio = request.author_bio
        db_author.updated_at = datetime.now()
        db.commit()
        db.refresh(db_author)
        return {'mesage' : 'data updated'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"An error occured: {e}")
    
  
def delete_author_data(author_id : UUID, db : Session):
    try:
        db_author = db.query(Author).filter(Author.uuid == author_id).first()

        if not db_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')

        db.delete(db_author)
        db.commit()
        return {'details': f'Auther data of id : {db_author.id} deleted'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
def get_author_data(author_id : UUID, db : Session):
    try:
        db_author = db.query(Author).filter(Author.uuid == author_id).first()

        if not db_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
        
        return db_author
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
    
def get_all_authors(db: Session):
    try:
        authors = db.query(Author).all()
        if not authors:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'No data found')
        return authors
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'an error occured: {e}')