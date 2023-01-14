# https://www.youtube.com/watch?v=7t2alSnE2-I
# store blog to database

from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id: {id} is not found")
    
    db.delete(synchronize_session=False)
    db.commit()
    
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    blog.update(request)
    db.commit()
    
    return 'updated'


@app.get('/blog', response_model=list[schemas.ShowBlog], tags=['blogs'])
def all_blog(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"blog with {id} not found"}
    return blog


@app.post('/user', response_model=schemas.ShowUsers, tags=['users'])
def create_user(request: schemas.Users, response: Response, db: Session=Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.Users(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUsers, tags=['users'])
def show_user(id: int, response: Response, db: Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found.")
    
    return user
