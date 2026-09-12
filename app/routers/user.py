from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

from ..celery_worker import send_welcome_email

from fastapi import File, UploadFile
import os, uuid
from app.config import settings


router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    #hash the password - user.password 

    hasehed_password = utils.hash(user.password)
    user.password = hasehed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_welcome_email.delay(new_user.email)

    return new_user



@router.get("/{id}", response_model = schemas.UserOut)
def get_users(id: int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")

    return user


@router.post("/upload-avatar", status_code=200)
async def upload_avatar(
    file: UploadFile = File(...), 
    current_user: int = Depends(oauth2.get_current_user)
):
    # 1. Validate the file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    # 2. Generate a unique filename so we don't overwrite existing ones
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # 3. Define the path where we want to save it
    # This points to the 'app/static/images' folder we created on the VM
    file_location = f"app/static/images/{unique_filename}"

    # 4. Save the file to the server's hard drive
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    # 5. Generate the URL to access the image
    # This matches the '/static' mount we created in main.py
    image_url = f"/static/images/{unique_filename}"

    return {"message": "Image uploaded successfully", "image_url": image_url}