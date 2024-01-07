from webapp.domain.answer import Answer
from webapp.domain.question import Question, QuestionType, list_questions
from fastapi import HTTPException


class AnswerValidator:
    def validate(self, answer: Answer, question: Question):
        pass


class ListAnswerValidator(AnswerValidator):
    def validate(self, answer: Answer, question: Question):
        if question.type in list_questions:
            if answer.str_value not in question.options:
                raise HTTPException(status_code=400, detail="answer must be match one of options")


class DateAnswerValidator(AnswerValidator):
    def validate(self, answer: Answer, question: Question):
        if question.type == QuestionType.DATE:
            pass


class TimeAnswerValidator(AnswerValidator):
    def validate(self, answer: Answer, question: Question):
        if question.type == QuestionType.TIME:
            pass
