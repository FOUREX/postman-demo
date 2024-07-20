from datetime import datetime

from flask import Flask, jsonify, request, Response
from flask.json.provider import DefaultJSONProvider

from list_users import Context


app = Flask(__name__)
DefaultJSONProvider.sort_keys = False


@app.route("/", methods=["GET"])
def root():
    payload = {
        "message": "Quack! It works!",
        "routes": {
            "get_datetime": {
                "methods": ["GET"],
                "params": None
            },
            "get_users": {
                "methods": ["GET"],
                "params": None
            },
            "get_user": {
                "methods": ["GET"],
                "params": ["name"]
            },
            "add_user": {
                "methods": ["POST"],
                "params": ["name", "password"]
            }
        }
    }

    return Response(response=jsonify(payload).get_data(), status=200, mimetype="application/json")


@app.route("/get_datetime", methods=["GET"])
def get_datetime():
    """
    Повертає дату та час в момент відправлення запиту
    """

    time = datetime.now()

    payload = {
        "year": time.date().year,
        "month": time.date().month,
        "day": time.date().day,
        "hour": time.time().hour,
        "minute": time.time().minute,
        "second": time.time().second,
        "unix_timestamp": time.timestamp()
    }

    return Response(response=jsonify(payload).get_data(), status=200, mimetype="application/json")


@app.route("/get_users", methods=["GET"])
def get_users():
    """
    Повертає список всіх користувачів
    """

    users = Context.get_users()

    payload = {
        "users": users,
        "total": len(users)
    }

    return Response(response=jsonify(payload).get_data(), status=200, mimetype="application/json")


@app.route("/get_user", methods=["GET"])
def get_user():
    """
    Повертає інформацію про конкретного користувача

    Параметри:
        name - Ім'я користувача

    Статуси:
        200 (OK) - користувач знайдений
        404 (Not Found) - користувач не знайдений
    """

    name = request.args.get("name")

    if not name:
        return Response(response=jsonify({
            "message": "Missing parameters"
        }).get_data(), status=400, mimetype="application/json")

    user = Context.get_user(name)

    if not user:
        return Response(response=jsonify({
            "message": "User not found"
        }).get_data(), status=404, mimetype="application/json")

    payload = {
        "name": name,
        "display_name": user.get("display_name"),
        "status": user.get("status")
    }

    return Response(response=jsonify(payload).get_data(), status=200, mimetype="application/json")


@app.route("/add_user", methods=["POST"])
def add_user():
    """
    Додає нового користувача

    Параметри:
        name - ім'я користувача
        password - пароль

    Статуси:
        201 (Created) - успішно додано користувача
        400 (Bad Request) - пропущено параметри
        409 (Conflict) - введене ім'я вже використовується
    """

    name = request.args.get("name")
    password = request.args.get("password")

    if not name or not password:
        return Response(response=jsonify({
            "message": "Missing parameters"
        }).get_data(), status=400, mimetype="application/json")

    if not Context.add_user(name, password):
        return Response(response=jsonify({
            "message": "This name is already in use"
        }).get_data(), status=409, mimetype="application/json")

    payload = {
        "message": "User successfully added"
    }

    return Response(response=jsonify(payload).get_data(), status=201, mimetype="application/json")


if __name__ == '__main__':
    app.run()
