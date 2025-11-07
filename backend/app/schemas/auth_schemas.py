from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    discord_id: Optional[str] = None
    username: str
    discriminator: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None
    role: str
    rank_image: Optional[str] = None
    must_change_password: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Password change schema
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

# Member schemas
class MemberBase(BaseModel):
    discord_id: str
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class MemberResponse(BaseModel):
    id: int
    discord_id: str
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    rank: str
    missions_completed: list
    trainings_completed: list
    stats: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Admin user management schemas
class UserRoleUpdate(BaseModel):
    role: str = Field(..., pattern="^(member|admin)$")

class UserRankUpdate(BaseModel):
    rank: str = Field(..., min_length=1, max_length=50)
    rank_image: Optional[str] = Field(None, max_length=500)

class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    limit: int
    pages: int

    class Config:
        from_attributes = True

# User profile schema (combined auth + member data)
class UserProfileResponse(BaseModel):
    username: str
    discord_id: Optional[str] = None
    email: Optional[str] = None
    role: str
    rank: str = "member"
    rank_image: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    member_id: Optional[int] = None
    member_data: Optional[dict] = None

    class Config:
        from_attributes = True
