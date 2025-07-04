from email.mime import message
from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from app.blogs.models.blog_model import BlogModel
from app.utils.logger.application_logger import ApplicationLogger
from app.utils.errors.exception_handlers import handle_repository_exception
from app.utils.errors.error_messages import database_error_message, unknown_error_message
from app.utils.enums.operations import Operations

_logger = ApplicationLogger(__name__, log_to_console=False)

_MODEL = "Blogs"


class BlogRepository:
    def __init__(self, db: Session) -> None:
        self._db_session: Session = db

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.FETCH
    )
    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """Fetches all blogs with pagination support."""
        return self._db_session.query(BlogModel).limit(limit=limit).offset(offset=offset).all()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.FETCH
    )
    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        return self._db_session.query(BlogModel).filter(BlogModel.id == id).first()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.CREATE
    )
    def create_blog(self, blog: BlogModel) -> BlogModel:
        """Creates a new blog entry in the database."""
        self._db_session.add(blog)
        self._db_session.commit()
        self._db_session.refresh(blog)
        return blog

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.UPDATE
    )
    def update_blog(self, blog_data: dict, blog_id: int) -> Optional[BlogModel]:
        rows_affected: int = self._db_session.query(BlogModel).filter(
            BlogModel.id == blog_id).update(blog_data)
        if rows_affected == 0:
            return None
        self._db_session.commit()
        return self.get_blog_by_id(blog_id)

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.DELETE
    )
    def delete_blog(self, blog_id: int) -> Optional[BlogModel]:
        blog: BlogModel | None = self.get_blog_by_id(blog_id)
        rows_affected: int = self._db_session.query(
            BlogModel).filter(BlogModel.id == blog_id).delete()
        if rows_affected == 0 or not blog:
            return None
        self._db_session.commit()
        return blog

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.PATCH
    )
    def update_blog_visibility(self, blog_id: int, visibility: bool) -> Optional[BlogModel]:
        rows_affected: int = self._db_session.query(BlogModel).filter(BlogModel.id == blog_id).update(
            values={"is_published": visibility})
        if rows_affected == 0:
            return None
        self._db_session.commit()
        return self.get_blog_by_id(id=blog_id)

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.FETCH)
    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """Fetches all public blogs with pagination support."""
        return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).limit(limit=limit).offset(offset=offset).all()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.FETCH)
    def get_blogs_by_user(self, user_id: int, limit: int, offset: int) -> List[BlogModel]:
        return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).limit(limit=limit).offset(offset=offset).all()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.FETCH)
    def count_blogs_by_user(self, user_id: int) -> int:
        """Counts the number of blogs by a specific user."""
        return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).count()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.FETCH)
    def count_public_blogs(self) -> int:
        """Counts the number of public blogs."""
        return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).count()
