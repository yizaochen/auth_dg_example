import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routers import register, auth, employees, refresh, logout, users
import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(register.router)
app.include_router(auth.router)
app.include_router(refresh.router)
app.include_router(employees.router)
app.include_router(logout.router)
app.include_router(users.router)


@app.get("/")
def index():
    return {"version": "v001, 2024-07-21T19:21:34.899985"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3500, log_level="info", host="localhost")
