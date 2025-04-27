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

import re
from turtle import st
from flask import Flask, jsonify, request, Response
from models import Student, Group
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


# POST /api/students/create
# Создание новоо студента
@app.route("/api/students/create", methods=["POST"])
def create_student():
    try:
        # Пробуем получить данные из запроса
        data = request.get_json()

        # Проверяем, что данные были получены - если нет, то возвращаем ошибку
        if not data:
            return Response(
                json.dumps({"error": "Нет данных для создания студента"}, ensure_ascii=False),
                status=400,
                mimetype="application/json; charset=utf-8",
            )
        
        # Если тело запроса есть, мы добываем данные из него
        first_name = data.get("first_name")
        middle_name = data.get("middle_name")
        last_name = data.get("last_name")
        age = data.get("age")
        group = data.get("group")

        # Если мы НЕ получили данные из тела запроса, то возвращаем ошибку
        if not all([first_name, middle_name, last_name, age, group]):
            return Response(
                json.dumps({"error": "Не все данные для создания студента были предоставлены"}, ensure_ascii=False),
                status=400,
                mimetype="application/json; charset=utf-8",
            )
        
        # Для создания нового студента нам нужен экземпляр группы
        try:
            group = Group.get(Group.group_name == group)
        except Group.DoesNotExist:
            return Response(
                json.dumps({"error": "Группа не найдена"}, ensure_ascii=False),
                status=404,
                mimetype="application/json; charset=utf-8",
            )
        
        # Создаем нового студента
        student = Student.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            age=age,
            group=group,
        )

        # Возвращаем ответ с данными созданного студента
        data = {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "group": student.group.group_name if student.group else None,
            "age": student.age,
            "middle_name": student.middle_name,
        }

        json_data = json.dumps(data, ensure_ascii=False)

        return Response(
            json_data,
            mimetype="application/json; charset=utf-8",
            status=201,
        )
    
    except Exception as e:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype="application/json; charset=utf-8",
        )
    

# DELETE /api/student/{id}/delete
# Удаление студента по id
@app.route("/api/student/<int:id>/delete", methods=["DELETE"])
def delete_student(id):
    # Находим студента по id
    try:
        student = Student.get(Student.id == id)
    
    # Если студент НЕ найден, возвращаем ошибку
    except Student.DoesNotExist:
        return Response(
            json.dumps({"error": "Студент не найден"}, ensure_ascii=False),
            status=404,
            mimetype="application/json; charset=utf-8",
        )
    
    # Если студент найден, то удаляем его
    student.delete_instance()

    # Возвращаем ответ с сообщением об успешном удалении
    return Response(
        json.dumps({"message": "Студент успешно удален"}, ensure_ascii=False),
        status=200,
        mimetype="application/json; charset=utf-8",
    )

# PUT /api/student/{id}/update
# Обновление данных студента по id
@app.route("/api/student/<int:id>/update", methods=["PUT"])
def update_student(id):
    # Находим студента по id
    try:
        student = Student.get(Student.id == id)
    
    # Если студент НЕ найден, возвращаем ошибку
    except Student.DoesNotExist:
        return Response(
            json.dumps({"error": "Студент не найден"}, ensure_ascii=False),
            status=404,
            mimetype="application/json; charset=utf-8",
        )
    
    # Получаем данные из тела запроса
    data = request.get_json()

    # Проверяем, что данные были получены - если нет, то возвращаем ошибку
    if not data:
        return Response(
            json.dumps({"error": "Нет данных для обновления студента"}, ensure_ascii=False),
            status=400,
            mimetype="application/json; charset=utf-8",
        )
    
    # Если тело запроса есть, мы добываем данные из него
    first_name = data.get("first_name")
    middle_name = data.get("middle_name")
    last_name = data.get("last_name")
    age = data.get("age")
    group = data.get("group")

    # Если мы НЕ получили данные из тела запроса, то возвращаем ошибку
    if not all([first_name, middle_name, last_name, age, group]):
        return Response(
            json.dumps({"error": "Не все данные для обновления студента были предоставлены"}, ensure_ascii=False),
            status=400,
            mimetype="application/json; charset=utf-8",
        )
    
    # Для создания нового студента нам нужен экземпляр группы
    try:
        group = Group.get(Group.group_name == group)
    except Group.DoesNotExist:
        return Response(
            json.dumps({"error": "Группа не найдена"}, ensure_ascii=False),
            status=404,
            mimetype="application/json; charset=utf-8",
        )
    
    # Обновляем данные студента
    student.first_name = first_name
    student.middle_name = middle_name
    student.last_name = last_name
    student.age = age
    student.group = group

    # Сохраняем изменения в базе данных
    student.save()

    # Возвращаем ответ с данными обновленного студента
    data = {
        "id": student.id,
        "name": f"{student.first_name} {student.last_name}",
        "group": student.group.group_name if student
        .group else None,
        "age": student.age,
        "middle_name": student.middle_name,
    }

    response_data = json.dumps(data, ensure_ascii=False)

    return Response(
        response_data,
        mimetype="application/json; charset=utf-8",
        status=200,
    )


if __name__ == "__main__":
    # 2. Запустили приложение на локальном сервере
    app.run(debug=True)