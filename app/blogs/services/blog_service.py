from typing import Any, List, Optional
from app.blogs.models.blog_model import BlogModel
from app.blogs.repositories.blog_repository import BlogRepository
from app.utils.errors.exceptions import NotFoundException as BlogNotFoundException
class BlogService:
    def __init__(self, blog_repository: BlogRepository) -> None:
        self._blog_repository: BlogRepository = blog_repository
        self.model_name = "Blogs"

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:   
        return self._blog_repository.get_all_blogs(limit=limit, offset=offset)

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
         return self._blog_repository.get_blog_by_id(id=id)
        

    def create_blog(self, blog: BlogModel) -> BlogModel:
        return self._blog_repository.create_blog(blog=blog)

    def update_blog(self, blog: dict[str, Any], id : int) -> BlogModel:
        operation_result: BlogModel | None = self._blog_repository.update_blog(blog_data=blog, blog_id=id)
        if not operation_result:
            raise BlogNotFoundException(identifier=id, model=self.model_name)
        return operation_result

    def delete_blog(self, blog_id : int ) -> BlogModel:
        operation_result: BlogModel | None = self._blog_repository.delete_blog(blog_id=blog_id)
        if not operation_result:
            raise BlogNotFoundException(identifier=blog_id, model=self.model_name)
        return operation_result

    def update_blog_visibility(self, id: int, visibility: bool) -> BlogModel:
        operation_result: BlogModel | None = self._blog_repository.update_blog_visibility(blog_id=id, visibility=visibility)
        if not operation_result:
            raise BlogNotFoundException(identifier=id, model=self.model_name)
        return operation_result
       

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self._blog_repository.get_public_blogs(limit=limit, offset=offset)

    def get_blogs_by_user(self, user_id: int, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self._blog_repository.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)
    
    def set_blog_as_public(self, blog_id : int) -> BlogModel:
        operation_result: BlogModel | None = self._blog_repository.update_blog_visibility(blog_id=blog_id, visibility=True)
        if not operation_result:
            raise BlogNotFoundException(identifier=blog_id, model=self.model_name)
        return operation_result
    
    def set_blog_as_private(self, blog_id : int) -> BlogModel:
        operation_result: BlogModel | None = self._blog_repository.update_blog_visibility(blog_id=blog_id, visibility=False)
        if not operation_result:
            raise BlogNotFoundException(identifier=blog_id, model=self.model_name)
        return operation_result
    