from fastapi import FastAPI

app  = FastAPI()


@app.get(path="/")
async def greet():
    return {"Hello": "World"}

@app.get(path="/health")
async def health_check():
    return {"status": "ok"}

