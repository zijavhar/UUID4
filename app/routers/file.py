from fileinput import filename
from pickletools import int4
from fastapi import APIRouter, Depends, Form, UploadFile, status, HTTPException
from typing import Optional
from .. import oauth2
from ..database import db
from .. import schemas

router = APIRouter(tags=['File'])

# creating file instanse
@router.post('/files', status_code=201)
def create_file(file: UploadFile =  Form(...), filename: str = Form(...), access_id: int = Form(...), 
user: schemas.TokenData = Depends(oauth2.get_current_user), db_conn = Depends(db.connect)):
    file_location = f"files/{filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    db.create_file(db_conn, filename, access_id, user.id)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@router.get('/files', status_code=200)
def get_files(db_conn = Depends(db.connect), user: schemas.TokenData = Depends(oauth2.get_current_user)):
    files = db.get_files(db_conn, user.id)
    return files

#@router.put('/files', status_code=200)
#def update_file(db_conn = Depends(db.connect), user: schemas.TokenData = Depends(oauth2.get_current_user)):
