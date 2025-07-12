"""
Admin API routes for admin-only endpoints.

This module defines FastAPI routes that are accessible only to admin users.
"""

from fastapi import APIRouter
from app.core.dependencies import AccessTokenDependency
from app.core.security.authentication_decorators import admin_only

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@admin_router.get("/admin-only", summary="Admin Only Endpoint", tags=["admin"])
@admin_only()
async def admin_only_endpoint(token: AccessTokenDependency):
    """
    Endpoint accessible only to admin users.

    Args:
        token (AccessTokenDependency): The JWT payload containing user information.

    Returns:
        dict: A message indicating admin access and the user ID.
    """
    return {"message": "This is an admin-only endpoint", "user_id": token.get("user_id")}