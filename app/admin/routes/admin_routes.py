from fastapi import APIRouter, HTTPException, Path
from app.core.dependencies import AccessTokenDependency
from app.core.security.authentication_decorators import admin_only
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@admin_router.get("/admin-only", summary="Admin Only Endpoint", tags=["admin"])
@admin_only()
async def admin_only_endpoint(token: AccessTokenDependency):
    return {"message": "This is an admin-only endpoint", "user_id": token.get("user_id")}