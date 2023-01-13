from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {"Hello": "world"}


@app.get('/about')
def about():
    return {'about page': {'name': 'chaitu'}}
