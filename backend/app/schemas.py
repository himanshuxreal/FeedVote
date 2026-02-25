from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema"""
    pass


class User(UserBase):
    """User schema"""
    id: int

    class Config:
        from_attributes = True


class FeedbackBase(BaseModel):
    """Base feedback schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)

    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('description')
    def description_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty or whitespace only')
        return v.strip()


class FeedbackCreate(FeedbackBase):
    """Feedback creation schema"""
    pass


class Feedback(FeedbackBase):
    """Feedback schema"""
    id: int
    user_id: int
    created_at: datetime
    vote_count: Optional[int] = 0

    class Config:
        from_attributes = True


class VoteBase(BaseModel):
    """Base vote schema"""
    feedback_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    vote_type: str = Field(..., pattern="^(upvote|downvote)$")


class VoteCreate(VoteBase):
    """Vote creation schema"""
    pass


class Vote(VoteBase):
    """Vote schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackWithVotes(Feedback):
    """Feedback schema with vote details"""
    votes: List[Vote] = []


class TopIdea(BaseModel):
    """Top idea schema (for leaderboard)"""
    id: int
    title: str
    description: str
    vote_count: int
    username: str
    upvotes: int = 0
    downvotes: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
