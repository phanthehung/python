"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, BigInteger, JSON, Index, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

datetime_format = "%m/%b/%Y %H:%M:%S"
datetime_hour_format = "%m/%d/%Y %H:%M"


class QuestionModel(Base):
    __tablename__ = "question"

    id_question = Column(BigInteger, primary_key=True, autoincrement="auto")
    type = Column(String)
    question = Column(String, nullable=False)
    group = Column(String)
    required = Column(Boolean, default=False)
    options = Column(JSON)
    score = Column(Integer)
    fk_form = Column(BigInteger, nullable=False)
    allow_multi = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP(True))


Index("question_form_idx", QuestionModel.fk_form)


class FormModel(Base):
    __tablename__ = "form"

    id_form = Column(BigInteger, primary_key=True, autoincrement="auto")
    email = Column(String, nullable=False)
    is_test = Column(Boolean, default=False)
    instant_scoring = Column(Boolean, default=False)
    show_wrong_answer = Column(Boolean, default=False)
    show_correct_answer = Column(Boolean, default=False)
    see_single_score = Column(Boolean, default=False)
    login_required = Column(Boolean, default=False)
    allow_resubmit = Column(Boolean, default=False)
    show_progress = Column(Boolean, default=False)
    shuffle_questions = Column(Boolean, default=False)
    send_copy = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP(True))


class AnswerModel(Base):
    __tablename__ = "answer"

    id_answer = Column(BigInteger, primary_key=True, autoincrement="auto")
    str_value = Column(String, nullable=False)
    fk_question = Column(BigInteger, nullable=False)
    fk_submission = Column(BigInteger, nullable=False)
    score = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP(True))


Index("answer_question_idx", AnswerModel.fk_question)
Index("answer_submission_idx", AnswerModel.fk_submission)


class SubmissionModel(Base):
    __tablename__ = "submission"

    id_submission = Column(BigInteger, primary_key=True, autoincrement="auto")
    fk_form = Column(BigInteger, nullable=False)
    email = Column(String, nullable=False)
    score = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP(True))


Index("submission_form_idx", SubmissionModel.fk_form)


class ScheduleModel(Base):
    __tablename__ = "schedule"

    id_schedule = Column(BigInteger, primary_key=True, autoincrement="auto")
    fk_form = Column(BigInteger, nullable=False)
    date_time = Column(BigInteger, nullable=False)
    execution = Column(String, nullable=True)
    updated_at = Column(TIMESTAMP(True))


Index("schedule_date_time_index", ScheduleModel.date_time)


class ScheduledEmail(Base):
    __tablename__ = "scheduled_email"

    id_schedule_email = Column(BigInteger, primary_key=True, autoincrement="auto")
    fk_schedule = Column(BigInteger, nullable=False)
    email = Column(String, nullable=False)


Index("scheduled_email_schedule_index", ScheduledEmail.fk_schedule)
