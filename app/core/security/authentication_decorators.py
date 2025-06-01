from typing import Callable, List


def admin_only(func):
    """
    Decorator to ensure that the user is an admin.
    """
    def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if not user or not user.is_admin:
            raise PermissionError("You must be an admin to perform this action.")
        return func(*args, **kwargs)
    return wrapper

def authentication_required(func : Callable):
    """
    Decorator to ensure that the user is authenticated.
    """
    def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if not user or not user.is_superuser:
            raise PermissionError("You must be a superuser to perform this action.")
        return func(*args, **kwargs)
    return wrapper


def role_required(required_roles : List[str]):
    """
    Decorator to ensure that the user has the required role.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_role = kwargs.get('role')
            if not user_role or user_role not in required_roles:
                raise PermissionError(f"You must have one of the roles {required_roles} to perform this action.")
            return func(*args, **kwargs)
        return wrapper
    return decorator