import uvicorn
from fastapi import FastAPI
from database import engine
from routers import register
import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(register.router)


@app.get("/")
def index():
    return {"version": "v001, 2024-07-21T19:21:34.899985"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3500, log_level="info", host="localhost")
