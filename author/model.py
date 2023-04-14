from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship


from server.database import base 

class Author(base):
    __tablename__ = "authors"

    id=Column(Integer,primary_key=True,index=True)
    name = Column(String(255))
    books = relationship('Book',cascade = "all,delete",back_populates='authors')
    