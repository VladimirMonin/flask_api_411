"""
API для управления учетными записями студентов
===============================================

Этот модуль предоставляет RESTful API для работы с данными студентов.
Все маршруты начинаются с префикса `/api/`.

Доступные маршруты
-----------------

GET /api/students
----------------
    Получение списка всех студентов.

    Параметры запроса:
        order (str, необязательный):
            Порядок сортировки. Допустимые значения: 'asc', 'desc'.
            По умолчанию сортировка производится по возрастанию.

    Возвращает:
        JSON-массив объектов студентов:
        [
            {
                "id": 1,
                "name": "Иван Иванов",
                "group": "Группа-101",
                ...
            },
            ...
        ]

POST /api/students/create
-----------------------
    Создание записи о новом студенте.

    Тело запроса (JSON):
        {
            "name": "Имя Фамилия",
            "group": "Группа-XXX",
            ...другие поля...
        }

    Возвращает:
        JSON-объект созданного студента с присвоенным id:
        {
            "id": 123,
            "name": "Имя Фамилия",
            "group": "Группа-XXX",
            ...
        }

GET /api/student/{id}
------------------
    Получение данных конкретного студента по его идентификатору.

    Параметры пути:
        id (int): Уникальный идентификатор студента.

    Возвращает:
        JSON-объект студента:
        {
            "id": 1,
            "name": "Иван Иванов",
            "group": "Группа-101",
            ...
        }

PUT /api/student/{id}/update
-------------------------
    Обновление данных студента.

    Параметры пути:
        id (int): Уникальный идентификатор студента.

    Тело запроса (JSON):
        {
            "name": "Новое Имя",
            "group": "Новая-Группа",
            ...поля для обновления...
        }

    Возвращает:
        JSON-объект обновленного студента:
        {
            "id": 1,
            "name": "Новое Имя",
            "group": "Новая-Группа",
            ...
        }

DELETE /api/student/{id}/delete
---------------------------
    Удаление записи о студенте.

    Параметры пути:
        id (int): Уникальный идентификатор студента.

    Возвращает:
        JSON с результатом операции:
        {
            "success": true,
            "message": "Студент успешно удален"
        }
"""

from flask import Flask, jsonify, request, Response
from models import Student
import json

# 1. Создали экземпляр приложения Flask
app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False


# GET /api/student/{id}
# http://127.0.0.1:5000/api/student/1
# <int:id> - это тип данных, который будет передан в функцию как параметр id
# Функция будет вызываться в формате get_student_by_id(id=1)
@app.route("/api/student/<int:id>", methods=["GET"])
def get_student_by_id(id):
    try:
        student = Student.get(Student.id == id)

        data = {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "group": student.group.group_name if student.group else None,
            "age": student.age,
            "middle_name": student.middle_name,
        }

        # Явно указываем ensure_ascii=False для корректной работы с кириллицей
        json_data = json.dumps(data, ensure_ascii=False)

        return Response(
            json_data,
            # application - это тип контента, который мы отправляем
            # json - формат данных, который мы отправляем
            # charset - кодировка, в которой мы отправляем данные
            mimetype="application/json; charset=utf-8",
            status=200,
        )
    except Student.DoesNotExist:
        return Response(
            json.dumps({"error": "Студент не найден"}, ensure_ascii=False),
            status=404,
            mimetype="application/json; charset=utf-8",
        )


if __name__ == "__main__":
    # 2. Запустили приложение на локальном сервере
    app.run(debug=True)
