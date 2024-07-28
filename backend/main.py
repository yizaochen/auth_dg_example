import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from routers import register, auth, employees, refresh, logout, users
from routers.register.routes import router as register_router
from routers.auth.routes import router as auth_router
from routers.refresh.routes import router as refresh_router
from routers.logout.routes import router as logout_router
from routers.users.routes import router as users_router


from core.database import Base, engine

Base.metadata.create_all(bind=engine)


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

app.include_router(register_router)
app.include_router(auth_router)
app.include_router(refresh_router)
app.include_router(logout_router)
app.include_router(users_router)


# app.include_router(register.router)
# app.include_router(auth.router)
# app.include_router(refresh.router)
# app.include_router(employees.router)
# app.include_router(logout.router)
# app.include_router(users.router)


@app.get("/")
def index():
    return {"version": "v001, 2024-07-21T19:21:34.899985"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3500, log_level="info", host="localhost")
