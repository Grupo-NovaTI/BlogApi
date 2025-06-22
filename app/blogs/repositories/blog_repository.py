from typing import List, Optional
from sqlalchemy.orm.session import Session
from blogs.models.blog_model import BlogModel
from blogs.exceptions.blog_exceptions import BlogOperationException
from sqlalchemy.exc import SQLAlchemyError


class BlogRepository:
    def __init__(self, db: Session) -> None:
        self.__db: Session = db

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        try:
            return self.__db.query(BlogModel).limit(limit=limit).offset(offset=offset).all()
        except Exception as e:
            raise BlogOperationException(f"Error fetching all blogs: {str(e)}")

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        try:
            return self.__db.query(BlogModel).filter(BlogModel.id == id).first()
        except Exception as e:
            raise BlogOperationException(
                f"Error fetching blog by id {id}: {str(e)}")

    def create_blog(self, blog: BlogModel) -> BlogModel:
        try:
            self.__db.add(blog)
            self.__db.commit()
            self.__db.refresh(blog)
            return blog
        except Exception as e:
            raise BlogOperationException(f"Error creating blog: {str(e)}")

    def update_blog(self, blog_data: dict, blog_id: int) -> BlogModel:
        try:
            with self.__db.begin():
                self.__db.query(BlogModel).filter(
                    BlogModel.id == blog_id).update(blog_data)
            return self.get_blog_by_id(blog_id)
        except Exception as e:
            raise BlogOperationException(f"Error updating blog: {str(e)}")

    def delete_blog(self, blog: BlogModel) -> BlogModel:
        try:
            self.__db.delete(blog)
            self.__db.commit()
            return blog
        except SQLAlchemyError as e:
            self.__db.rollback()

            raise BlogOperationException(
                f"Database error while deleting blog: {str(e)}")
        except Exception as e:
            self.__db.rollback()

            raise BlogOperationException(f"Error deleting blog: {str(e)}")

    def update_blog_visibility(self, blog_id: int, visibility: bool) -> Optional[BlogModel]:
        try:
            with self.__db.begin():
                self.__db.query(BlogModel).filter(BlogModel.id == blog_id).update(
                    values={"is_published": visibility})
                self.__db.commit()
            return self.get_blog_by_id(id=blog_id)
        except SQLAlchemyError as e:
            self.__db.rollback()
            raise BlogOperationException(
                f"Database error while updating blog visibility: {str(e)}")

        except Exception as e:
            self.__db.rollback()
            raise BlogOperationException(
                f"Error updating blog visibility: {str(e)}")

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        try:
            return self.__db.query(BlogModel).filter(BlogModel.is_published == True).limit(limit).offset(offset).all()
        except Exception as e:
            raise BlogOperationException(
                f"Error fetching public blogs: {str(e)}")

    def get_blogs_by_user(self, user_id: int, limit: int, offset: int) -> List[BlogModel]:
        try:
            return self.__db.query(BlogModel).filter(BlogModel.author_id == user_id).limit(limit).offset(offset).all()
        except Exception as e:
            raise BlogOperationException(
                f"Error fetching blogs by user {user_id}: {str(e)}")
