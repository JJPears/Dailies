from flask import request, jsonify
from app import app
from models import User, Habit
from database import db
from ..models.helpers import UserValidator, HabitValidator


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_json()), 200


# TODO add some validation here, currently it's possible to pass null values for fields and will throw an integrity exception in DB
# Need some kind of validation before we get to data layer
@app.route("/user", methods=["POST"])
def create_user():
    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No data provided for creating user"}), 400
    try:
        user = User.create(user_data)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(user.to_json()), 201


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No data provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    user.update(user_data)

    db.session.commit()

    return jsonify(user.to_json()), 201


# TODO data validation needed, same as with create_user
@app.route("/user/<int:user_id>/habit", methods=["POST"])
def create_habit(user_id):
    habit_data = request.get_json()
    if not habit_data:
        return jsonify({"error": "No data provided for creating habit"}), 400
    try:
        habit = Habit.create(habit_data, user_id)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(habit.to_json()), 201


@app.route("/user/<int:user_id>/habit/<int:habit_id>", methods=["PUT"])
def update_habit(user_id, habit_id):
    habit_data = request.get_json()
    if not habit_data:
        return jsonify({"error": "No data provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    habit = Habit.query.get(habit_id)
    if habit is None:
        return jsonify({"error": "Habit not found"}), 404

    habit.update(habit_data)

    db.session.commit()

    return jsonify(habit.to_json()), 201
