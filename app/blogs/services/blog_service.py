from typing import List, Optional
from blogs.models.blog_model import BlogModel
from blogs.repositories.blog_repository import BlogRepository
from blogs.exceptions.blog_exceptions import BlogNotFoundException
class BlogService:
    def __init__(self, blog_repository: BlogRepository) -> None:
        self.__blog_repository: BlogRepository = blog_repository

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:   
        return self.__blog_repository.get_all_blogs(limit=limit, offset=offset)

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        return self.__blog_repository.get_blog_by_id(id=id)

    def create_blog(self, blog: BlogModel) -> BlogModel:
        return self.__blog_repository.create_blog(blog=blog)

    def update_blog(self, blog: dict, id : int) -> BlogModel:
        blog_exists: Optional[BlogModel] = self.__blog_repository.get_blog_by_id(id=id)
        if not blog_exists:
            raise BlogNotFoundException(f"Blog with id {id} not found.")
        return self.__blog_repository.update_blog(blog_data=blog, blog_id=id)

    def delete_blog(self, blog_id : int ) -> BlogModel:
        blog_exists: BlogModel | None = self.__blog_repository.get_blog_by_id(id=blog_id)
        if not blog_exists:
            raise BlogNotFoundException(f"Blog with id {blog_id} not found.")
        return self.__blog_repository.delete_blog(blog=blog_exists)

    def update_blog_visibility(self, id: int, visibility: bool):
        blog_exists: BlogModel | None = self.__blog_repository.get_blog_by_id(id=id)
        if not blog_exists:
            raise BlogNotFoundException(f"Blog with id {id} not found.")
        return self.__blog_repository.update_blog_visibility(blog_id=id, visibility=visibility)

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self.__blog_repository.get_public_blogs(limit=limit, offset=offset)

    def get_blogs_by_user(self, user_id: int, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self.__blog_repository.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)