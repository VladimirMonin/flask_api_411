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
        param (str, необязательный):
            Признак сортировки. Допустимые значения: 'last_name', 'group', 'age'.
        order (str, необязательный):
            Порядок сортировки. Допустимые значения: 'asc', 'desc'.
            По умолчанию сортировка производится по возрастанию.
        filter (str, необязательный):
            Фильтрация студентов по группе. Допустимые ключи: `group
            Фильтр допустим только один. Но может быть использован с параметрами.

        Примеры:
            /api/students?param=last_name&order=asc - Все студенты, отсортированные по фамилии по возрастанию
            /api/students?filter=python411&param=age&order=desc - Все студенты из группы python411, отсортированные по возрасту по убыванию

    Возвращает:
        JSON-массив объектов студентов:
        [
            {
                "id": 1,
                "name": "Фласка Джанговна",
                "group": "python411",
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

from flask import Flask, request, Response
from models import Student, Group
import json

# 1. Создали экземпляр приложения Flask
app = Flask(__name__)


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
                json.dumps(
                    {"error": "Нет данных для создания студента"}, ensure_ascii=False
                ),
                status=400,
                mimetype="application/json; charset=utf-8",
            )

        # Получаем список полей модели (кроме id, который автоматически генерируется)
        valid_fields = [name for name in Student._meta.fields.keys() if name != 'id']

        # Создаём словарь с данными для нового студента
        student_data = {}
        
        # Проходим по всем полям модели и заполняем словарь данными из запроса
        for field_name in valid_fields:
            if field_name in data:
                # Особая обработка для поля-связи с другой таблицей
                if field_name == 'group':
                    try:
                        student_data[field_name] = Group.get(Group.group_name == data.get(field_name))
                    except Group.DoesNotExist:
                        return Response(
                            json.dumps({"error": "Группа не найдена"}, ensure_ascii=False),
                            status=404,
                            mimetype="application/json; charset=utf-8",
                        )
                else:
                    student_data[field_name] = data.get(field_name)

        # Проверяем, что все обязательные поля заполнены
        required_fields = ['first_name', 'last_name', 'age', 'group']
        if not all(field in student_data for field in required_fields):
            return Response(
                json.dumps(
                    {"error": "Не все обязательные данные предоставлены"},
                    ensure_ascii=False,
                ),
                status=400,
                mimetype="application/json; charset=utf-8",
            )

        # Создаём студента одной командой, распаковывая словарь в параметры
        student = Student.create(**student_data)

        

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
            json.dumps(
                {"error": "Нет данных для обновления студента"}, ensure_ascii=False
            ),
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
            json.dumps(
                {"error": "Не все данные для обновления студента были предоставлены"},
                ensure_ascii=False,
            ),
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
        "group": student.group.group_name if student.group else None,
        "age": student.age,
        "middle_name": student.middle_name,
    }

    response_data = json.dumps(data, ensure_ascii=False)

    return Response(
        response_data,
        mimetype="application/json; charset=utf-8",
        status=200,
    )


# GET /api/students
# Получение списка всех студентов
@app.route("/api/students", methods=["GET"])
def get_students():
    try:
        # Получаем параметры запроса
        param = request.args.get("param")  # Параметр сортировки
        order = request.args.get(
            "order", "asc"
        )  # Порядок сортировки (по умолчанию 'asc')
        filter_group = request.args.get("filter")  # Фильтрация по группе

        # Начинаем с базового запроса
        query = Student.select()

        # Применяем фильтрацию по группе, если указана
        if filter_group:
            try:
                # Находим группу по имени
                group = Group.get(Group.group_name == filter_group)
                # Фильтруем студентов по найденной группе
                query = query.where(Student.group == group)
            
            except Group.DoesNotExist:
                return Response(
                    json.dumps({"error": "Группа не найдена"}, ensure_ascii=False),
                    status=404,
                    mimetype="application/json; charset=utf-8",
                )

        # Применяем сортировку, если параметр указан
        if param:
            # Определяем поле для сортировки
            if param == "last_name":
                sort_field = Student.last_name
            elif param == "age":
                sort_field = Student.age
            elif param == "group":
                # Для сортировки по группе нужно использовать join
                query = query.join(Group)
                sort_field = Group.group_name
            else:
                return Response(
                    json.dumps(
                        {"error": "Некорректный параметр сортировки"},
                        ensure_ascii=False,
                    ),
                    status=400,
                    mimetype="application/json; charset=utf-8",
                )

            # Применяем направление сортировки если desc
            if order.lower() == "desc":
                query = query.order_by(sort_field.desc())
            # Если asc, то по умолчанию
            else:
                query = query.order_by(sort_field.asc())

        # Выполняем запрос и формируем список студентов
        students_data = []
        for student in query:
            students_data.append(
                {
                    "id": student.id,
                    "name": f"{student.first_name} {student.last_name}",
                    "group": student.group.group_name if student.group else None,
                    "age": student.age,
                    "middle_name": student.middle_name,
                }
            )

        # Возвращаем результат
        return Response(
            json.dumps(
                {"success": True, "students": students_data}, ensure_ascii=False
            ),
            mimetype="application/json; charset=utf-8",
            status=200,
        )

    except Exception as e:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        return Response(
            json.dumps({"success": False, "error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype="application/json; charset=utf-8",
        )


if __name__ == "__main__":
    # 2. Запустили приложение на локальном сервере
    app.run(debug=True)
