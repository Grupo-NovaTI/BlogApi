from functools import wraps
from typing import Callable, List
from starlette import status
from fastapi import HTTPException
from app.utils.enums.user_roles import UserRole
from app.utils.errors.exceptions import UnauthorizedException, ForbiddenException


def current_user_only():
    """
    Decorator to ensure that the user is accessing their own data.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            
            authenticated_user_id = kwargs.get('jwt_payload', {}).get('user_id')
            expected_user_id = kwargs.get("user_id", 0)
            if not authenticated_user_id:
                raise UnauthorizedException()
            if int(authenticated_user_id) != expected_user_id:
                raise ForbiddenException()
            import inspect
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def admin_only():
    """
    Decorator to ensure that the user has the required role.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get('jwt_payload')
            if not isinstance(user_role, dict):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JWT payload")
            user_role = user_role.get('role')
            if not user_role or user_role != UserRole.ADMIN:
                raise ForbiddenException()
            import inspect
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator



def authentication_required():
    """
    Decorator to ensure that the user has the required role.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get('jwt_payload')
            if not isinstance(user_role, dict):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JWT payload")
            user_role = user_role.get('role')
            if not user_role or user_role == UserRole.GUEST:
                raise UnauthorizedException()
            import inspect
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator




def role_required(required_role : List[UserRole]):
    """
    Decorator to ensure that the user has the required role.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get('jwt_payload')
            if not isinstance(user_role, dict):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JWT payload")
            user_role = user_role.get('role')
            if not user_role or user_role not in required_role:
                raise ForbiddenException("Trying to access a resource that requires a different role.")
            import inspect
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator