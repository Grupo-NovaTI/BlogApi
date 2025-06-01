from fastapi import APIRouter, Depends, HTTPException

from tags.models.tag_model import TagModel
from tags.models.blog_tags import blog_tags

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)

