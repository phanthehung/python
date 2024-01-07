from webapp.domain.submission import Submission
from webapp.repository.submission import SubmissionRepository
from webapp.service.validator.answer_validator import AnswerValidator
from webapp.service.form import FormService
from webapp.domain.submission_stats import AnswerStats
from typing import Union
from fastapi import HTTPException


class SubmissionService:
    def __init__(self,
                 submission_repository: SubmissionRepository,
                 validators: list[AnswerValidator],
                 form_service: FormService
                 ):
        self.validators = validators
        self.repository: SubmissionRepository = submission_repository
        self.form_service = form_service

    def submit(self, submission: Submission) -> Submission:
        answer_map = dict()
        for ans in submission.answers:
            answer_map[ans.id_question] = ans

        self.__validate_submission(submission)
        id_submission = self.repository.create_submission(submission)
        return self.repository.get_submission(id_submission)

    def get_submission(self, id_submission: int) -> Submission:
        return self.repository.get_submission(id_submission)

    def update_submission(self, submission: Submission) -> Submission:
        if not submission.id_submission:
            raise HTTPException(status_code=400, detail="submission id must not be null")

        self.__validate_submission(submission)
        return self.repository.update_submission(submission)

    def __validate_submission(self, submission: Submission):
        answer_map = dict()
        for ans in submission.answers:
            answer_map[ans.id_question] = ans

        form = self.form_service.get_form(submission.id_form)
        for q in form.questions:
            if q.required and q.id_question not in answer_map:
                raise HTTPException(status_code=400, detail="A required question was not answered")
            if q.id_question not in answer_map:
                continue
            for validator in self.validators:
                validator.validate(answer_map[q.id_question], q)

    def get_question_stats(self, id_question: int, next_cursor: Union[int, None]) -> AnswerStats:
        return self.repository.get_stats(id_question, next_cursor)

    def export_submissions(self, id_form: int) -> list[dict]:
        return self.repository.export_answers(id_form)
