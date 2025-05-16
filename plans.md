# План развития проекта Flask API

Данный документ описывает поэтапный план улучшения и расширения текущего учебного проекта Flask API для управления учетными записями студентов.

## Текущее состояние проекта

Проект представляет собой REST API на базе Flask для управления данными студентов учебного заведения с использованием ORM Peewee. В настоящее время реализованы следующие функции:

- Получение списка всех студентов (с фильтрацией и сортировкой)
- Получение информации о конкретном студенте
- Создание новой записи о студенте
- Обновление данных студента
- Удаление студента

База данных также содержит таблицы для:
- Групп
- Профессий (специальностей)
- Преподавателей
- Студенческих билетов
- Связей между преподавателями и группами
- Специализаций преподавателей

Однако API реализовано только для работы с сущностью "Студент".

## Этап 1: Структуризация кода с использованием Blueprint

**Почему это важно**: Разделение кода на логические модули позволит:
- Легче ориентироваться в растущем проекте
- Независимо разрабатывать отдельные компоненты API
- Упростить тестирование
- Создать четкую структуру проекта

### План действий:

1. Создать структуру каталогов для Blueprint-ов
2. Реорганизовать код, выделив различные сущности в отдельные blueprint-ы

### Пример реализации:

#### 1. Структура проекта:

```
/flask_api_411
  /app
    __init__.py               # Инициализация приложения
    config.py                 # Конфигурация приложения
    /api
      __init__.py             # Сборка всех API Blueprint-ов
      /students
        __init__.py           # Blueprint для студентов
        routes.py             # Маршруты для студентов
      /teachers
        __init__.py           # Blueprint для преподавателей
        routes.py             # Маршруты для преподавателей
      /groups
        __init__.py           # Blueprint для групп
        routes.py             # Маршруты для групп
    /models
      __init__.py             # Инициализация моделей и базы данных
      students.py             # Модель Student
      teachers.py             # Модель Teacher
      groups.py               # Модель Group
      ...
  run.py                      # Точка входа в приложение
```

#### 2. Создание Blueprint для студентов:

```python
# app/api/students/__init__.py
from flask import Blueprint

students_bp = Blueprint('students', __name__, url_prefix='/api/students')

from . import routes
```

```python
# app/api/students/routes.py
from flask import request, jsonify, Response
import json
from app.models import Student, Group
from . import students_bp


@students_bp.route('/', methods=['GET'])
def get_students():
    try:
        # Получаем параметры запроса
        param = request.args.get("param")  # Параметр сортировки
        order = request.args.get("order", "asc")  # Порядок сортировки
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

        # ... остальной код функции ...
        
        # Формируем и возвращаем результат
```

#### 3. Создание основного приложения:

```python
# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False
    
    # Регистрация blueprints
    from app.api import students_bp, teachers_bp, groups_bp
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(groups_bp)
    
    return app
```

```python
# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

**Преимущества данного подхода**:
- Модульность - каждая сущность имеет свой Blueprint
- Масштабируемость - легко добавлять новые Blueprint-ы
- Чистая структура - код логически разделен по функциональности
- Легкая поддержка - проще понять, где что находится

## Этап 2: Валидация с использованием Pydantic

**Почему это важно**: 
- Автоматическая проверка входящих данных
- Четкие и информативные сообщения об ошибках
- Преобразование типов данных
- Сложная валидация через встроенные валидаторы

### План действий:

1. Установить Pydantic
2. Создать Pydantic-модели для валидации входящих данных
3. Интегрировать Pydantic с маршрутами API

### Пример реализации:

#### 1. Обновление requirements.txt:

```
peewee==3.17.9
flask==3.1.0
pydantic==2.6.1
email-validator==2.1.0  # для поддержки EmailStr
```

#### 2. Создание схем данных:

```python
# app/api/students/schemas.py
from typing import Optional
from pydantic import BaseModel, Field, validator
from app.models.models import Group

class StudentBase(BaseModel):
    """Базовые поля для студента"""
    first_name: str = Field(..., min_length=2, max_length=50, description="Имя студента")
    middle_name: Optional[str] = Field(None, max_length=50, description="Отчество студента")
    last_name: str = Field(..., min_length=2, max_length=50, description="Фамилия студента")
    age: int = Field(..., ge=16, le=100, description="Возраст студента")
    group: str = Field(..., description="Название группы студента")
    
    @validator('group')
    def validate_group_exists(cls, v):
        """Проверяем, существует ли указанная группа"""
        try:
            Group.get(Group.group_name == v)
            return v
        except Group.DoesNotExist:
            raise ValueError(f"Группа {v} не найдена в системе")

class StudentCreate(StudentBase):
    """Схема для создания нового студента"""
    pass

class StudentUpdate(StudentBase):
    """Схема для обновления студента"""
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=16, le=100)
    group: Optional[str] = None

class StudentResponse(BaseModel):
    """Схема для ответа с данными студента"""
    id: int
    name: str
    group: Optional[str] = None
    age: Optional[int] = None
    middle_name: Optional[str] = None
    
    class Config:
        orm_mode = True
```

#### 3. Использование схем в маршрутах:

```python
# app/api/students/routes.py
from flask import request, jsonify, Response
from pydantic import ValidationError
import json

from app.models.models import Student, Group
from . import students_bp
from .schemas import StudentCreate, StudentUpdate, StudentResponse


@students_bp.route('/create', methods=['POST'])
def create_student():
    try:
        # Получаем JSON из запроса
        data = request.get_json()
        if not data:
            return Response(
                json.dumps(
                    {"error": "Нет данных для создания студента"}, 
                    ensure_ascii=False
                ),
                status=400,
                mimetype="application/json; charset=utf-8",
            )
        
        # Валидируем данные с помощью Pydantic
        try:
            student_data = StudentCreate.model_validate(data)
        except ValidationError as e:
            return Response(
                json.dumps({"error": e.errors()}, ensure_ascii=False),
                status=400,
                mimetype="application/json; charset=utf-8",
            )
            
        # Получаем объект группы
        group = Group.get(Group.group_name == student_data.group)
            
        # Создаем нового студента
        student = Student.create(
            first_name=student_data.first_name,
            middle_name=student_data.middle_name,
            last_name=student_data.last_name,
            age=student_data.age,
            group=group,
        )
            
        # Возвращаем данные созданного студента
        response_data = {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "group": student.group.group_name if student.group else None,
            "age": student.age,
            "middle_name": student.middle_name,
        }
            
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            mimetype="application/json; charset=utf-8",
            status=201,
        )
            
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype="application/json; charset=utf-8",
        )
```

**Преимущества данного подхода**:
- Автоматическая валидация типов данных
- Информативные сообщения об ошибках
- Встроенные валидаторы для сложной логики
- Документация схем (для будущей интеграции со Swagger)
- Разделение логики валидации от бизнес-логики

## Этап 3: Оптимизация обработчиков с использованием MethodView

**Почему это важно**:
- Более чистый и организованный код
- Логическая группировка методов для одного ресурса
- Уменьшение дублирования кода
- Более удобная структура для RESTful API

### План действий:

1. Преобразовать функциональные обработчики в классы MethodView
2. Регистрировать views в Blueprint

### Пример реализации:

#### 1. Создание класса StudentAPI:

```python
# app/api/students/routes.py
from flask import request, jsonify, Response
from flask.views import MethodView
from pydantic import ValidationError
import json

from app.models.models import Student, Group
from . import students_bp
from .schemas import StudentCreate, StudentUpdate, StudentResponse


class StudentAPI(MethodView):
    """API для работы с отдельным студентом"""
    
    def get(self, id):
        """Получение данных студента по ID"""
        try:
            student = Student.get(Student.id == id)
            
            data = {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "group": student.group.group_name if student.group else None,
                "age": student.age,
                "middle_name": student.middle_name,
            }
            
            return Response(
                json.dumps(data, ensure_ascii=False),
                mimetype="application/json; charset=utf-8",
                status=200,
            )
        except Student.DoesNotExist:
            return Response(
                json.dumps({"error": "Студент не найден"}, ensure_ascii=False),
                status=404,
                mimetype="application/json; charset=utf-8",
            )
    
    def put(self, id):
        """Обновление данных студента"""
        # Находим студента по id
        try:
            student = Student.get(Student.id == id)
            
        except Student.DoesNotExist:
            return Response(
                json.dumps({"error": "Студент не найден"}, ensure_ascii=False),
                status=404,
                mimetype="application/json; charset=utf-8",
            )
            
        # Получаем данные из тела запроса
        data = request.get_json()
        
        # Проверяем, что данные были получены
        if not data:
            return Response(
                json.dumps(
                    {"error": "Нет данных для обновления студента"}, 
                    ensure_ascii=False
                ),
                status=400,
                mimetype="application/json; charset=utf-8",
            )
            
        # Валидируем данные с Pydantic
        try:
            student_data = StudentUpdate.model_validate(data)
        except ValidationError as e:
            return Response(
                json.dumps({"error": e.errors()}, ensure_ascii=False),
                status=400,
                mimetype="application/json; charset=utf-8",
            )
            
        # Обновляем данные студента
        if student_data.first_name:
            student.first_name = student_data.first_name
        if student_data.middle_name:
            student.middle_name = student_data.middle_name
        if student_data.last_name:
            student.last_name = student_data.last_name
        if student_data.age:
            student.age = student_data.age
        if student_data.group:
            try:
                group = Group.get(Group.group_name == student_data.group)
                student.group = group
            except Group.DoesNotExist:
                return Response(
                    json.dumps({"error": "Группа не найдена"}, ensure_ascii=False),
                    status=404,
                    mimetype="application/json; charset=utf-8",
                )
                
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
    
    def delete(self, id):
        """Удаление студента"""
        # Находим студента по id
        try:
            student = Student.get(Student.id == id)
            
        except Student.DoesNotExist:
            return Response(
                json.dumps({"error": "Студент не найден"}, ensure_ascii=False),
                status=404,
                mimetype="application/json; charset=utf-8",
            )
            
        # Если студент найден, удаляем его
        student.delete_instance()
        
        # Возвращаем ответ с сообщением об успешном удалении
        return Response(
            json.dumps({"message": "Студент успешно удален"}, ensure_ascii=False),
            status=200,
            mimetype="application/json; charset=utf-8",
        )


class StudentsListAPI(MethodView):
    """API для работы со списком студентов"""
    
    def get(self):
        """Получение списка студентов с фильтрацией и сортировкой"""
        # Реализация метода получения списка студентов
        pass
        
    def post(self):
        """Создание нового студента"""
        try:
            # Получаем JSON из запроса
            data = request.get_json()
            if not data:
                return Response(
                    json.dumps(
                        {"error": "Нет данных для создания студента"}, 
                        ensure_ascii=False
                    ),
                    status=400,
                    mimetype="application/json; charset=utf-8",
                )
            
            # Валидируем данные с помощью Pydantic
            try:
                student_data = StudentCreate.model_validate(data)
            except ValidationError as e:
                return Response(
                    json.dumps({"error": e.errors()}, ensure_ascii=False),
                    status=400,
                    mimetype="application/json; charset=utf-8",
                )
                
            # Получаем объект группы
            try:
                group = Group.get(Group.group_name == student_data.group)
            except Group.DoesNotExist:
                return Response(
                    json.dumps({"error": "Группа не найдена"}, ensure_ascii=False),
                    status=404,
                    mimetype="application/json; charset=utf-8",
                )
                
            # Создаем нового студента
            student = Student.create(
                first_name=student_data.first_name,
                middle_name=student_data.middle_name,
                last_name=student_data.last_name,
                age=student_data.age,
                group=group,
            )
                
            # Возвращаем данные созданного студента
            response_data = {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "group": student.group.group_name if student.group else None,
                "age": student.age,
                "middle_name": student.middle_name,
            }
                
            return Response(
                json.dumps(response_data, ensure_ascii=False),
                mimetype="application/json; charset=utf-8",
                status=201,
            )
                
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}, ensure_ascii=False),
                status=500,
                mimetype="application/json; charset=utf-8",
            )


# Регистрация представлений в Blueprint
students_bp.add_url_rule('/', 
                        view_func=StudentsListAPI.as_view('students_list'))
students_bp.add_url_rule('/<int:id>', 
                        view_func=StudentAPI.as_view('student'))
```

**Преимущества данного подхода**:
- Логическое разделение кода по HTTP-методам
- Более чистая и понятная структура
- Меньше дублирования кода
- RESTful подход к организации API
- Упрощенное расширение функционала

## Этап 4: Добавление базовой аутентификации по API ключам

**Почему это важно**:
- Защита API от несанкционированного доступа
- Контроль доступа к различным эндпоинтам
- Отслеживание использования API

### План действий:

1. Создать модель для хранения API ключей
2. Добавить декоратор для проверки API ключей
3. Применить декоратор к защищенным маршрутам

### Пример реализации:

#### 1. Добавление модели для API ключей:

```python
# app/models/api_keys.py
import peewee as pw
from .base import BaseModel

class ApiKey(BaseModel):
    key = pw.CharField(unique=True)
    user = pw.CharField()
    role = pw.CharField(default='user')  # 'admin', 'user', 'read_only', etc.
    active = pw.BooleanField(default=True)
    
    class Meta:
        table_name = 'api_keys'
```

#### 2. Создание утилиты для проверки API ключей:

```python
# app/utils/auth.py
from flask import request, Response, g
from functools import wraps
import json
from app.models.api_keys import ApiKey

def require_api_key(f):
    """Декоратор для проверки API ключа в заголовке запроса"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return Response(
                json.dumps({"error": "Требуется API ключ"}, ensure_ascii=False),
                status=401,
                mimetype="application/json; charset=utf-8",
            )
            
        try:
            key_record = ApiKey.get(ApiKey.key == api_key, ApiKey.active == True)
            # Сохраняем информацию о пользователе в контекст запроса
            g.user = key_record.user
            g.role = key_record.role
            
        except ApiKey.DoesNotExist:
            return Response(
                json.dumps({"error": "Недействительный API ключ"}, ensure_ascii=False),
                status=401,
                mimetype="application/json; charset=utf-8",
            )
            
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'role') or g.role != 'admin':
            return Response(
                json.dumps({"error": "Требуются права администратора"}, ensure_ascii=False),
                status=403,
                mimetype="application/json; charset=utf-8",
            )
        return f(*args, **kwargs)
    return decorated
```

#### 3. Применение декоратора к маршрутам:

```python
# app/api/students/routes.py (модифицированный пример)
from app.utils.auth import require_api_key, admin_required

class StudentsListAPI(MethodView):
    """API для работы со списком студентов"""
    
    decorators = [require_api_key]
    
    def get(self):
        """Получение списка студентов с фильтрацией и сортировкой"""
        # Доступно всем авторизованным пользователям
        pass
        
    @admin_required
    def post(self):
        """Создание нового студента (только для админов)"""
        # Доступно только админам
        pass

class StudentAPI(MethodView):
    """API для работы с отдельным студентом"""
    
    decorators = [require_api_key]
    
    def get(self, id):
        """Получение данных студента по ID"""
        # Доступно всем авторизованным пользователям
        pass
    
    @admin_required
    def put(self, id):
        """Обновление данных студента (только для админов)"""
        # Доступно только админам
        pass
    
    @admin_required
    def delete(self, id):
        """Удаление студента (только для админов)"""
        # Доступно только админам
        pass
```

#### 4. Скрипт для генерации API ключей:

```python
# scripts/generate_api_key.py
import sys
import secrets
sys.path.append('..')  # Добавляем родительский каталог в путь

from app.models.api_keys import ApiKey
from app.models.base import db

def generate_api_key(user, role='user'):
    """Генерирует новый API ключ для указанного пользователя"""
    key = secrets.token_hex(16)
    
    with db.atomic():
        api_key = ApiKey.create(
            key=key,
            user=user,
            role=role,
            active=True
        )
    
    return api_key

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python generate_api_key.py <username> [role]")
        sys.exit(1)
        
    username = sys.argv[1]
    role = sys.argv[2] if len(sys.argv) > 2 else 'user'
    
    api_key = generate_api_key(username, role)
    print(f"API ключ успешно создан:")
    print(f"Пользователь: {api_key.user}")
    print(f"Роль: {api_key.role}")
    print(f"Ключ: {api_key.key}")
```

**Преимущества данного подхода**:
- Простая реализация аутентификации
- Гибкая система ролей
- Возможность отключения API ключей
- Отсутствие необходимости в сложных механизмах авторизации (для учебного проекта)

## Дальнейшие перспективы развития проекта

После реализации четырех основных этапов проект можно развивать в следующих направлениях:

1. **Документирование API**:
   - Добавить автоматическую генерацию документации с использованием Swagger/OpenAPI
   - Создать интерактивную документацию для тестирования API

2. **Расширение функциональности**:
   - Добавить эндпоинты для работы с учебными расписаниями и занятиями
   - Создать систему оценок и аттестаций
   - Реализовать учет посещаемости занятий

3. **Улучшение безопасности**:
   - Перейти на JWT-аутентификацию
   - Добавить двухфакторную аутентификацию для административного доступа
   - Логирование действий пользователей

4. **Масштабирование**:
   - Переход с SQLite на PostgreSQL или MySQL
   - Контейнеризация приложения (Docker)
   - Настройка CI/CD

5. **Пользовательский интерфейс**:
   - Добавить веб-интерфейс для администраторов
   - Создать мобильное приложение для студентов и преподавателей

## Заключение

Поэтапная реализация предложенных улучшений позволит значительно улучшить архитектуру проекта, добавить новый функционал и обеспечить базовую безопасность API. Каждый этап логически продолжает предыдущий и создает основу для последующих улучшений.

Данный план ориентирован на реалистичную реализацию в рамках учебного проекта и охватывает наиболее важные аспекты разработки современного REST API на Flask.
