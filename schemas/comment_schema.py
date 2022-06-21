import datetime as _dt

from pydantic import BaseModel



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
