from sqlalchemy import Column, Integer, String, DateTime,Uuid
from sqlalchemy.orm import relationship


from server.database import base 

class Author(base):
    __tablename__ = "authors"

    id=Column(Integer,primary_key=True,index=True)
    uuid = Column(Uuid, index= True)
    name = Column(String(255))
    email = Column(String(120),unique= True, nullable= True)
    bio = Column(String(500))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable= True)
    books = relationship('Book',cascade = "all,delete",back_populates='authors')
    