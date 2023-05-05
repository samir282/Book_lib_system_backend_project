from pydantic import BaseModel
from datetime import datetime

class Author_data(BaseModel):
    author_name : str
    author_email : str
    author_bio : str

class Show_data(BaseModel):
    id : int
    name : str
    email : str
    bio : str
    created_at : datetime
    updated_at : datetime = None

    class Config():
        orm_mode = True