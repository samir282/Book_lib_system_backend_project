from fastapi import APIRouter

book_router = APIRouter(
    prefix= "/book",
    tags= ["Book"]
)

author_router = APIRouter(
    tags= ["Author"],
    prefix= '/author'
)