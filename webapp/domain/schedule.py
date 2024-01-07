from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Schedule(BaseModel):
    id_form: int
    date_time: str
    emails: list[str]
    updated_at: Optional[datetime] = None
