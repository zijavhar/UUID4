import sqlite3
from fastapi import APIRouter, Depends, status, HTTPException
from ..database import db
from .. import schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Auth'])

@router.post('/signup', status_code=201)
def signup(user_creds: OAuth2PasswordRequestForm = Depends(), db_conn = Depends(db.connect)):
    try:
        db.add_user(db_conn, user_creds.username, utils.hash(user_creds.password))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this name is already taken")

@router.post('/signin')
def signin(user_creds: OAuth2PasswordRequestForm = Depends(), db_conn = Depends(db.connect)):
    # fetching our user data from db
    user = db.get_user_by_name(db_conn, user_creds.username)
    # if username does not exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid creds")
    
    if not utils.verify(user_creds.password, user[2]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid creds")

    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user[0]})
    return {"token": access_token, "token_type": "bearer"}