from pydantic import BaseModel, EmailStr, Field, field_validator


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    email: EmailStr
    name: str = "Admin"

    @field_validator('name')
    @classmethod
    def set_name(cls, name: str) -> str:
        if 'string' in name:
            raise ValueError('must not be hardcode string')
        return name or 'Admin'


class UserCreateSchema(UserBase):
    password: str = "$348789asd86745d6s34a36f75s"


class UserSchema(UserBase):
    id: str
    is_active: bool = Field(default=True)

    class Config:
        from_attributes = True
        validate_assignment = True
