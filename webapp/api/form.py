"""Endpoints module."""

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from webapp.containers import Container
from webapp.service.form import FormService
from webapp.domain.form import Form
from typing import Annotated
from webapp.api.user import User, get_current_user, get_current_optional_user

router = APIRouter()


@router.post("/forms")
@inject
def create_form(
        form: Form,
        user: Annotated[User, Depends(get_current_user)],
        service: FormService = Depends(Provide[Container.form_service]),
):
    print("----------------------------------------------------")
    print(user.email)
    form.email = user.email
    print(form.email)
    return service.create_form(form)


@router.get("/forms/{id_form}")
@inject
def get_form(
        id_form: int,
        user: Annotated[User, Depends(get_current_optional_user)],
        service: FormService = Depends(Provide[Container.form_service]),
):
    return service.get_form(id_form, user)
