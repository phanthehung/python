from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy import update

from webapp.repository.models import ScheduledEmail, ScheduleModel, datetime_hour_format, FormModel
from webapp.domain.schedule import Schedule
from webapp.api.user import User
from fastapi import HTTPException

import pandas as pd
import uuid
from datetime import datetime


class ScheduleRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def send_scheduled_emails(self):
        now = pd.Timestamp.now().round('60min').to_pydatetime().timestamp()
        execution = str(uuid.uuid4())
        with self.session_factory() as session:
            schedules = session.query(ScheduleModel).where(ScheduleModel.date_time <= now).all()

        for schedule in schedules:
            if schedule.execution:
                continue

            with self.session_factory() as session:
                session.execute(
                    update(ScheduleModel).where(ScheduleModel.id_schedule == schedule.id_schedule).values(
                        execution=execution))
                session.commit()

            with self.session_factory() as session:
                updated_schedule = session.query(ScheduleModel).where(ScheduleModel.execution == execution).first()

            if not updated_schedule:
                continue

            with self.session_factory() as session:
                emails = session.query(ScheduledEmail).where(ScheduledEmail.fk_schedule == schedule.id_schedule).all()
            for email in emails:
                print("sending email for " + str(email))

    def create_schedule(self, schedule: Schedule, user: User):
        with self.session_factory() as session:
            form = session.query(FormModel).where(FormModel.id_form == schedule.id_form).first()
            if form.email != user.email:
                raise HTTPException(status_code=403, detail="Cannot create schedule for form")


            schedule_model = ScheduleModel(
                fk_form=schedule.id_form,
                date_time=datetime.strptime(schedule.date_time, datetime_hour_format).timestamp(),
                updated_at=datetime.now(),
            )
            session.add(schedule_model)
            session.flush()

            emails = [ScheduledEmail(email=email, fk_schedule=schedule_model.id_schedule) for email in schedule.emails]
            session.add_all(emails)
            session.commit()
