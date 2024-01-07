"""Application module."""

from fastapi import FastAPI

from webapp.containers import Container
from webapp.api import dummy, form, submission, schedule, user


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(dummy.router)
    app.include_router(form.router)
    app.include_router(submission.router)
    app.include_router(schedule.router)
    app.include_router(user.router)
    return app


app = create_app()
