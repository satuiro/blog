from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class BlogBase(BaseModel):
    title: str
    content: str


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    likes_count: int

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    blog_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
