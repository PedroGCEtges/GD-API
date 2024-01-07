from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import ALGORITHM, SECRET_KEY
from database.mongodb import user_collection
from models.token import TokenData
from models.user import User, UserInDB
import hashlib

pwd_context_1 = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(plain_password):
    x = pwd_context_1.hash(plain_password)
    return x

def verify_password(plain_password, hashed_password):
    return pwd_context_1.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context_1.hash(password)


def get_user(db, username: str):
    user = db.find_one({"username": username})
    if user:
        return UserInDB(**user)
    else:
        raise HTTPException(status_code=404, detail=f'User {username} not found')

def get_user_by_email(db, email: str):
    user = db.find_one({"email": email})
    if user:
        return UserInDB(**user)
    else:
        raise HTTPException(status_code=404, detail=f'User {email} not found')
    
def authenticate_user(db, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = get_user(user_collection(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def is_admin(user: Annotated[User, Depends(get_current_user)]):
    if user.role == "admin":
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

