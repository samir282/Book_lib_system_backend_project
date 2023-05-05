
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey,Uuid
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.orm import relationship

from server.database import base
# from author.model import Author


class Book(base):
    __tablename__="books"
    id = Column(Integer,primary_key=True,index=True)
    uuid = Column(Uuid,index=True)
    title = Column(String(255),unique=True,index=True)
    rating = Column(Float)
    authorId = Column(Integer,ForeignKey('authors.id'))
    createdAt = Column(Date)
    updatedAt = Column(Date)
    # body = Column(LargeBinary(length=(2**32)-1))
    body = Column(MEDIUMBLOB) #max_size : 16 MB
    authors = relationship('Author',back_populates='books')
