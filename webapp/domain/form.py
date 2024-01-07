from webapp.domain.question import Question
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Form(BaseModel):
    id_form: Optional[int] = None
    email: Optional[str] = None
    questions: list[Question]
    instant_scoring: bool
    show_wrong_answer: bool
    show_correct_answer: bool
    see_single_score: bool
    login_required: bool
    allow_resubmit: bool
    show_progress: bool
    shuffle_questions: bool
    send_copy: bool
    is_test: bool
    updated_at: Optional[datetime] = None
