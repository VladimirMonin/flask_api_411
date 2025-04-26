"""
Модуль аутентификации API
========================

Этот модуль обеспечивает JWT-аутентификацию для API. Он предоставляет функции для:
- Создания JWT-токенов
- Проверки JWT-токенов
- Хэширования и проверки паролей
- Декораторы для защиты маршрутов
"""

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, g, jsonify
from passlib.hash import pbkdf2_sha256
import config

# Фиктивная база данных пользователей для примера
# В реальном проекте нужно использовать базу данных с моделью Users
users_db = {
    "admin": {
        "username": "admin",
        "password": pbkdf2_sha256.hash("password"),
        "is_admin": True,
    }
}


def generate_token(username):
    """
    Создает JWT токен для указанного пользователя.

    Args:
        username (str): Имя пользователя

    Returns:
        str: Сгенерированный JWT токен
    """
    expiration = datetime.utcnow() + timedelta(seconds=config.JWT_EXPIRATION)
    payload = {
        "sub": username,
        "exp": expiration,
        "is_admin": users_db.get(username, {}).get("is_admin", False),
    }
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm="HS256")


def verify_token(token):
    """
    Проверяет валидность JWT токена.

    Args:
        token (str): JWT токен для проверки

    Returns:
        dict or None: Данные пользователя при успешной верификации, иначе None
    """
    try:
        # Декодируем токен и проверяем его валидность
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
        username = payload["sub"]

        if username not in users_db:
            return None

        # Сохраняем данные пользователя
        user_data = {"username": username, "is_admin": payload.get("is_admin", False)}

        return user_data
    except jwt.ExpiredSignatureError:
        # Токен истек
        return None
    except (jwt.InvalidTokenError, KeyError):
        # Токен недействителен или не содержит нужных полей
        return None


def token_required(f):
    """
    Декоратор для защиты маршрутов, требующих аутентификацию по токену.

    Args:
        f: Защищаемая функция маршрута

    Returns:
        function: Обернутая функция маршрута с проверкой аутентификации
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Проверяем наличие токена в заголовке Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return (
                jsonify({"error": "Отсутствует токен! Требуется аутентификация."}),
                401,
            )

        # Проверяем токен
        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Недействительный или истекший токен!"}), 401

        # Сохраняем данные пользователя для использования в маршруте
        g.current_user = user_data

        return f(*args, **kwargs)

    return decorated_function


def register_user(username, password, is_admin=False):
    """
    Регистрирует нового пользователя.

    Args:
        username (str): Имя пользователя
        password (str): Пароль пользователя
        is_admin (bool): Флаг администратора

    Returns:
        bool: True если регистрация успешна, иначе False
    """
    if username in users_db:
        return False

    # Хешируем пароль и создаем пользователя
    hashed_password = pbkdf2_sha256.hash(password)
    users_db[username] = {
        "username": username,
        "password": hashed_password,
        "is_admin": is_admin,
    }

    return True


def authenticate_user(username, password):
    """
    Аутентифицирует пользователя по имени и паролю.

    Args:
        username (str): Имя пользователя
        password (str): Пароль пользователя

    Returns:
        bool: True если аутентификация успешна, иначе False
    """
    user = users_db.get(username)
    if not user:
        return False

    # Проверяем пароль
    return pbkdf2_sha256.verify(password, user["password"])
