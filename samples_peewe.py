"""
СТРУКТУРА БД:
--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.16 в Вс апр 13 12:38:43 2025
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL UNIQUE,
    start_date TEXT DEFAULT CURRENT_TIMESTAMP,
    end_date TEXT,
    profession_id INTEGER,
    FOREIGN KEY (profession_id) REFERENCES professions(id) ON DELETE SET NULL  ON UPDATE CASCADE
);
INSERT INTO groups (id, group_name, start_date, end_date, profession_id) VALUES (1, 'python411', '2025-04-12 09:14:07', NULL, 6);
INSERT INTO groups (id, group_name, start_date, end_date, profession_id) VALUES (2, 'js412', '2025-04-12 09:14:07', NULL, 5);

-- Таблица: professions
DROP TABLE IF EXISTS professions;
CREATE TABLE IF NOT EXISTS professions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT
);
INSERT INTO professions (id, title, description) VALUES (3, 'Frontend-разработчик', 'Создание пользовательского интерфейса веб-приложений на JavaScript');
INSERT INTO professions (id, title, description) VALUES (4, 'Backend-разработчик', 'Разработка серверной части веб-приложений на Python');
INSERT INTO professions (id, title, description) VALUES (5, 'Frontend-разработчик_2', 'Создание пользовательского интерфейса веб-приложений на JavaScript');
INSERT INTO professions (id, title, description) VALUES (6, 'Backend-разработчик_2', 'Разработка серверной части веб-приложений на Python');

-- Таблица: student_cards
DROP TABLE IF EXISTS student_cards;
CREATE TABLE IF NOT EXISTS student_cards (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_id INTEGER NOT NULL UNIQUE,

        number TEXT NOT NULL UNIQUE,

        FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE ON UPDATE CASCADE

    );
INSERT INTO student_cards (id, student_id, number) VALUES (1, 1, 'PY-0001');
INSERT INTO student_cards (id, student_id, number) VALUES (2, 2, 'PY-0002');
INSERT INTO student_cards (id, student_id, number) VALUES (3, 3, 'PY-0003');
INSERT INTO student_cards (id, student_id, number) VALUES (4, 4, 'PY-0004');
INSERT INTO student_cards (id, student_id, number) VALUES (5, 5, 'PY-0005');
INSERT INTO student_cards (id, student_id, number) VALUES (6, 6, 'JS-0006');
INSERT INTO student_cards (id, student_id, number) VALUES (7, 7, 'JS-0007');
INSERT INTO student_cards (id, student_id, number) VALUES (8, 8, 'JS-0008');
INSERT INTO student_cards (id, student_id, number) VALUES (9, 9, 'JS-0009');
INSERT INTO student_cards (id, student_id, number) VALUES (10, 10, 'JS-0010');

-- Таблица: students
DROP TABLE IF EXISTS students;
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    age INTEGER,
    group_id INTEGER,
    -- Указание внешнего ключа
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE SET NULL ON UPDATE CASCADE
);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (1, 'Артём', 'Питонович', 'Серпентьев', 22, 1);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (2, 'Ольга', 'Джанговна', 'Фласкина', 19, 1);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (3, 'Виктор', 'Алгоритмович', 'Рекурсивный', 24, 1);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (4, 'Анна', 'Датафреймовна', 'Пандасова', 21, 1);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (5, 'Дмитрий', 'Генадьевич', 'Индентов', 20, 1);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (6, 'Светлана', 'Реактовна', 'Хуковская', 23, 2);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (7, 'Максим', 'Промисович', 'Аякcов', 20, 2);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (8, 'Ксения', 'Вьюевна', 'Компонентова', 19, 2);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (9, 'Игорь', 'Ноудович', 'Экспрессов', 25, 2);
INSERT INTO students (id, first_name, middle_name, last_name, age, group_id) VALUES (10, 'Алина', 'Домовна', 'Вёрсточкина', 22, 2);

-- Таблица: teachers
DROP TABLE IF EXISTS teachers;
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    age INTEGER,
    phone TEXT NOT NULL,
    email TEXT
);
INSERT INTO teachers (id, first_name, middle_name, last_name, age, phone, email) VALUES (1, 'Иван', 'Компиляторович', 'Кодмастеров', 45, '+7 (900) 123-45-67', 'codmaster@teachmail.ru');
INSERT INTO teachers (id, first_name, middle_name, last_name, age, phone, email) VALUES (2, 'Елена', 'Алгоритмовна', 'Сортирова', 38, '+7 (900) 234-56-78', 'sort_queen@teachmail.ru');
INSERT INTO teachers (id, first_name, middle_name, last_name, age, phone, email) VALUES (3, 'Николай', 'Фреймворкович', 'Библиотечный', 42, '+7 (900) 345-67-89', 'framework_guru@teachmail.ru');
INSERT INTO teachers (id, first_name, middle_name, last_name, age, phone, email) VALUES (4, 'Татьяна', 'Баговна', 'Дебаггер', 36, '+7 (900) 456-78-90', 'bug_hunter@teachmail.ru');
INSERT INTO teachers (id, first_name, middle_name, last_name, age, phone, email) VALUES (5, 'Михаил', 'Гитович', 'Коммитов', 41, '+7 (900) 567-89-01', 'never_merge_to_master@teachmail.ru');

-- Таблица: teachers_groups
DROP TABLE IF EXISTS teachers_groups;
CREATE TABLE IF NOT EXISTS teachers_groups (
    teacher_id INTEGER,
    group_id INTEGER,
    date_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)  ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id)  ON DELETE SET NULL ON UPDATE CASCADE,
    PRIMARY KEY (teacher_id, group_id) -- составной первичный ключ
);
INSERT INTO teachers_groups (teacher_id, group_id, date_start) VALUES (1, 1, '2025-04-12 09:14:07');
INSERT INTO teachers_groups (teacher_id, group_id, date_start) VALUES (2, 1, '2025-04-12 09:14:07');
INSERT INTO teachers_groups (teacher_id, group_id, date_start) VALUES (5, 1, '2025-04-12 09:14:07');
INSERT INTO teachers_groups (teacher_id, group_id, date_start) VALUES (3, 2, '2025-04-12 09:14:07');
INSERT INTO teachers_groups (teacher_id, group_id, date_start) VALUES (4, 2, '2025-04-12 09:14:07');
INSERT INTO teachers_groups (teacher_id, group_id, date_start) VALUES (5, 2, '2025-04-12 09:14:07');

-- Таблица: teachers_professions
DROP TABLE IF EXISTS teachers_professions;
CREATE TABLE IF NOT EXISTS teachers_professions (
    teacher_id INTEGER,
    profession_id INTEGER,
    notions TEXT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)  ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (profession_id) REFERENCES professions(id)  ON DELETE SET NULL ON UPDATE CASCADE,
    PRIMARY KEY (teacher_id, profession_id) -- составной первичный ключ
);
INSERT INTO teachers_professions (teacher_id, profession_id, notions) VALUES (1, 6, 'Эксперт по Python с опытом написания кода во сне');
INSERT INTO teachers_professions (teacher_id, profession_id, notions) VALUES (2, 6, 'Может объяснить рекурсию рекурсивно, а потом нерекурсивно');
INSERT INTO teachers_professions (teacher_id, profession_id, notions) VALUES (3, 5, 'JavaScript-гуру, по слухам однажды починил Internet Explorer');
INSERT INTO teachers_professions (teacher_id, profession_id, notions) VALUES (4, 5, 'CSS-волшебница, умеет центрировать div с первого раза');
INSERT INTO teachers_professions (teacher_id, profession_id, notions) VALUES (5, 4, 'Универсальный боец, может работать full-stack даже на калькуляторе');

-- Индекс: idx_groups_name
DROP INDEX IF EXISTS idx_groups_name;
CREATE INDEX IF NOT EXISTS idx_groups_name ON groups(group_name);

-- Индекс: idx_groups_profession
DROP INDEX IF EXISTS idx_groups_profession;
CREATE INDEX IF NOT EXISTS idx_groups_profession ON groups(profession_id);

-- Индекс: idx_students_fullname
DROP INDEX IF EXISTS idx_students_fullname;
CREATE INDEX IF NOT EXISTS idx_students_fullname ON students(first_name, middle_name, last_name);

-- Индекс: idx_students_group
DROP INDEX IF EXISTS idx_students_group;
CREATE INDEX IF NOT EXISTS idx_students_group ON students(group_id);

-- Индекс: idx_students_lastname
DROP INDEX IF EXISTS idx_students_lastname;
CREATE INDEX IF NOT EXISTS idx_students_lastname ON students(last_name);

-- Индекс: idx_teachers_email
DROP INDEX IF EXISTS idx_teachers_email;
CREATE INDEX IF NOT EXISTS idx_teachers_email ON teachers(email);

-- Индекс: idx_teachers_fullname
DROP INDEX IF EXISTS idx_teachers_fullname;
CREATE INDEX IF NOT EXISTS idx_teachers_fullname ON teachers(first_name, middle_name, last_name);

-- Индекс: idx_teachers_lastname
DROP INDEX IF EXISTS idx_teachers_lastname;
CREATE INDEX IF NOT EXISTS idx_teachers_lastname ON teachers(last_name);

-- Индекс: idx_teachers_phone
DROP INDEX IF EXISTS idx_teachers_phone;
CREATE INDEX IF NOT EXISTS idx_teachers_phone ON teachers(phone);

-- Представление: student_info
DROP VIEW IF EXISTS student_info;
CREATE VIEW IF NOT EXISTS student_info AS

SELECT

    s.first_name,

    s.middle_name,

    s.last_name,

    s.age,

    g.group_name,

    sc.number AS student_card_number



FROM

    students s

LEFT JOIN groups g ON s.group_id = g.id

LEFT JOIN student_cards sc ON s.id = sc.student_id;

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

"""

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


#################### ЗАПРОСЫ ####################

"""
READ
0. Попрбовать backref. Найти студента, и добыть его студенческий билет
1. Получить всех преподавателей и вывести их на экран
2. Взять первого преподавателя и посмотреть его группы
3. Взять первого преподавателя и посмотреть его профессии
4. Взять первого преподавателя и посмотреть его студентов + названия их групп

CREATE
1. Создать нового преподавателя
2. Назначить ему профессию
3. Назначить ему группу

UPDATE
1. Изменить профессию преподавателя
2. Изменить группу преподавателя
3. Изменить номер студенческого билета


DELETE
1. Удалить преподавателя
2. Проверим что происходит в связующих таблицах где выставлено ON DELETE SET NULL


Добавить индексы?

"""

# 0. Попрбовать backref. Найти студента, и добыть его студенческий билет
student_1 = Student.get(Student.id == 1)
print(student_1)
print(student_1.student_cards[0].number)  # Получаем номер студенческого билета через backref

# Проверка метода get_card
print("Проверка метода", student_1.get_card())  # Получаем номер студенческого билета через метод get_card


# TODO Получить группу ID 1 и через backref students получить всех её студентов
group_1 = Group.get(Group.id == 1)
print(group_1)

[print(student) for student in group_1.students]  # Получаем всех студентов группы 1 через backref students

# Как бы это выглядело БЕЗ backref
group_name = "python411"
students = Student.select().where(Student.group == group_name)
[print(student) for student in students]  # Получаем всех студентов группы 1 без backref



# 1. Получить всех преподавателей и вывести их на экран
all_teachers = Teacher.select()
print("Все преподаватели:")
[print(teacher) for teacher in all_teachers]  # Получаем всех преподавателей и выводим их на экран

# 2. Взять первого преподавателя и посмотреть его группы
teacher_1 = all_teachers[0]  # Берем первого преподавателя
print("Первый преподаватель:", teacher_1)

# Делаем выборку из связующей таблицы TeacherGroup, где teacher_id == teacher_1_id
# В результате получаем все группы в формате связки многие-ко-многим 1-1 1-2 1-3 где работает преподаватель 1
teacher_groups = TeacherGroup.select().where(TeacherGroup.teacher == teacher_1)  # Получаем группы первого преподавателя

# Идем по связке циклом, и обращаясь к group_id добываем название групп
print("Группы первого преподавателя:")
[print(record.group.group_name) for record in teacher_groups]  # Выводим группы первого преподавателя

# Так как описан __str__ мы можем просто вывести teacher_groups
[print(record) for record in teacher_groups]  # Выводим группы первого преподавателя с использованием __str__


# 3. Взять препода с ID 1  и посмотреть его профессии
teacher_1_professions = TeacherProfession.select().where(TeacherProfession.teacher == 1)  # Получаем профессии первого преподавателя
print("Профессии первого преподавателя:")

[print(record.profession.title) for record in teacher_1_professions]  # Выводим профессии первого преподавателя
[print(record) for record in teacher_1_professions]  # Выводим профессии первого преподавателя с использованием __str__


# 4. Взять первого преподавателя и посмотреть его студентов + названия их групп
teacher_1_students = Student.select().join(Group).join(TeacherGroup).where(TeacherGroup.teacher == teacher_1)  # Получаем студентов первого преподавателя

print("Студенты первого преподавателя:")
[print(student) for student in teacher_1_students]  # Выводим студентов первого преподавателя

# Протестируем метод get_all_students
print("Студенты первого преподавателя через метод get_all_students:")
all_students_of_teacher_1 = teacher_1.get_all_students()

[print(student) for student in all_students_of_teacher_1]  # Выводим студентов первого преподавателя через метод get_all_students


# 5. Создать нового преподавателя
# teacher_2 = Teacher.create(
#     first_name="Александр",
#     middle_name="Сергеевич",
#     last_name="Птушкин",
#     age=35,
#     phone="+7 (900) 111-22-33",
#     email="ptushka@mail.ru"
# )

# teacher_3 = Teacher(
#     first_name="Николай",
#     middle_name="Львович",
#     last_name="Тонкий",
#     age=35,
#     phone="+7 (900) 111-22-33",
#     email="tonko@mail.ru"
# )

# teacher_3.save()  # Сохраняем нового преподавателя в базе данных

# Получить всех преподов
# all_teachers = Teacher.select()
# [print(teacher) for teacher in all_teachers]  # Выводим всех преподавателей


# 6. Получим препода Птушкин и назначим ему профессию и группу
teacher_ptushkin = Teacher.get(Teacher.last_name == "Птушкин")  # Получаем преподавателя Птушкина
print(teacher_ptushkin)  # Выводим преподавателя Птушкина

# 7. Назначим ему профессию
# TeacherProfession.create(
#     teacher=teacher_ptushkin,
#     profession=Profession.get(Profession.title == "Backend-разработчик"),
#     notions="Может в Django и FastAPI, но ленивый и много пьет кофе на занятиях!"
# )  # Назначаем преподавателю Птушкину профессию Backend-разработчик

# 8. Назначим ему группу
# TeacherGroup.create(
#     teacher=teacher_ptushkin,
#     group=Group.get(Group.group_name == "python411"),
# )  # Назначаем преподавателю Птушкину группу python411

# Получим данные о Птушкине и выведем его группы и профессии
ptushkin_groups = TeacherGroup.select().where(TeacherGroup.teacher == teacher_ptushkin)  # Получаем группы преподавателя Птушкина
ptushkin_groups = TeacherGroup.select().where(TeacherGroup.teacher == teacher_ptushkin)  # Получаем группы преподавателя Птушкина

print("Группы преподавателя Птушкина:")
[print(record.group.group_name) for record in ptushkin_groups]  # Выводим группы преподавателя Птушкина
print("Профессии преподавателя Птушкина:")
[print(record) for record in ptushkin_groups]  # Выводим группы преподавателя Птушкина с использованием __str__

# Обновим фамилию Птушкина на Пушкин
teacher_ptushkin.last_name = "Пушкин"  # Изменяем фамилию преподавателя Птушкина на Пушкин
teacher_ptushkin.save()  # Сохраняем изменения в базе данных


# TODO МОЖНО ЛИ ЭТО СДЕЛАТЬ МАССОВО? И ДЕЙСТВИЯ ПРИ УДАЛЕНИИ - проверка SET NULL
# Студенты id 11 и 12 перевод в группу js412
students = Student.select().where(Student.id.in_([11, 12]))  # Получаем студентов с id 11 и 12

# Переводим студентов в группу js412
for student in students:
    student.group = Group.get(Group.group_name == "js412")  # Изменяем группу студента на js412
    student.save()  # Сохраняем изменения в базе данных


# Удаление преподавателя Тонкий
teacher_tonkiy = Teacher.get(Teacher.last_name == "Тонкий")  # Получаем преподавателя Тонкого
print(teacher_tonkiy)  # Выводим преподавателя Тонкого
teacher_tonkiy.delete_instance()  # Удаляем преподавателя Тонкого из базы данных
print("Преподаватель Тонкий удален")  # Выводим сообщение об удалении преподавателя Тонкого