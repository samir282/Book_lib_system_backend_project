from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


from server.database import get_db
from author.schema import Author_data, Show_data
from author.helper import add_author, delete_author_data, get_author_data, get_all_authors,update_author_data

author_router = APIRouter()

@author_router.post('/create', status_code= status.HTTP_201_CREATED)
def create_author(request : Author_data, db: Session = Depends(get_db)):
    return add_author(request, db)

@author_router.put('/update/{author_id}',status_code= status.HTTP_201_CREATED)
def update_author(author_id : UUID, request : Author_data, db : Session = Depends(get_db)):
    return update_author_data(author_id, request, db)

@author_router.delete('/delete/{author_id}', status_code= status.HTTP_200_OK)
def delete_author(author_id : UUID, db: Session = Depends(get_db)):
    return delete_author_data(author_id, db)

@author_router.get('/get/{author_id}', status_code= status.HTTP_200_OK, response_model= Show_data)
def get_author(author_id: UUID, db: Session = Depends(get_db)):
    return get_author_data(author_id, db)

@author_router.get('/get_all', status_code= status.HTTP_200_OK, response_model= List[Show_data])
def get_all(db: Session = Depends(get_db)):
    return get_all_authors(db)