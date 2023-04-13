from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


from server.database import base
from author.model import Author


class Book(base):
    __tablename__="books"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255),unique=True,index=True)
    ratings = Column(Float)
    authorId = Column(Integer,ForeignKey('authors.id'))
    createdAt = Column(Date)
    updatedAt = Column(Date)
    body = Column(String(255))
    authors = relationship('Author',back_populates='books')
