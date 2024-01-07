"""Endpoints module."""

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from webapp.containers import Container
from webapp.service.submission import SubmissionService
from webapp.domain.submission import Submission
from typing import Union
from fastapi.responses import StreamingResponse
import io
import pandas as pd

router = APIRouter()


@router.post("/submissions")
@inject
def submit(
        submission: Submission,
        service: SubmissionService = Depends(Provide[Container.submission_service]),
):
    return service.submit(submission)


@router.put("/submissions")
@inject
def resubmit(
        submission: Submission,
        service: SubmissionService = Depends(Provide[Container.submission_service]),
):
    return service.update_submission(submission)


@router.get("/submissions/{id_submission}")
@inject
def get_submission(
        id_submission: int,
        service: SubmissionService = Depends(Provide[Container.submission_service]),
):
    return service.get_submission(id_submission)


@router.get("/questions/stats/{id_question}")
@inject
def get_question_stats(
        id_question: int,
        next_cursor: Union[int, None] = None,
        service: SubmissionService = Depends(Provide[Container.submission_service]),

):
    return service.get_question_stats(id_question, next_cursor)


@router.get("/submissions/export/{id_form}")
@inject
def export_submissions(
        id_form: int,
        service: SubmissionService = Depends(Provide[Container.submission_service]),

):
    data = service.export_submissions(id_form)
    df = pd.DataFrame.from_dict(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False, header=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response
