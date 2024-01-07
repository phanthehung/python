"""Services module."""

from webapp.domain.form import Form
from webapp.repository.form import FormRepository
from webapp.service.validator.question_validator import QuestionValidator
from webapp.api.user import User
from fastapi import HTTPException
from typing import Union


class FormService:
    def __init__(self, form_repository: FormRepository, validators: list[QuestionValidator]):
        self.validators = validators
        self._repository: FormRepository = form_repository

    def create_form(self, _form: Form) -> Form:
        for q in _form.questions:
            for validator in self.validators:
                validator.validate(q)
        id_form = self._repository.create_form(_form)
        return self._repository.get_form(id_form)

    def get_form(self, id_form: int, user: Union[User, None]) -> Form:
        form = self._repository.get_form(id_form)
        if form.login_required and (not user or form.email != user.email):
            raise HTTPException(status_code=403, detail="Cannot get form")
        return form
