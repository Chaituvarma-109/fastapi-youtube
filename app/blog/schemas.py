from pydantic import BaseModel
from typing import Union


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class Users(BaseModel):
    name: str
    email: str
    password: str


class ShowUsers(BaseModel):
    name: str
    email: str
    blogs: list[Blog] = []
    
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUsers
    
    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
