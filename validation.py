from pydantic import BaseModel, field_validator, model_validator
from datetime import date, timedelta

class HomeworkCreate(BaseModel):
    city: str
    school: str
    class_name: str

    subject: str
    task: str
    photo: list[str] = []

    @field_validator('city', 'school', 'class_name', 'subject')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Поле не может быть пустым')
        return v.strip()

    @model_validator(mode='after')
    def check_task_or_photo(self):
        if not self.task.strip() and not self.photo:
            raise ValueError('Задание и фото не могут быть одновременно пустыми')
        return self


class Registration(BaseModel):
    city: str
    school: str
    class_name: str

    @field_validator('city', 'school', 'class_name')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Город, школа или класс не могут быть пустыми')
        return v.strip()


class TimetableCreate(BaseModel):
    city: str
    school: str
    class_name: str
    
    timetable: str
    date_on: date

    @field_validator('city', 'school', 'class_name', 'timetable')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Поле не может быть пустым')
        return v.strip()

    @field_validator('date_on')
    @classmethod
    def not_past(cls, v: date) -> date:
        today = date.today()
        if v < today:
            raise ValueError('Нельзя сделать расписание на прошедшую дату')
        if v > today + timedelta(days=14):
            raise ValueError('Нельзя сделать расписание дальше чем на 2 недели')
        return v
