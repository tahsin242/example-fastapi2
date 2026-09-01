from pydantic import BaseModel, EmailStr #Pydantic is a Python library for defining schemas (data models) and validating data against them. BaseModel is the base class that gives your schema all of Pydantic's functionality.Without inheriting from BaseModel, your class is just a normal Python class
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
    title: str
    content : str
    published : bool = True
    #rating : Optional[int] = None 

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at : datetime

    class Config:
        from_attributes = True



class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int 

    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]