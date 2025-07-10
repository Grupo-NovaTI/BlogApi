from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from app.blogs.models.blog_model import BlogModel

class BlogRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """Fetches all blogs with pagination support."""
        return self._db_session.query(BlogModel).filter(and_(BlogModel.is_published == True)).limit(limit=limit).offset(offset=offset).all()

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        return self._db_session.query(BlogModel).filter(BlogModel.id == id).first()

    def create_blog(self, blog: BlogModel) -> BlogModel:
        """Creates a new blog entry in the database."""
        self._db_session.add(blog)
        self._db_session.flush()
        return blog


    def update_blog(self, blog_data: dict, blog_id: int, user_id : int) -> Optional[BlogModel]:
        rows_affected: int = self._db_session.query(BlogModel).filter(
            and_(BlogModel.id == blog_id, BlogModel.author_id == user_id)).update(blog_data)
        if rows_affected == 0:
            return None
        return self.get_blog_by_id(blog_id)


    def delete_blog(self, blog_id: int, user_id: int) -> bool:
        blog: Optional[BlogModel] = self._db_session.query(BlogModel).filter(
            and_(BlogModel.id == blog_id, BlogModel.author_id == user_id)).first()
        if not blog:
            return False
        self._db_session.delete(instance=blog)
        return True


    def update_blog_visibility(self, blog_id: int, visibility: bool, user_id: int) -> Optional[BlogModel]:
        rows_affected: int = self._db_session.query(BlogModel).filter(and_(BlogModel.id == blog_id, BlogModel.author_id == user_id)).update(
            values={"is_published": visibility})
        if rows_affected == 0:
            return None
        return self.get_blog_by_id(id=blog_id)

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """Fetches all public blogs with pagination support."""
        return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).limit(limit=limit).offset(offset=offset).all()

    def get_blogs_by_user(self, user_id: int, limit: int, offset: int) -> List[BlogModel]:
        return self._db_session.query(BlogModel).filter(and_(BlogModel.author_id == user_id, BlogModel.is_published == True)).limit(limit=limit).offset(offset=offset).all()

    def count_blogs_by_user(self, user_id: int) -> int:
        """Counts the number of blogs by a specific user."""
        return self._db_session.query(BlogModel).filter(BlogModel.author_id == user_id).count()

    def count_public_blogs(self) -> int:
        """Counts the number of public blogs."""
        return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).count()