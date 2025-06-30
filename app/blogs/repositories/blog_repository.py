from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from app.blogs.models.blog_model import BlogModel
from app.blogs.exceptions.blog_exceptions import BlogOperationException
from app.utils.logger.application_logger import ApplicationLogger

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
                f"Database error while fetching all blogs: {str(e)}")
            raise BlogOperationException(
                f"Database error while fetching all blogs: {str(e)}")
        except Exception as e:
            _logger.log_error(f"Error fetching all blogs: {str(e)}")
            raise BlogOperationException(f"Error fetching all blogs: {str(e)}")

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.id == id).first()
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(
                f"Database error while fetching blog by id {id}: {str(e)}")
            raise BlogOperationException(
                f"Database error while fetching blog by id {id}: {str(e)}")
        except Exception as e:
            _logger.log_error(f"Error fetching blog by id {id}: {str(e)}")
            raise BlogOperationException(
                f"Error fetching blog by id {id}: {str(e)}")

    def create_blog(self, blog: BlogModel) -> BlogModel:
        try:
            self._db_session.add(blog)
            self._db_session.commit()
            self._db_session.refresh(blog)
            return blog
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(f"Database error while creating blog: {str(e)}")
            raise BlogOperationException(
                f"Database error while creating blog: {str(e)}")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(f"Error creating blog: {str(e)}")
            raise BlogOperationException(f"Error creating blog: {str(e)}")

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
            _logger.log_error(f"Database error while updating blog: {str(e)}")
            raise BlogOperationException(
                f"Database error while updating blog: {str(e)}")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(f"Error updating blog: {str(e)}")
            raise BlogOperationException(f"Error updating blog: {str(e)}")

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
            _logger.log_error(f"Database error while deleting blog: {str(e)}")
            raise BlogOperationException(
                f"Database error while deleting blog: {str(e)}")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(f"Error deleting blog: {str(e)}")
            raise BlogOperationException(f"Error deleting blog: {str(e)}")

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
                f"Database error while updating blog visibility: {str(e)}")
            raise BlogOperationException(
                f"Database error while updating blog visibility: {str(e)}")
        except Exception as e:
            self._db_session.rollback()
            raise BlogOperationException(
                f"Error updating blog visibility: {str(e)}")

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).limit(limit).offset(offset).all()
        except SQLAlchemyError as e:
            _logger.log_error(
                f"Database error fetching public blogs: {str(e)}")
            raise BlogOperationException(
                f"Database error fetching public blogs: {str(e)}")
        except Exception as e:
            _logger.log_error(f"Error fetching public blogs: {str(e)}")
            raise BlogOperationException(
                f"Error fetching public blogs: {str(e)}")

    def get_blogs_by_user(self, user_id: int, limit: int, offset: int) -> List[BlogModel]:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).limit(limit).offset(offset).all()
        except SQLAlchemyError as e:
            _logger.log_error(
                f"Database error fetching blogs by user {user_id}: {str(e)}")
            raise BlogOperationException(
                f"Database error fetching blogs by user {user_id}: {str(e)}")
        except Exception as e:
            _logger.log_error(
                f"Error fetching blogs by user {user_id}: {str(e)}")
            raise BlogOperationException(
                f"Error fetching blogs by user {user_id}: {str(e)}")
            
    def count_blogs_by_user(self, user_id: int) -> int:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).count()
        except SQLAlchemyError as e:
            _logger.log_error(
                f"Database error counting blogs by user {user_id}: {str(e)}")
            raise BlogOperationException(
                f"Database error counting blogs by user {user_id}: {str(e)}")
        except Exception as e:
            _logger.log_error(
                f"Error counting blogs by user {user_id}: {str(e)}")
            raise BlogOperationException(
                f"Error counting blogs by user {user_id}: {str(e)}")
    
    def count_public_blogs(self) -> int:
        try:
            return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).count()
        except SQLAlchemyError as e:
            _logger.log_error(f"Database error counting public blogs: {str(e)}")
            raise BlogOperationException(
                f"Database error counting public blogs: {str(e)}")
        except Exception as e:
            _logger.log_error(f"Error counting public blogs: {str(e)}")
            raise BlogOperationException(
                f"Error counting public blogs: {str(e)}")
