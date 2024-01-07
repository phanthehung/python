from webapp.domain.question import Question, list_questions, text_questions, grid_questions
from fastapi import HTTPException


class QuestionValidator:
    def validate(self, question: Question):
        pass


class ListQuestionValidator(QuestionValidator):

    def validate(self, question: Question):
        if question.type in list_questions:
            if question.options is None or len(question.options) < 1:
                raise HTTPException(status_code=400, detail="you must provide options for list question")


class TextQuestionValidator(QuestionValidator):

    def validate(self, question: Question):
        if question.type in text_questions:
            if question.options is not None:
                raise HTTPException(status_code=400, detail="text question must not have predefined options")


class GridQuestionValidator(QuestionValidator):

    def validate(self, question: Question):
        if question.type in grid_questions:
            if not question.group or len(question.group.strip()) < 1:
                raise HTTPException(status_code=400, detail="Group is required for grid questions")
