# https://www.youtube.com/watch?v=7t2alSnE2-I
# store blog to database

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user


app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)


models.Base.metadata.create_all(bind=engine)
