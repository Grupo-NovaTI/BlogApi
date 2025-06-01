import uvicorn
from fastapi import FastAPI
from core.db.database import init_db
from users.routes.user_routes import user_router
from core.config.application_config import ApplicationConfig

# Gets the application global configuration
application_config = ApplicationConfig()

app = FastAPI(
    title=application_config.app_name,
    version=application_config.app_version,
    debug=application_config.debug,
)

# Initialize the database at application startup
init_db()


@app.get(path="/")
async def greet():
    return {"Hello": "World"}


@app.get(path="/health", description="Health check endpoint")
async def health_check():
    """Health check endpoint to verify the service is running.
    Returns:
        dict: A dictionary with the status of the service.
    """
    try:
        # Here you can add any health check logic, like checking database connection
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

app.include_router(user_router, prefix="/api/v1", tags=["users"])

if __name__ == "__main__" and application_config.debug:
    uvicorn.run(app, host=application_config.host, port=int(
        application_config.port), log_level="info")
