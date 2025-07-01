from functools import wraps
from typing import Callable, List
from starlette import status
from fastapi import HTTPException
from app.utils.enumns.user_roles import UserRole


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
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in JWT payload")
            if int(authenticated_user_id) != expected_user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only access your own data.")
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