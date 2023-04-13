from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session


from server.database import get_db
from router.apirouter import author_router
from author.schema import author_data
from author.helper import create_author, delete_author_data, get_author_data, get_all_authors


@author_router.post('/create', status_code= status.HTTP_201_CREATED)
def add_author(request : author_data, db: Session = Depends(get_db)):
    return create_author(request, db)

@author_router.delete('/delete/{author_id}', status_code= status.HTTP_200_OK)
def delete_author(author_id : int, db: Session = Depends(get_db)):
    return delete_author_data(author_id, db)

@author_router.get('/get/{author_id}', status_code= status.HTTP_200_OK)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return get_author_data(author_id, db)

@author_router.get('/get_all', status_code= status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return get_all_authors(db)