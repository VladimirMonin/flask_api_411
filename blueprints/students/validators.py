# 1. pip install pydantic
# Импорт pydantic для валидации данных и валидаторов

from pydantic import BaseModel, Field
from typing import Optional


class StudentValidator(BaseModel):
    """Модель для валидации данных студента"""

    first_name: str = Field(min_length=3, max_length=30, description="Имя студента")
    last_name: str = Field(min_length=3, max_length=30, description="Фамилия студента")
    middle_name: str = Field(
        min_length=3, max_length=30, description="Отчество студента"
    )
    age: int = Field(gt=0, le=120, description="Возраст студента")
    group: str = Field(
        min_length=3, max_length=30, description="Название группы студента"
    )
