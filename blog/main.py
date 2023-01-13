# https://www.youtube.com/watch?v=7t2alSnE2-I
# store blog to database

from fastapi import FastAPI
from . import schemas, models
from .database import engine


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


@app.post('/blog')
def create(request: schemas.Blog):
    return {'title': request.title, 'body': request.body}
