import datetime as _dt

from pydantic import BaseModel, EmailStr
from typing import Optional


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
