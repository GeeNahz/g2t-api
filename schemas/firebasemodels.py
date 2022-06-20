import datetime as _dt
import os
from typing import Optional, List, Union
from uuid import UUID
from pydantic import Field, BaseModel, EmailStr, HttpUrl, FilePath

# remember to include things like 
# -> date post
# -> date updated 

class Comment(BaseModel):
    comment: str

class CommentIn(Comment):
    pass

class CommentOut(CommentIn):
    date: _dt.datetime
    user_id: str

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }


Post_Model = {
    "Post ID",
    "Userid",
    "Title",
    "body",
    "create_Date => timestamp",
    # "modified_Date => timestamp",
    "Image = > link",
    "Likes = > Array of user ids",
    "Comments = > Array = > {userid, comment, timestamp}"

}

class Post(BaseModel):
    name: str
    body: str
    image: Optional[str] = None
    user_id: str

class PostIn(Post):
    pass

class PostOut(Post):
    id: str
    date: _dt.datetime
    like: Optional[List[str]] = None
    comment:Optional[List[CommentOut]] = None

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }


class JobIn(BaseModel):
    position: str
    salary: str
    title: str
    job_description: str
    requirements: Optional[str] = None
    location: str
    image: Optional[str] = None
    company_name: str
    job_type: Optional[str] = None
    link: Optional[str] = None
    

class JobOut(JobIn):
    likes: Optional[List[str]]= None
    comments: Optional[List[CommentOut]]= None
    id: str
    date: _dt.datetime

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }


class Socials(BaseModel):
    name: str

class Contact(BaseModel):
    email: EmailStr
    name: str
    phone: int
    address: str
    location: str
    company_name: Optional[str] = None
    socials: Optional[List[Socials]]= None


class ContactIn(Contact):
    pass

class ContactOut(Contact):
    id: str
    date_created: _dt.datetime
    date_updated: _dt.datetime

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }


class Faq(BaseModel):
    question: str
    answer: str


class UserProfile(BaseModel):
    name: str
    email: EmailStr
    phone: str
    matric: str

class UserRecord(BaseModel):
    university: str
    degree: str
    place_of_work: str

class User(BaseModel):
    profile: Optional[UserProfile] = None
    record: Optional[UserRecord] = None

class Finduser(BaseModel):
    name: str
    university: str


class Message(BaseModel):
    message: str
