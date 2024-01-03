from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    role: str | None = None

    @validator('role')
    def valid_role_admin(cls,v):
        if (v != 'admin') and (v!='operator'):
            raise ValueError(f'Non valid Role {v}')
        return v


class UserInDB(User):
    hashed_password: str