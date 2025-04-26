# Lesson 43 - Начинаем собственный API на Flask

## Зависимости
- Flask
- Peewee

Впишем это в requirements.txt:
```txt
flask
peewee
```

## Создаем окружение
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Наша система PeeWee моделей

У нас уже есть готовая база данных, и система таблиц и данные в ней. А так же описаны модели в файле `models.py`.
А так же есть файл `samples_peewee.py`, в котором примеры запросов из прошлого урока, модели, SQL структура и т.п.

Итак, наши модели:

```python
# 1. Установка peewee
# pip install peewee

# 2. Импортируем библиотеку peewee
import peewee as pw

# 3. Создаем подключение к базе данных SQLite
db = pw.SqliteDatabase("data/students_new.db")

# 4. Модель профессии
class Profession(pw.Model):
    title = pw.CharField(unique=True)
    description = pw.TextField(null=True)

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "professions"  # Указываем имя таблицы в базе данных


# 5. Модель группы
class Group(pw.Model):
    group_name = pw.CharField(unique=True)
    start_date = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    end_date = pw.DateTimeField(null=True)
    profession = pw.ForeignKeyField(Profession, backref="groups", null=True)

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "groups"  # Указываем имя таблицы в базе данных

# 6. Модель студента
class Student(pw.Model):
    first_name = pw.CharField()
    middle_name = pw.CharField(null=True)
    last_name = pw.CharField()
    age = pw.IntegerField(null=True)
    group = pw.ForeignKeyField(Group, backref="students", null=True)
    
    def __str__(self):
        return f"Имя: {self.first_name}, Фамилия: {self.last_name}, Возраст: {self.age}, Группа: {self.group.group_name}"
    
    def get_card(self):
        return self.student_cards[0].number if self.student_cards else None

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "students"  # Указываем имя таблицы в базе данных


# Добыть и распечатать студента
student_1 = Student.get(Student.id == 1)
print(student_1)


# Инвертаризация 
# Studentcard, teachers, teachers_groups, teachers_professions


# 7. Модель студенческого билета
class StudentCard(pw.Model):
    student = pw.ForeignKeyField(Student, backref="student_cards", unique=True)
    number = pw.CharField(unique=True)

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "student_cards"  # Указываем имя таблицы в базе данных


# 8. Модель преподавателя
class Teacher(pw.Model):
    first_name = pw.CharField(max_length=50)
    middle_name = pw.CharField(null=True, max_length=50)
    last_name = pw.CharField(max_length=50)
    age = pw.IntegerField(null=True)
    phone = pw.CharField(max_length=15)
    email = pw.CharField(null=True, max_length=50)


    def get_all_students(self):
        return Student.select().join(Group).join(TeacherGroup).where(TeacherGroup.teacher == self)

    def __str__(self):
        return f"Имя: {self.first_name}, Фамилия: {self.last_name}, Телефон: {self.phone}"

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "teachers"  # Указываем имя таблицы в базе данных


class TeacherGroup(pw.Model):
    teacher = pw.ForeignKeyField(Teacher, on_delete='SET NULL', on_update='CASCADE')
    group = pw.ForeignKeyField(Group, on_delete='SET NULL', on_update='CASCADE')
    date_start = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    
    def __str__(self):
        return f"Преподаватель {self.teacher.last_name} ведет группу {self.group.group_name} с {self.date_start}"
    
    class Meta:
        database = db  # База данных
        table_name = "teachers_groups"  # Имя таблицы
        primary_key = pw.CompositeKey('teacher', 'group')  # Составной первичный ключ



class TeacherProfession(pw.Model):
    teacher = pw.ForeignKeyField(Teacher, on_delete='SET NULL', on_update='CASCADE')
    profession = pw.ForeignKeyField(Profession, on_delete='SET NULL', on_update='CASCADE')
    notions = pw.TextField(null=True)  # Заметки о квалификации преподавателя
    
    def __str__(self):
        return f"Преподаватель {self.teacher.last_name} специализируется на {self.profession.title}"
    
    class Meta:
        database = db
        table_name = "teachers_professions"
        primary_key = pw.CompositeKey('teacher', 'profession')  # Составной первичный ключ

```

## Создание Hello World На Flask

Нам нужно создать файл `app.py` и в нем написать следующее:
```python
from flask import Flask, jsonify, request

# Сделать приложение
from flask import Flask, jsonify, request

# Сделать приложение
app = Flask(__name__)

# Создать маршрут
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Hello from Flask!")


if __name__ == '__main__':
    app.run(debug=True)
```

## TODO - Первое приложение на Flask

1. Создать пустую папку
2. Создать файл зависимостей `requirements.txt` и вписать туда `flask` и `peewee`
3. Создать окружение `venv` и установить зависимости
4. Создать файл `app.py` и написать туда код из примера выше
5. Запустить приложение командой `python app.py` в октивированном окружении
6. Перейти в браузере по адресу `http://127.0.0.1:5000`