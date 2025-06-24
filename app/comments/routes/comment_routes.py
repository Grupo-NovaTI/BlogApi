from fastapi import APIRouter, Depends, HTTPException
from app.comments.models.comment_model import CommentModel

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

