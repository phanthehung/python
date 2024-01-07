"""Repositories module."""
import json
from contextlib import AbstractContextManager
from typing import Callable
from datetime import datetime
from sqlalchemy.orm import Session

from webapp.repository.models import FormModel, QuestionModel

from webapp.domain import form, question


class FormRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def create_form(self, _form: form.Form) -> int:
        with self.session_factory() as session:
            form_model = FormModel(
                is_test=_form.is_test,
                email=_form.email,
                instant_scoring=_form.instant_scoring,
                show_wrong_answer=_form.show_wrong_answer,
                show_correct_answer=_form.show_correct_answer,
                see_single_score=_form.see_single_score,
                login_required=_form.login_required,
                allow_resubmit=_form.allow_resubmit,
                show_progress=_form.show_progress,
                shuffle_questions=_form.shuffle_questions,
                send_copy=_form.send_copy,
                updated_at=datetime.now()
            )
            session.add(form_model)
            session.flush()
            session.refresh(form_model)

            questions = _form.questions
            for q in questions:
                question_model = QuestionModel(
                    type=q.type.value,
                    question=q.question,
                    group=q.group,
                    required=q.required,
                    options=json.dumps(q.options),
                    score=q.score,
                    fk_form=form_model.id_form,
                    allow_multi=q.allow_multi,
                    updated_at=datetime.now()
                )
                session.add(question_model)
            session.commit()
            return form_model.id_form

    def get_form(self, id_form: int) -> form.Form:
        with self.session_factory() as session:
            question_models = session.query(QuestionModel).where(QuestionModel.fk_form == id_form).all()
            questions = []
            for model in question_models:
                q = question.Question(
                    id_question=model.id_question,
                    type=question.QuestionType(model.type),
                    question=model.question,
                    group=model.group,
                    required=model.required,
                    options=json.loads(model.options),
                    score=model.score,
                    allow_multi=model.allow_multi,
                    updated_at=model.updated_at.timestamp()
                )
                questions.append(q)

            form_model = session.query(FormModel).where(FormModel.id_form == id_form).first()
            _form = form.Form(
                id_form=form_model.id_form,
                email=form_model.email,
                questions=questions,
                instant_scoring=form_model.instant_scoring,
                show_wrong_answer=form_model.show_wrong_answer,
                show_correct_answer=form_model.show_correct_answer,
                see_single_score=form_model.see_single_score,
                login_required=form_model.login_required,
                allow_resubmit=form_model.allow_resubmit,
                show_progress=form_model.show_progress,
                shuffle_questions=form_model.shuffle_questions,
                send_copy=form_model.send_copy,
                is_test=form_model.is_test,
                updated_at=form_model.updated_at.timestamp()
            )

            return _form
