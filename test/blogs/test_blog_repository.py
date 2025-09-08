from typing import List, Optional
from app.blogs.models.blog_model import BlogModel
from app.users.models.user_model import UserModel
from app.comments.models.comment_model import CommentModel
from app.blogs.repositories.blog_repository import BlogRepository
from app.tags.models.tag_model import TagModel
import pytest
from sqlalchemy.orm.session import Session
from test.utils.conftest import db_session

@pytest.fixture(scope="function")
def blog_repo(db_session: Session) -> BlogRepository:
    return BlogRepository(db_session=db_session)

class TestBlogRepository:
    def test_create_blog(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        
        new_blog = BlogModel(title="Test Blog", content="This is a test blog.", user_id=1)
        
        # Act
        created_blog: BlogModel = blog_repo.create_blog(new_blog)
        db_session.commit()
        
        # Assert
        assert created_blog.id is not None
        assert created_blog.title == "Test Blog" # type: ignore
        assert created_blog.content == "This is a test blog." # type: ignore
        assert created_blog.user_id == 1 # type: ignore
        
    def test_get_blog(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        new_blog = BlogModel(title="Test Blog", content="This is a test blog.", user_id=1)
        blog_repo.create_blog(blog=new_blog)
        db_session.commit()

        # Act
        retrieved_blog: Optional[BlogModel] = blog_repo.get_blog_by_id(new_blog.id) # type: ignore

        # Assert
        assert retrieved_blog is not None
        assert retrieved_blog.id == new_blog.id # type: ignore
        assert retrieved_blog.title == new_blog.title # type: ignore
        assert retrieved_blog.content == new_blog.content # type: ignore
        assert retrieved_blog.user_id == new_blog.user_id # type: ignore

    def test_update_blog(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        new_blog = BlogModel(title="Test Blog", content="This is a test blog.", user_id=1)
        blog_repo.create_blog(new_blog)
        db_session.commit()

        # Act
        blog_to_update: dict[str, str] = {"title": "Updated Blog Title"}
        updated_blog: Optional[BlogModel] = blog_repo.update_blog(blog_data=blog_to_update, blog=new_blog)
        db_session.commit()

        # Assert
        assert updated_blog.id == new_blog.id # type: ignore
        assert updated_blog.title == "Updated Blog Title" # type: ignore
        assert updated_blog.content == new_blog.content # type: ignore
        assert updated_blog.user_id == new_blog.user_id # type: ignore

    def test_delete_blog(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        new_blog = BlogModel(title="Test Blog", content="This is a test blog.", user_id=1)
        blog_repo.create_blog(blog=new_blog)
        db_session.commit()

        # Act
        blog_repo.delete_blog(blog=new_blog)
        db_session.commit()

        # Assert
        deleted_blog: Optional[BlogModel] = blog_repo.get_blog_by_id(new_blog.id) # type: ignore
        assert deleted_blog is None
        
    def test_get_blogs_by_user(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        user1 = UserModel(username="testuser", email="test@example.com", name="Test", last_name="User", hashed_password="hashedpassword")
        user2 = UserModel(username="user2", email="user2@example.com", name="User", last_name="Two", hashed_password="hashedpassword2")
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        blog1 = BlogModel(title="Blog 1", content="Content 1", user_id=user1.id, is_published=True)
        blog2 = BlogModel(title="Blog 2", content="Content 2", user_id=user1.id, is_published=True)
        blog3 = BlogModel(title="Blog 3", content="Content 3", user_id=user2.id, is_published=True)
        
        blog_repo.create_blog(blog=blog1)
        blog_repo.create_blog(blog=blog2)
        blog_repo.create_blog(blog=blog3)
        db_session.commit()
        
        # Act
        limit : int = 10
        offset : int = 0
        user1_blogs: List[BlogModel] = blog_repo.get_blogs_by_user(user_id=user1.id, limit=limit, offset=offset) # type: ignore
        user2_blogs: List[BlogModel] = blog_repo.get_blogs_by_user(user_id=user2.id, limit=limit, offset=offset) # type: ignore
        
        # Assert
        assert len(user1_blogs) == 2
        assert len(user2_blogs) == 1
        
        # Sort blogs by title to ensure consistent ordering for assertions
        user1_blogs_sorted : List[BlogModel] = sorted(user1_blogs, key=lambda blog: blog.title) # type: ignore
        user2_blogs_sorted : List[BlogModel] = sorted(user2_blogs, key=lambda blog: blog.title) # type: ignore

        assert user1_blogs_sorted[0].title == "Blog 1" # type: ignore
        assert user1_blogs_sorted[1].title == "Blog 2" # type: ignore
        assert user2_blogs_sorted[0].title == "Blog 3" # type: ignore
        
    def test_get_public_blogs(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        blog1 = BlogModel(title="Public Blog 1", content="Content 1", user_id=1, is_published=True)
        blog2 = BlogModel(title="Public Blog 2", content="Content 2", user_id=1, is_published=True)
        blog3 = BlogModel(title="Private Blog", content="Content 3", user_id=1, is_published=False)
        
        blog_repo.create_blog(blog=blog1)
        blog_repo.create_blog(blog=blog2)
        blog_repo.create_blog(blog=blog3)
        db_session.commit()
        
        # Act
        limit : int = 10
        offset : int = 0
        public_blogs: List[BlogModel] = blog_repo.get_public_blogs(limit=limit, offset=offset)
        
        # Assert
        assert len(public_blogs) == 2
        titles: list[str] = [blog.title for blog in public_blogs] # type: ignore
        assert "Public Blog 1" in titles
        assert "Public Blog 2" in titles
        assert "Private Blog" not in titles
    
    
    def test_get_blog_by_id_not_found(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Act
        retrieved_blog: Optional[BlogModel] = blog_repo.get_blog_by_id(9999)
        # Assert
        assert retrieved_blog is None
        
    def test_count_blogs_by_user(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        user1 = UserModel(username="testuser", email="test@example.com", name="Test", last_name="User", hashed_password="hashedpassword")
        user2 = UserModel(username="user2", email="user2@example.com", name="User", last_name="Two", hashed_password="hashedpassword2")
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        blog1 = BlogModel(title="Blog 1", content="Content 1", user_id=user1.id, is_published=True)
        blog2 = BlogModel(title="Blog 2", content="Content 2", user_id=user1.id, is_published=True)
        blog3 = BlogModel(title="Blog 3", content="Content 3", user_id=user2.id, is_published=True)

        blog_repo.create_blog(blog=blog1)
        blog_repo.create_blog(blog=blog2)
        blog_repo.create_blog(blog=blog3)
        db_session.commit()

        # Act
        user1_blog_count: int = blog_repo.count_blogs_by_user(user_id=user1.id) # type: ignore
        user2_blog_count: int = blog_repo.count_blogs_by_user(user_id=user2.id) # type: ignore

        # Assert
        assert user1_blog_count == 2
        assert user2_blog_count == 1
        
    def test_count_public_blogs(self, blog_repo: BlogRepository, db_session: Session) -> None:
        # Arrange
        blog1 = BlogModel(title="Public Blog 1", content="Content 1", user_id=1, is_published=True)
        blog2 = BlogModel(title="Public Blog 2", content="Content 2", user_id=1, is_published=True)
        blog3 = BlogModel(title="Private Blog", content="Content 3", user_id=1, is_published=False)

        blog_repo.create_blog(blog=blog1)
        blog_repo.create_blog(blog=blog2)
        blog_repo.create_blog(blog=blog3)
        db_session.commit()

        # Act
        public_blog_count: int = blog_repo.count_public_blogs()

        # Assert
        assert public_blog_count == 2