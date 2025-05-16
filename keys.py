# Модуль для хранения ключей API наших пользователей
USERS = [
    {
        "username": "admin",
        "api_key": r"asfd234U*(&*#@$@#$sf---)",
        "role": "admin"
    },
    {
        "username": "user1",
        "api_key": r"aasdfJLs13&^^%%^ads!!fs",
        "role": "user"
    },
]

# Мы можем пойти по 2 путям. 1. Декораторы проверки прав и ключей. 2. Просто функции возвращающие True/False

# Пойдем по простому пути - функции!

def is_valid_api_key(api_key):
    """
    Проверяет, является ли переданный ключ действительным.`
    :param api_key: Ключ API для проверки
    :return: True, если ключ действителен, иначе False
    """
    return any(user["api_key"] == api_key for user in USERS)


def is_admin(api_key):
    """
    Проверяет, является ли пользователь администратором.
    :param api_key: Ключ API для проверки
    :return: True, если пользователь администратор, иначе False
    """
    return any(user["api_key"] == api_key and user["role"] == "admin" for user in USERS)
