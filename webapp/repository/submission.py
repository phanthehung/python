"""Repositories module."""
import json
from contextlib import AbstractContextManager
from typing import Callable
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from webapp.repository.models import SubmissionModel, AnswerModel, QuestionModel, datetime_format

from webapp.domain import submission, answer
from webapp.domain.question import QuestionType, text_questions
from webapp.domain.submission_stats import AnswerStats, Distribution
from collections import Counter
from typing import Union
import numpy as np

pagination_limit = 50


class SubmissionRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def create_submission(self, _submission: submission.Submission) -> int:
        with self.session_factory() as session:
            submission_model = SubmissionModel(
                fk_form=_submission.id_form,
                email=_submission.email,
                score=0,
                updated_at=datetime.now()
            )
            session.add(submission_model)
            session.flush()
            session.refresh(submission_model)

            answers = _submission.answers
            for ans in answers:
                ans_model = AnswerModel(
                    str_value=ans.str_value,
                    fk_question=ans.id_question,
                    fk_submission=submission_model.id_submission,
                    score=0,
                    updated_at=datetime.now()
                )
                session.add(ans_model)
            session.commit()
            return submission_model.id_submission

    def update_submission(self, _submission: submission.Submission) -> submission.Submission:
        with self.session_factory() as session:
            answer_models = session.query(AnswerModel).where(
                AnswerModel.fk_submission == _submission.id_submission).all()
            new_answers = dict()
            for ans in _submission.answers:
                new_answers[ans.id_answer] = ans

            for model in answer_models:
                model.str_value = new_answers[model.id_answer].str_value
                model.score = 0
                model.updated_at = datetime.now()

            submission_model = session.query(SubmissionModel).where(
                SubmissionModel.id_submission == _submission.id_submission).first()

            submission_model.score = 0
            submission_model.updated_at = datetime.now()

            session.commit()
            return _submission

    def get_submission(self, id_submission: int) -> submission.Submission:
        with self.session_factory() as session:
            answer_models = session.query(AnswerModel).where(AnswerModel.fk_submission == id_submission).all()
            answers = []
            for model in answer_models:
                ans = answer.Answer(
                    id_answer=model.id_answer,
                    str_value=model.str_value,
                    id_question=model.fk_question,
                    score=model.score,
                    updated_at=model.updated_at.timestamp()
                )
                answers.append(ans)

            submission_model = session.query(SubmissionModel).where(
                SubmissionModel.id_submission == id_submission).first()
            _submission = submission.Submission(
                id_submission=submission_model.id_submission,
                answers=answers,
                id_form=submission_model.fk_form,
                score=submission_model.score,
                email=submission_model.email,
                updated_at=submission_model.updated_at.timestamp()
            )

            return _submission

    def get_stats(self, id_question: int, next_cursor: Union[int, None]) -> AnswerStats:
        with self.session_factory() as session:
            question = session.query(QuestionModel).where(QuestionModel.id_question == id_question).first()
            question_type = QuestionType(question.type)

            if question_type in text_questions:
                if not next_cursor:
                    next_cursor = 9223372036854775807
                answers = session.query(AnswerModel).where(
                    AnswerModel.fk_question == id_question,
                    AnswerModel.id_answer <= next_cursor
                ).order_by(AnswerModel.id_answer.desc()).limit(pagination_limit).all()
                counter = Counter([ans.str_value for ans in answers])
                distribution = [Distribution(value=e, count=counter[e], percent=0) for e in counter]
                if len(answers) < pagination_limit:
                    next_cursor = -1
                else:
                    next_cursor = min([ans.id_answer for ans in answers]) - 1

                stats = AnswerStats(
                    id_question=id_question,
                    type=question_type,
                    distribution=distribution,
                    group=question.group,
                    next_cursor=next_cursor
                )

                return stats
            else:
                answers = session.query(AnswerModel.str_value, func.count(AnswerModel.str_value)).group_by(
                    AnswerModel.str_value).where(AnswerModel.fk_question == id_question).all()
                distributions = []
                total = sum([ans[1] for ans in answers])
                for ans in answers:
                    distributions.append(
                        Distribution(
                            value=ans[0],
                            count=ans[1],
                            percent=round((ans[1] / total), 2)
                        )
                    )

                stats = AnswerStats(
                    id_question=id_question,
                    type=question_type,
                    distribution=distributions,
                    group=question.group,
                    next_cursor=None
                )
                return stats

    def export_answers(self, id_form: int) -> list[dict]:
        with (self.session_factory() as session):
            answers = session.query(
                AnswerModel.str_value,
                AnswerModel.fk_submission,
                AnswerModel.fk_question,
                SubmissionModel.email,
                SubmissionModel.updated_at
            ).join(SubmissionModel, SubmissionModel.id_submission == AnswerModel.fk_submission).where(
                SubmissionModel.fk_form == id_form).all()

            submission_map = dict()
            for ans in answers:
                if ans.fk_submission not in submission_map:
                    submission_map[ans.fk_submission] = []
                submission_map[ans.fk_submission].append(ans)

            questions = session.query(QuestionModel).where(QuestionModel.fk_form == id_form).order_by(
                QuestionModel.id_question.asc()).all()

            header = {"timestamp": "timestamp", "email": "email"}
            for q in questions:
                header[q.id_question] = q.question

            output = [header]
            for id in submission_map:
                row = {"timestamp": submission_map[id][0].updated_at.strftime(datetime_format),
                       "email": submission_map[id][0].email}
                for ans in submission_map[id]:
                    row[ans.fk_question] = ans.str_value
                output.append(row)

            return output
