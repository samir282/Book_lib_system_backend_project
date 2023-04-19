from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from author.schema import author_data
from author.model import Author

def create_author(request: author_data, db : Session):
    try:
        new_author = Author(
            name = request.Author_name
        )
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return {'details' : 'author created',
                'id' : new_author.id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
    

def delete_author_data(author_id : int, db : Session):
    try:
        db_author = db.query(Author).filter(Author.id == author_id).first()

        if not db_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')

        db.delete(db_author)
        db.commit()
        return {'details': f'Auther data of id : {db_author.id} deleted'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
    
def get_author_data(author_id : int, db : Session):
    try:
        db_author = db.query(Author).filter(Author.id == author_id).first()

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