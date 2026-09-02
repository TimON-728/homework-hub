from pydantic import BaseModel, field_validator, model_validator

class HomeworkCreate(BaseModel):
    subject: str
    task: str
    photo: list[str] = []

    @field_validator('subject')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Название не может быть пустым')
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
            raise('Город, школа или класс не могут быть пустыми')
        return v.strip()