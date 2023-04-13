from fastapi import FastAPI

from server.database import base, engine
# from router.apirouter import book_router
from book.controller import book_router
from author.controller import author_router


base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)




