from fastapi import APIRouter
from book.controller import book_router
from author.controller import author_router

router = APIRouter()

router.include_router(
    book_router,
    tags= ["Book"],
    prefix= "/Book"
)
router.include_router(
    author_router,
    tags= ["Author"],
    prefix= "/Author"
)

# router.include_router(
#     author_router,
#     tags= ["Author"],
#     prefix= "/Author"
# )