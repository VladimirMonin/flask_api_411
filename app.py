"""
API для управления учетными записями студентов
===============================================

Этот модуль предоставляет RESTful API для работы с данными студентов.
Все маршруты начинаются с префикса `/api/`.

Доступные маршруты
-----------------

* Аутентификация
    * POST /api/auth/login - Вход в систему и получение JWT токена
    * POST /api/auth/register - Регистрация нового пользователя

* Студенты
    * GET /api/student/{id} - Получение данных конкретного студента по его идентификатору
    * POST /api/students/create - Создание записи о новом студенте

Документация API доступна по адресу /api/docs
"""

from apiflask import APIFlask
from flask import Response, json, g
from models import Student, Group, db
import config

# Импортируем маршруты
from api.routes.students import students_bp
from api.routes.auth import auth_bp

# Создаем экземпляр приложения APIFlask
app = APIFlask(
    __name__,
    title=config.APP_NAME,
    version=config.APP_VERSION,
    spec_path=config.API_SPEC_PATH,
    docs_path=config.API_DOCS_PATH,
)

# Настраиваем приложение
app.config["JSON_AS_ASCII"] = False

# Регистрируем blueprints для модульности
app.register_blueprint(students_bp)
app.register_blueprint(auth_bp)


# Подключение к БД перед каждым запросом
@app.before_request
def connect_db():
    """
    Подключаемся к базе данных перед обработкой запроса.
    """
    db.connect(reuse_if_open=True)


# Закрытие соединения с базой данных после обработки запроса
@app.teardown_appcontext
def close_db(exception):
    """
    Закрывает соединение с базой данных после обработки запроса.
    """
    if not db.is_closed():
        db.close()


if __name__ == "__main__":
    # Создаем таблицы перед запуском приложения
    db.connect(reuse_if_open=True)
    db.create_tables([Student, Group], safe=True)
    db.close()

    # Запускаем приложение
    app.run(debug=config.DEBUG)
