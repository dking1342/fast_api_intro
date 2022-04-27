from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# routers
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"detail": "Hello World"}
