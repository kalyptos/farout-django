"""Legacy schemas for backward compatibility"""
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


# Authentication Schemas (Old)
class UserLogin(BaseModel):
    """Schema for user login request"""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6)


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


# Item Schemas
class ItemIn(BaseModel):
    title: str

class ItemOut(BaseModel):
    id: int
    title: str

    model_config = {"from_attributes": True}

class Health(BaseModel):
    status: str


# Blog Post Schemas
class BlogPostCreate(BaseModel):
    heading: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=100)
    feature_image: str = Field(..., min_length=1, max_length=500)
    published: bool = True


class BlogPostUpdate(BaseModel):
    heading: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    feature_image: Optional[str] = Field(None, min_length=1, max_length=500)
    published: Optional[bool] = None


class BlogPostResponse(BaseModel):
    id: int
    heading: str
    content: str
    author: str
    feature_image: str
    created_at: datetime
    updated_at: datetime
    slug: str
    published: bool

    model_config = {"from_attributes": True}


class BlogPostListResponse(BaseModel):
    posts: list[BlogPostResponse]
    total: int
    page: int
    limit: int
    total_pages: int
