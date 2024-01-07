from typing import Optional
from pydantic import BaseModel
from webapp.domain.question import QuestionType
from collections import Counter


class Distribution(BaseModel):
    value: str
    count: int
    percent: float


class AnswerStats(BaseModel):
    id_question: int
    type: QuestionType
    distribution: Optional[list[Distribution]] = None
    group: Optional[str] = None
    next_cursor: Optional[int] = None
