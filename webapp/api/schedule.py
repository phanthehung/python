from fastapi_utilities import repeat_at
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from webapp.containers import Container
from webapp.repository.schedule import ScheduleRepository
from webapp.domain.schedule import Schedule
from typing import Annotated
from webapp.api.user import User, get_current_user

router = APIRouter()


@router.on_event("startup")
@repeat_at(cron="0 * * * *")
@inject
def send_form(
        repository: ScheduleRepository = Depends(Provide[Container.schedule_repo])
):
    repository.send_scheduled_emails()


@router.post("/schedules")
@inject
def create_schedule(
        schedule: Schedule,
        user: Annotated[User, Depends(get_current_user)],
        repository: ScheduleRepository = Depends(Provide[Container.schedule_repo]),
):
    return repository.create_schedule(schedule, user)
