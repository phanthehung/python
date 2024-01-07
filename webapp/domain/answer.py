from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Answer(BaseModel):
    id_answer: Optional[int] = None
    str_value: str
    id_question: int
    score: Optional[int] = 0
    updated_at: Optional[datetime] = None
