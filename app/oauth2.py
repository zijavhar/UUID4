from http.client import HTTPException
import time
from fastapi import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "gh{j%R4j#h34kF34hk578346y48@pA]_G3ryh$&*T^#4ghjfg76itgY$GJG67sfdsdgfhjsdg3w7t"
ALGORITHM = "HS256"
EXPIRATION_TIME = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, creds_exception):
    try:
        data = jwt.decode(token, SECRET_KEY, ALGORITHM)
    
        id = data.get("user_id")

        if id is None:
            raise creds_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise creds_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exception = HTTPException(status_code=401, detail="Could not validate creds", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, creds_exception)
