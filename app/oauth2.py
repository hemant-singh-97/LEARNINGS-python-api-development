from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.setting import settings
from app import schemas, database, models

# This is the endpoint where the client will send the username and password to get the access token.
# The tokenUrl should be the same as the endpoint defined in the auth router for the login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login") 

# To create a token we need the following information:
# 1. A secret key, which is used to sign the token and verify its authenticity. This should be a long and random string to ensure the security of the token.
# 2. An algorithm, which is used to specify the hashing algorithm used to sign the token. The most commonly used algorithm is HS256 (HMAC with SHA-256).
# 3. An expiration time, which is used to specify the duration for which the token is valid. This is important to ensure that the token cannot be used indefinitely if it is compromised.

# This should be a long and random string to ensure the security of the token.
# It should be kept secret and not shared with anyone.
# In a production environment, it is recommended to use an environment variable to store the secret key instead of hardcoding it in the code.
SECRET_KEY = settings.OAUTH_SECRET_KEY # This key can be generated using the command: openssl rand -hex 32
ALGORITHM = settings.OAUTH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict) :
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) :
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    
    token =  verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user