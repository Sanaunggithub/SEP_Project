from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime, date
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class AccountStatusEnum(str, Enum):
    active = "active"
    suspended = "suspended"
    inactive = "inactive"

class UserBase(BaseModel):
    full_name:               str
    email:                   EmailStr
    phone_number:            Optional[str] = None
    date_of_birth:           Optional[date] = None  # ← Optional
    gender:                  Optional[GenderEnum] = None  # ← Optional
    address:                 Optional[str] = None   # ← Optional
    emergency_contact_name:  Optional[str] = None   # ← Optional
    emergency_contact_phone: Optional[str] = None   # ← Optional

class UserCreate(UserBase):
    password:   str
    role:       RoleEnum     = RoleEnum.student
    department: Optional[str] = None  # ← add
    program:    Optional[str] = None  # ← add
    
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    department:              Optional[str] = None  # ← add
    program:                 Optional[str] = None

class UserResponse(UserBase):
    id: str
    role: RoleEnum
    account_status: AccountStatusEnum
    profile_picture_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
