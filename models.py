import peewee as pw


db = pw.SqliteDatabase("students_new.db")


class Profession(pw.Model):
    title = pw.CharField(unique=True)
    description = pw.TextField(null=True)

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "professions"  # Указываем имя таблицы в базе данных


class Group(pw.Model):
    group_name = pw.CharField(unique=True)
    start_date = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    end_date = pw.DateTimeField(null=True)
    profession = pw.ForeignKeyField(Profession, backref="groups", null=True)

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "groups"  # Указываем имя таблицы в базе данных


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


class StudentCard(pw.Model):
    student = pw.ForeignKeyField(Student, backref="student_cards", unique=True)
    number = pw.CharField(unique=True)

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "student_cards"  # Указываем имя таблицы в базе данных


class Teacher(pw.Model):
    first_name = pw.CharField(max_length=50)
    middle_name = pw.CharField(null=True, max_length=50)
    last_name = pw.CharField(max_length=50)
    age = pw.IntegerField(null=True)
    phone = pw.CharField(max_length=15)
    email = pw.CharField(null=True, max_length=50)

    def get_all_students(self):
        return (
            Student.select()
            .join(Group)
            .join(TeacherGroup)
            .where(TeacherGroup.teacher == self)
        )

    def __str__(self):
        return (
            f"Имя: {self.first_name}, Фамилия: {self.last_name}, Телефон: {self.phone}"
        )

    class Meta:
        database = db  # Указываем базу данных для этой модели
        table_name = "teachers"  # Указываем имя таблицы в базе данных


class TeacherGroup(pw.Model):
    teacher = pw.ForeignKeyField(Teacher, on_delete="SET NULL", on_update="CASCADE")
    group = pw.ForeignKeyField(Group, on_delete="SET NULL", on_update="CASCADE")
    date_start = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])

    def __str__(self):
        return f"Преподаватель {self.teacher.last_name} ведет группу {self.group.group_name} с {self.date_start}"

    class Meta:
        database = db  # База данных
        table_name = "teachers_groups"  # Имя таблицы
        primary_key = pw.CompositeKey("teacher", "group")  # Составной первичный ключ


class TeacherProfession(pw.Model):
    teacher = pw.ForeignKeyField(Teacher, on_delete="SET NULL", on_update="CASCADE")
    profession = pw.ForeignKeyField(
        Profession, on_delete="SET NULL", on_update="CASCADE"
    )
    notions = pw.TextField(null=True)  # Заметки о квалификации преподавателя

    def __str__(self):
        return f"Преподаватель {self.teacher.last_name} специализируется на {self.profession.title}"

    class Meta:
        database = db
        table_name = "teachers_professions"
        primary_key = pw.CompositeKey(
            "teacher", "profession"
        )  # Составной первичный ключ
