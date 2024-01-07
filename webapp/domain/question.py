from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class QuestionType(Enum):
    TEXT = "text"
    MULTI_CHOICE = "multi_choice"
    MULTI_BOX = "multi_box"
    DROPDOWN = "dropdown"
    FILE = "file"
    RANGE = "range"
    DATE = "date"
    TIME = "time"
    MULTI_CHOICE_GRID = "multi_choice_grid"
    MULTI_BOX_GRID = "multi_box_grid"


class Question(BaseModel):
    id_question: Optional[int] = None
    question: str
    group: Optional[str] = None
    type: QuestionType
    required: bool
    options: Optional[list[str]] = None
    score: Optional[int] = 0
    allow_multi: Optional[bool] = False
    updated_at: Optional[datetime] = None


list_questions = [
    QuestionType.MULTI_CHOICE,
    QuestionType.MULTI_BOX,
    QuestionType.DROPDOWN,
    QuestionType.RANGE,
    QuestionType.MULTI_CHOICE_GRID,
    QuestionType.MULTI_BOX_GRID,
]

grid_questions = [
    QuestionType.MULTI_CHOICE_GRID,
    QuestionType.MULTI_BOX_GRID,
]

text_questions = [
    QuestionType.TEXT,
    QuestionType.FILE,
    QuestionType.DATE,
    QuestionType.TIME,
]
