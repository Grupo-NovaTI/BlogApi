from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse
from app.core.db.database import init_db
from app.users.routes.user_routes import user_router
from app.comments.routes.comment_routes import comment_router
from app.blogs.routes.blog_routes import blog_router
from app.auth.routes.auth_routes import auth_router
from app.tags.routes.tag_routes import tag_router
from app.core.config.application_config import ApplicationConfig
from app.utils.logger.application_logger import ApplicationLogger
from app.core.dependencies.dependencies import provide_application_config

_logger : ApplicationLogger = ApplicationLogger(name=__name__, log_to_console=False)
# Gets the application global configuration
application_config: ApplicationConfig = provide_application_config()

app = FastAPI(
    title=application_config.app_name,
    version=application_config.app_version,
    debug=application_config.debug,
)

# Initialize the database at application startup
init_db()


@app.get(path="/", description="Root endpoint", tags=["status"], include_in_schema=False)
async def home():
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Application</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }}
        h1 {{
            color: #4CAF50;
            text-align: center;
            margin-top: 20px;
        }}
        p {{
            text-align: center;
            font-size: 18px;
            margin: 10px 0;
        }}
        a {{
            color: #4CAF50;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to {app.title}!!</h1>
        <p>Version: {app.version}</p>
        <p>Welcome to the FastAPI application. Use the endpoints to interact with the service.</p>
        <p>Check the <a href="/docs">API documentation</a> for more details.</p>
        <p>For a quick overview, visit the <a href="/redoc">ReDoc documentation</a>.</p>
    </div>
</body>
</html>
""")
@app.get(path="/info", description="Get application information", tags=["status"])
async def get_info():
    return {
        "name": app.title,
        "version": app.version,
        "debug": app.debug
    }


@app.get(path="/health", description="Health check endpoint", tags=["status"])
async def health_check():
    """Health check endpoint to verify the service is running.
    Returns:
        dict: A dictionary with the status of the service.
    """
    try:
        # Here you can add any health check logic, like checking database connection
        return {"status": "ok"}
    except Exception as e:
        _logger.log_error(message=f"Health check failed: {str(e)}")
        return {"status": "error", "detail": str(e)}

app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(comment_router, prefix="/api/v1", tags=["comments"])
app.include_router(blog_router, prefix="/api/v1", tags=["blogs"])
app.include_router(tag_router, prefix="/api/v1", tags=["tags"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

