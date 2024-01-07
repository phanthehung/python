from webapp.domain.answer import Answer
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Submission(BaseModel):
    id_submission: Optional[int] = None
    answers: list[Answer]
    id_form: int
    score: Optional[int] = 0
    email: str
    updated_at: Optional[datetime] = None
