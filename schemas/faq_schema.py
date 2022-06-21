import datetime as _dt

from pydantic import BaseModel


class Faq(BaseModel):
    question: str
    answer: str
