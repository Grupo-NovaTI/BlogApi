from functools import wraps
from typing import Callable, List
from starlette import status
from fastapi import HTTPException
from app.utils.enumns.user_roles import UserRole


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
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be an admin to perform this action.")
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
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be authenticated to perform this action.")
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
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You must have one of the roles {required_role} to perform this action.")
            import inspect
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator