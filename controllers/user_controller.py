from typing import Annotated
from fastapi import APIRouter, Security
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database.mongodb import user_collection
from models.token import Token

from models.user import User, UserInDB
from security import authenticate_user, create_access_token, get_current_active_user, get_current_user, hash_password, is_admin

route = APIRouter()

@route.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):  
    user = authenticate_user(user_collection(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@route.post("/createUser", response_description="Create a new user", 
            status_code=status.HTTP_201_CREATED,
            response_model=UserInDB)
async def create_user(user: User, password: str, admin: Annotated[get_current_user, Depends(is_admin)]):
    if admin.role != 'admin':
         print(admin)
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user_in_db = user_collection().find_one({"email": user.email})
    username_in_db = user_collection().find_one({"username": user.username})
    if user_in_db or username_in_db:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    dict_user = user.model_dump()
    dict_user['hashed_password'] = str(hash_password(password))
    new_user = UserInDB(**dict_user)
    user_collection().insert_one(new_user.model_dump())
    return new_user

@route.delete("/deleteUser", response_description="Delete user", 
            status_code=status.HTTP_200_OK)
async def delete_user(user: User, admin: Annotated[get_current_user, Depends(is_admin)]):
    if admin.role != 'admin':
         print(admin)
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        user_collection().delete_one({"email": user.email})
        return {"message": "User deleted successfully"}
    except Exception as e:
         raise(e)