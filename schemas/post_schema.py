import datetime as _dt

from pydantic import BaseModel
from typing import Optional, List

from schemas.comment_schema import CommentOut


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
    comment: Optional[List[CommentOut]] = None

    class Config:
        json_encoders = {
            _dt.datetime: lambda v: v.timestamp(),
        }
