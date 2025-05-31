from fastapi import FastAPI
import uvicorn
from core.db.database import init_db
from core.config.config import Config
from users.routes.user_routes import user_router


application_config = Config()

app  = FastAPI(
    title=application_config.app_name,
    version=application_config.app_version,
    debug=application_config.debug,
)

init_db()


@app.get(path="/")
async def greet():
    return {"Hello": "World"}

@app.get(path="/health")
async def health_check():
    return {"status": "ok"}

app.include_router(user_router, prefix="/api/v1", tags=["users"])

if __name__ == "__main__" and application_config.debug:
    uvicorn.run(app, host=application_config.host, port=int(application_config.port), log_level="info")