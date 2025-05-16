from flask import Flask, jsonify
from students_routes import students_bp
from teachers_routes import teachers_bp

# Создали экземпляр приложения Flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Для корректного отображения кириллицы

# Зарегистрировали блюпринты
app.register_blueprint(students_bp)
app.register_blueprint(teachers_bp)

# Создали маршрут для корневого URL
@app.route("/")
def index():
    return jsonify({"message": "Добро пожаловать в API управления студентами!"})

if __name__ == '__main__':
    app.run(debug=True)