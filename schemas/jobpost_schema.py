import datetime as _dt

from pydantic import BaseModel
from typing import Optional, List

from schemas.comment_schema import CommentOut


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
    likes: Optional[List[str]] = None
    comments: Optional[List[CommentOut]] = None
    id: str
    date: _dt.datetime

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }
