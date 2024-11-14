from pydantic import BaseModel, Field, BeforeValidator, conint, EmailStr
from typing import List, Optional, Annotated
from bson import ObjectId
from datetime import datetime

# Custom ObjectId handling
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None
    description: Optional[str] = None
    role: str = "user"
    followers: Optional[List[PyObjectId]] = []
    following: Optional[List[PyObjectId]] = []

    class Config:
        json_encoders = {ObjectId: str}


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    uploaded_videos: List[PyObjectId] = []
    saved_videos: List[PyObjectId] = []
    reacted_videos: List[PyObjectId] = []
    channels: List[PyObjectId] = []
    total_likes: int = 0
    total_followers: int = 0
    date_joined: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# Token Models

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class VideoBase(BaseModel):
    title: Optional[str] = None
    video: Optional[str] = None
    poster: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []

    class Config:
        json_encoders = {ObjectId: str}


class VideoCreate(VideoBase):
    uploader: PyObjectId


class Video(VideoBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    uploader: PyObjectId
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    last_modified: Optional[datetime] = None
    views: int = 0
    likes: int = 0
    comments: List[PyObjectId] = []

    class Config:
        populate_by_name = True


# Comment Models

class CommentBase(BaseModel):
    content: str
    likes: int = 0

    class Config:
        json_encoders = {ObjectId: str}


class CommentCreate(CommentBase):
    user_id: PyObjectId
    video_id: PyObjectId


class Comment(CommentBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    video_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# Channel Models

class ChannelBase(BaseModel):
    name: str
    description: Optional[str] = None
    followers: List[PyObjectId] = []
    total_followers: int = 0
    total_likes: int = 0
    videos: List[PyObjectId] = []

    class Config:
        json_encoders = {ObjectId: str}


class ChannelCreate(ChannelBase):
    owner_id: PyObjectId


class Channel(ChannelBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# Actor Models

class ActorBase(BaseModel):
    name: str
    profile_image: Optional[str] = None
    biography: Optional[str] = None
    total_likes: int = 0
    videos: List[PyObjectId] = []

    class Config:
        json_encoders = {ObjectId: str}


class ActorCreate(ActorBase):
    pass


class Actor(ActorBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# User Follow Models

class FollowBase(BaseModel):
    follower_id: PyObjectId
    following_id: PyObjectId

    class Config:
        json_encoders = {ObjectId: str}


class Follow(FollowBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# Popularity Models

class PopularVideo(BaseModel):
    video_id: PyObjectId
    views: int
    likes: int

    class Config:
        json_encoders = {ObjectId: str}


class PopularUser(BaseModel):
    user_id: PyObjectId
    total_followers: int

    class Config:
        json_encoders = {ObjectId: str}


class PopularChannel(BaseModel):
    channel_id: PyObjectId
    total_followers: int

    class Config:
        json_encoders = {ObjectId: str}