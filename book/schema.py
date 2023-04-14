from pydantic import BaseModel
from datetime import date

class book_data(BaseModel):
    #id : int
    title : str
    ratings: float
    author_id : int
    body : str

class update_data(BaseModel):
    title : str
    rating : float
    body : str