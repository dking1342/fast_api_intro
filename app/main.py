from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    print(db)
    return {"status": "success"}
