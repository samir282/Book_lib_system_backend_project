from pydantic import BaseModel
from datetime import date

# class Book_data(BaseModel):
#     id : int
#     title : str
#     rating: float
#     author_id : int

# class Update_data(BaseModel):
#     title : str
#     rating : float

class Book_details(BaseModel):
    id : int
    title : str
    rating : float
    createdAt : date
    updatedAt : date
    
    class Config():
        orm_mode = True

class Books_by_name_and_rating(BaseModel):
    author_or_title : str
    min_rating : float
