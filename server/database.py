from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_database_url="mysql://root:root@localhost:3306/mydb"

engine=create_engine(sql_database_url)

sessionLocal=sessionmaker(autocommit=False,bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

base=declarative_base()