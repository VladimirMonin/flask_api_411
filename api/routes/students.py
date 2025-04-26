"""
Модуль маршрутов API для работы со студентами
===========================================

Этот модуль содержит маршруты API для работы со студентами:
- GET /api/student/{id}: получение студента по ID
- POST /api/students/create: создание нового студента
"""

from apiflask import APIBlueprint, Schema, abort
from apiflask.fields import Integer, String
from flask import g, Response, json
from models import Student, Group
from api.auth import token_required
from peewee import DoesNotExist

# Создаем Blueprint для маршрутов студентов
students_bp = APIBlueprint("students", __name__, url_prefix="/api")

# Определяем схемы данных для API


class StudentOutSchema(Schema):
    """Схема для отображения данных студента"""

    id = Integer()
    name = String()  # ФИО студента
    group = String(allow_none=True)  # Название группы
    age = Integer(allow_none=True)  # Возраст
    middle_name = String(allow_none=True)  # Отчество


class StudentCreateSchema(Schema):
    """Схема для создания нового студента"""

    first_name = String(required=True)
    last_name = String(required=True)
    middle_name = String()
    age = Integer()
    group_id = Integer()

    # Добавляем метаданные через класс Meta
    class Meta:
        # Описания полей
        field_descriptions = {
            "first_name": "Имя студента",
            "last_name": "Фамилия студента",
            "middle_name": "Отчество студента",
            "age": "Возраст студента",
            "group_id": "ID группы",
        }


# Маршрут для получения студента по ID
@students_bp.get("/student/<int:id>")
@students_bp.doc(
    summary="Получение студента по ID",
    description="Возвращает информацию о студенте по его уникальному идентификатору",
    responses={404: "Студент не найден"},
)
@students_bp.output(StudentOutSchema)
@token_required
def get_student_by_id(id):
    """
    Получение данных конкретного студента по его ID.

    Args:
        id (int): Идентификатор студента

    Returns:
        dict: Данные студента
    """
    try:
        student = Student.get(Student.id == id)

        return {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "group": student.group.group_name if student.group else None,
            "age": student.age,
            "middle_name": student.middle_name,
        }
    except Student.DoesNotExist:
        abort(404, "Студент не найден")


# Маршрут для создания студента
@students_bp.post("/students/create")
@students_bp.doc(
    summary="Создание нового студента",
    description="Создает новую запись о студенте в базе данных",
)
@students_bp.input(StudentCreateSchema)
@students_bp.output(StudentOutSchema, status_code=201)
@token_required
def create_student(data):
    """
    Создание новой записи о студенте.

    Args:
        data (dict): Данные нового студента

    Returns:
        dict: Данные созданного студента
    """
    try:
        # Начинаем транзакцию для безопасного создания
        with Student._meta.database.atomic():
            # Проверяем существование группы, если указан group_id
            group_id = data.get("group_id")
            if group_id:
                try:
                    Group.get_by_id(group_id)
                except DoesNotExist:
                    abort(400, f"Группа с ID {group_id} не найдена")

            student = Student.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_name=data.get("middle_name"),
                age=data.get("age"),
                group=group_id,
            )

            return {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "group": student.group.group_name if student.group else None,
                "age": student.age,
                "middle_name": student.middle_name,
            }
    except Exception as e:
        # В реальном проекте здесь стоит логировать ошибки
        abort(400, f"Ошибка при создании студента: {str(e)}")
