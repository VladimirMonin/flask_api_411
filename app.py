from flask import Flask, jsonify, request

# 1. Создали экземпляр приложения Flask
app = Flask(__name__)

# 2. Описали маршрут для главной страницы
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Hello from Flask!")

# 3. Get запрос с параметрами name и age
# http://127.0.0.1:5000/greet?name=Vladimir&age=26
@app.route('/greet/', methods=['GET'])
def greet_user():
    name = request.args.get('name', 'Гость')
    age = request.args.get('age', 'неизвестен')
    
    return jsonify(message=f"Hello, {name}! Your age is {age}.")


if __name__ == '__main__':
    app.run(debug=True)