from venv import create
from flask import Blueprint, request, Response
# Создаем блюпринт для студентов с префиксом /api/students

teachers_bp = Blueprint("teachers", __name__, url_prefix="/api/teachers")
