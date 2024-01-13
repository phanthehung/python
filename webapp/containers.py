"""Containers module."""
import os
from dependency_injector import containers, providers

from webapp.database import Database
from webapp.service.form import FormService
from webapp.service.submission import SubmissionService
from webapp.repository.form import FormRepository
from webapp.repository.submission import SubmissionRepository
from webapp.repository.schedule import ScheduleRepository
from webapp.service.validator.question_validator import TextQuestionValidator, ListQuestionValidator, \
    GridQuestionValidator
from webapp.service.validator.answer_validator import ListAnswerValidator, DateAnswerValidator, TimeAnswerValidator


def get_url() -> str:
    user = os.getenv("POSTGRES_USER", "admin")
    password = os.getenv("POSTGRES_PASSWORD", "secret")
    server = os.getenv("POSTGRES_SERVER", "localhost")
    db = os.getenv("POSTGRES_DB", "local-db")
    return f"postgresql+psycopg://{user}:{password}@{server}/{db}"


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "webapp.api.form",
        "webapp.api.submission",
        "webapp.api.schedule",
        "webapp.api.user"
    ])

    db = providers.Singleton(Database, db_url=get_url())

    question_validators = [TextQuestionValidator(), ListQuestionValidator(), GridQuestionValidator()]
    answer_validators = [ListAnswerValidator(), DateAnswerValidator(), TimeAnswerValidator()]

    form_repo = providers.Factory(FormRepository, session_factory=db.provided.session)
    form_service = providers.Factory(FormService, form_repository=form_repo, validators=question_validators)

    submission_repo = providers.Factory(SubmissionRepository, session_factory=db.provided.session)
    submission_service = providers.Factory(
        SubmissionService,
        submission_repository=submission_repo,
        validators=answer_validators,
        form_service=form_service
    )

    schedule_repo = providers.Factory(ScheduleRepository, session_factory=db.provided.session)
