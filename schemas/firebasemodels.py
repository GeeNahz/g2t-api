import datetime as _dt
import os
from typing import Union
from uuid import UUID
from pydantic import Field, BaseModel, EmailStr, HttpUrl, FilePath

# remember to include things like 
# -> date post
# -> date updated 

class Comment(BaseModel):
    date: _dt.time
    comment: str

class CommentIn(Comment):
    pass

class CommentOut(CommentIn):
    user_id: int


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
    image: str | None = None
    user_id: str

class PostIn(Post):
    pass

class PostOut(Post):
    id: str
    date: _dt.datetime
    like: list[str] | None = None
    comment: list[CommentOut] | None = None

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }


class JobIn(BaseModel):
    position: str
    salary: str
    title: str
    job_description: str
    requirements: str | None = None
    location: str
    image: str | None = None
    company_name: str
    job_type: str | None = None
    link: str | None = None
    

class JobOut(JobIn):
    likes: list[str] | None = None
    comments: list[CommentOut] | None = None
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
    company_name: str | None = None
    socials: list[Socials] | None = None


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
    profile: UserProfile | None = None
    record: UserRecord | None = None

class Finduser(BaseModel):
    name: str
    university: str


class Message(BaseModel):
    message: str


# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
