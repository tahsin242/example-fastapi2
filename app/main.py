from fastapi import FastAPI #Imports the FastAPI class from the fastapi framework/module.
from pydantic import BaseModel #Pydantic is a Python library for defining schemas (data models) and validating data against them. BaseModel is the base class that gives your schema all of Pydantic's functionality.Without inheriting from BaseModel, your class is just a normal Python class
# python -jose[cryptography] handles sigining and verifying
from . import models
from fastapi.middleware.cors import CORSMiddleware
from . database import engine , get_db
from .routers import post, user, auth, vote
from .config import settings


#models.Base.metadata.create_all(bind = engine) 
# commented this part because alembic does it well enough


app = FastAPI() #Creates an instance of the FastAPI application. app is the main object that handles requests and routes.

origins = ["*"]

app.add_middleware(
    CORSMiddleware,         #this runs before every operation
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)


# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id" : 1}, {"title": "favourite foods", "content":"I like pizza", "id" : 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #A decorator that defines a route. Tells FastAPI: "Run the next function when someone visits /."
async def root(): #Defines an asynchronous function named root. async allows FastAPI to handle many requests efficiently without blocking.
    return {"message": "Hello, World!"}

#To start a server = uvicorn main{this is the file name}:app{fastapi instance this is }

