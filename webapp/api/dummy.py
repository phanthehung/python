"""Endpoints module."""

from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from ..containers import Container
from ..service.dummy import DummyService

router = APIRouter()


@router.get("/dummy")
@inject
def getList(
        dummyService: DummyService = Depends(Provide[Container.dummyService]),
):
    return dummyService.say()
