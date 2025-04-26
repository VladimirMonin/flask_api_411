"""
Модуль маршрутов API для аутентификации
=====================================

Этот модуль содержит маршруты API для аутентификации пользователей:
- POST /api/auth/login: вход в систему и получение токена
- POST /api/auth/register: регистрация нового пользователя
"""

from apiflask import APIBlueprint, Schema, abort
from apiflask.fields import String, Boolean, Integer
from api.auth import generate_token, authenticate_user, register_user
import config

# Создаем Blueprint для маршрутов аутентификации
auth_bp = APIBlueprint("auth", __name__, url_prefix="/api/auth")

# Определяем схемы данных для API


class LoginSchema(Schema):
    """Схема для аутентификации пользователя"""

    username = String(required=True)
    password = String(required=True)

    class Meta:
        # Описания полей
        field_descriptions = {"username": "Имя пользователя", "password": "Пароль"}


class TokenSchema(Schema):
    """Схема для ответа с токеном"""

    access_token = String()
    token_type = String()
    expires_in = Integer()


class RegisterSchema(Schema):
    """Схема для регистрации пользователя"""

    username = String(required=True)
    password = String(required=True)
    is_admin = Boolean()  # Удалили default

    class Meta:
        # Описания полей
        field_descriptions = {
            "username": "Имя пользователя",
            "password": "Пароль",
            "is_admin": "Является ли пользователь администратором",
        }
        # Значения по умолчанию теперь тут
        load_default = {"is_admin": False}


class MessageSchema(Schema):
    """Схема для сообщений об успехе/ошибке"""

    success = Boolean()
    message = String()


# Маршрут для входа в систему и получения токена
@auth_bp.post("/login")
@auth_bp.doc(
    summary="Вход в систему",
    description="Аутентифицирует пользователя и возвращает JWT токен",
)
@auth_bp.input(LoginSchema)
@auth_bp.output(TokenSchema)
def login(data):
    """
    Аутентифицирует пользователя и возвращает JWT токен.

    Args:
        data (dict): Данные входа (имя пользователя и пароль)

    Returns:
        dict: JWT токен и его параметры
    """
    username = data["username"]
    password = data["password"]

    # Проверяем учетные данные пользователя
    if not authenticate_user(username, password):
        abort(401, "Неверное имя пользователя или пароль")

    # Генерируем токен
    token = generate_token(username)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": config.JWT_EXPIRATION,
    }


# Маршрут для регистрации нового пользователя
@auth_bp.post("/register")
@auth_bp.doc(
    summary="Регистрация пользователя",
    description="Регистрирует нового пользователя в системе",
)
@auth_bp.input(RegisterSchema)
@auth_bp.output(MessageSchema)
def register(data):
    """
    Регистрирует нового пользователя.

    Args:
        data (dict): Данные для регистрации пользователя

    Returns:
        dict: Сообщение об успешной регистрации
    """
    username = data["username"]
    password = data["password"]
    is_admin = data.get("is_admin", False)

    # Регистрируем нового пользователя
    if not register_user(username, password, is_admin):
        abort(400, "Пользователь с таким именем уже существует")

    return {"success": True, "message": "Пользователь успешно зарегистрирован"}
