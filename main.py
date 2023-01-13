from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


app = FastAPI()


@app.get('/blog')
def index(published: bool, limit: int=10, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} blogs from db"}
    else:
        return {"data": 'all blogs'}


@app.get('/blog/unpublished')
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int, limit: int=10):
    return {"data": f"comments on blog {id}"}


@app.post('/blog')
def create_blog(blog: Blog):
    return {"data": f"blog is created with title as {blog.title}"}


# if __name__ == "__main__":
#     uvicorn.run(app, host='127.0.0.1', port=9000)
