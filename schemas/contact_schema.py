import datetime as _dt

from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Socials(BaseModel):
    name: str


class Contact(BaseModel):
    email: EmailStr
    name: str
    phone: int
    address: str
    location: str
    company_name: Optional[str] = None
    socials: Optional[List[Socials]] = None


class ContactIn(Contact):
    pass


class ContactOut(Contact):
    id: str
    date_created: _dt.datetime

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }
