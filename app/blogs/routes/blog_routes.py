from fastapi import APIRouter, Depends, HTTPException

from blogs.models.blog_model import BlogModel

blog_router= APIRouter(
    prefix="/blogs",
    tags=["blogs"],
    responses={404: {"description": "Not found"}},
)

