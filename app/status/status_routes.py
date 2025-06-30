from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from app.core.config.application_config import ApplicationConfig
from app.core.dependencies import provide_application_config

from app.utils.logger.application_logger import ApplicationLogger

_logger: ApplicationLogger = ApplicationLogger(name=__name__, log_to_console=False)

app = APIRouter(
    tags=["status"],
    responses={404: {"description": "Not found"}},
)


@app.get(path="/", description="Root endpoint", tags=["status"], include_in_schema=False)
async def home(config: ApplicationConfig = Depends(provide_application_config)) -> HTMLResponse:
    return HTMLResponse(content=f"""
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
        <h1>Welcome to {config.app_version}!!</h1>
        <p>Version: {config.app_version}</p>
        <p>Welcome to the FastAPI application. Use the endpoints to interact with the service.</p>
        <p>Check the <a href="/docs">API documentation</a> for more details.</p>
        <p>For a quick overview, visit the <a href="/redoc">ReDoc documentation</a>.</p>
    </div>
</body>
</html>
""")
@app.get(path="/info", description="Get application information", tags=["status"])
async def get_info(config: ApplicationConfig = Depends(provide_application_config)):
    return {
        "name": config.app_name,
        "version": config.app_version,
        "debug": config.debug
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