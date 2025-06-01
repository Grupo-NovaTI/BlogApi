from comments.models.comment_model import CommentModel
from fastapi import APIRouter, Depends, HTTPException

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

