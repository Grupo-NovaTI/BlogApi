from email.mime import message
from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from app.blogs.models.blog_model import BlogModel
from app.blogs.exceptions.blog_exceptions import BlogOperationException
from app.utils.logger.application_logger import ApplicationLogger
from app.utils.errors.error_messages import database_error_message, unknown_error_message

_logger = ApplicationLogger(__name__, log_to_console=False)


class BlogRepository:
    def __init__(self, db: Session) -> None:
        self._db_session: Session = db

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """Fetches all blogs with pagination support."""
        try:
            return self._db_session.query(BlogModel).limit(limit=limit).offset(offset=offset).all()
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(
                message=database_error_message(operation="fetching", instance="all blogs", exception=e))
            raise BlogOperationException(
                operation="fetching", message=str(e))
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="fetching", instance="all blogs", exception=e))
            raise BlogOperationException(operation="fetching", message=str(e))

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.id == id).first()
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(
                message=database_error_message(operation="fetching", instance="blog", exception=e))
            raise BlogOperationException(
                operation="fetching", message=str(e))
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="fetching", instance="blog", exception=e))
            raise BlogOperationException( operation="fetching",
                message=str(e))

    def create_blog(self, blog: BlogModel) -> BlogModel:
        try:
            self._db_session.add(blog)
            self._db_session.commit()
            self._db_session.refresh(blog)
            return blog
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="creating", instance="blog", exception=e))
            raise BlogOperationException(
                operation="creating", message=str(e))
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="creating", instance="blog", exception=e))
            raise BlogOperationException(
                operation="creating", message=str(e))

    def update_blog(self, blog_data: dict, blog_id: int) -> Optional[BlogModel]:
        try:
            rows_affected: int = self._db_session.query(BlogModel).filter(
                BlogModel.id == blog_id).update(blog_data)
            if rows_affected == 0:
                return None
            self._db_session.commit()
            return self.get_blog_by_id(blog_id)
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(
                operation="updating", instance="blog", exception=e))
            raise BlogOperationException(
                operation="updating", message=str(e))
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(
                operation="updating", instance="blog", exception=e))
            raise BlogOperationException(
                operation="updating", message=str(e))

    def delete_blog(self, blog_id: int) -> Optional[BlogModel]:
        try:
            blog: BlogModel | None = self.get_blog_by_id(blog_id)
            rows_affected: int = self._db_session.query(
                BlogModel).filter(BlogModel.id == blog_id).delete()
            if rows_affected == 0 or not blog:
                return None
            self._db_session.commit()
            return blog
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(
                operation="deleting", instance="blog", exception=e))
            raise BlogOperationException(
                operation="deleting", message=str(e))
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(
                operation="deleting", instance="blog", exception=e))
            raise BlogOperationException(
                operation="deleting", message=str(e))

    def update_blog_visibility(self, blog_id: int, visibility: bool) -> Optional[BlogModel]:
        try:
            rows_affected: int = self._db_session.query(BlogModel).filter(BlogModel.id == blog_id).update(
                values={"is_published": visibility})
            if rows_affected == 0:
                return None
            self._db_session.commit()
            return self.get_blog_by_id(id=blog_id)
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(
                database_error_message(
                    operation="updating visibility", instance="blog", exception=e))
            raise BlogOperationException(
                operation="updating visibility", message=str(e))
        except Exception as e:
            self._db_session.rollback()
            raise BlogOperationException(
                operation="updating visibility", message=str(e))

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).limit(limit=limit).offset(offset=offset).all()
        except SQLAlchemyError as e:
            _logger.log_error(
                database_error_message(operation="fetching public blogs", instance="blog", exception=e))
            raise BlogOperationException(
                operation="fetching public blogs", message=str(e))
        except Exception as e:
            _logger.log_error(
                unknown_error_message(operation="fetching public blogs", instance="blog", exception=e))
            raise BlogOperationException(
                operation="fetching public blogs", message=str(e))

    def get_blogs_by_user(self, user_id: int, limit: int, offset: int) -> List[BlogModel]:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).limit(limit=limit).offset(offset=offset).all()
        except SQLAlchemyError as e:
            _logger.log_error(
                database_error_message(
                    operation="fetching blogs by user", instance="blog", exception=e))
            raise BlogOperationException(
                operation="fetching blogs by user", message=str(e))
        except Exception as e:
            _logger.log_error(
                unknown_error_message(operation="fetching blogs by user", instance="blog", exception=e))
            raise BlogOperationException(
                operation="fetching blogs by user", message=str(e))
            
    def count_blogs_by_user(self, user_id: int) -> int:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).count()
        except SQLAlchemyError as e:
            _logger.log_error(
                message=database_error_message(operation="counting blogs by user", instance="blog", exception=e))
            raise BlogOperationException(
                operation="counting blogs by user", message=str(e))
        except Exception as e:
            _logger.log_error(
                message=unknown_error_message(operation="counting blogs by user", instance="blog", exception=e))
            raise BlogOperationException(
                operation="counting blogs by user", message=str(e))

    def count_public_blogs(self) -> int:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).count()
        except SQLAlchemyError as e:
            _logger.log_error(
                database_error_message(operation="counting public blogs", instance="blog", exception=e))
            raise BlogOperationException(
                operation="counting public blogs", message=str(e))
        except Exception as e:
            _logger.log_error(
                unknown_error_message(operation="counting public blogs", instance="blog", exception=e))
            raise BlogOperationException(
                operation="counting public blogs", message=str(e))
