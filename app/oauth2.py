from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


SECRECT_KEY = settings.secret_key

ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms = [ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = str(id))

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token : str = Depends(oauth2_scheme) ):        # we use this one just to fetch the data from the base as the verify access token returns the token_data
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate" : "Bearer"})

    return verify_access_token(token, credentials_exception)
