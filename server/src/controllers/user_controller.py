"""
This module is a controller for the user model and its associated habits.
It handles the requests for creating, updating, and getting users and habits.
"""

from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, Blueprint
from server.src.models.models import User, Habit
from server.src.database import db

user_controller = Blueprint("user_controller", __name__)


@user_controller.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a user by ID.

    :param user_id: The ID of the user to retrieve.
    :return: A JSON object of the user and a 200 HTTP status code if the user is found,
             else 404.
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_json()), 200


# TODO add some validation here, currently it's possible to pass null values
# for fields and will throw an integrity exception in DB
# Need some kind of validation before we get to data layer
@user_controller.route("/user", methods=["POST"])
def create_user():
    """
    Create a new user.

    :return: A JSON object of the created user and a 201 HTTP status code if the user
             is created successfully, else an error message and a 400 HTTP status code.
    """
    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No data provided for creating user"}), 400
    try:
        user = User.create(user_data)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (IntegrityError, DataError) as e:
        return jsonify({"error": "Data integrity error: " + str(e)}), 400
    return jsonify(user.to_json()), 201


@user_controller.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user by ID.

    :param user_id: The ID of the user to update.
    :return: A JSON object of the updated user and a 201 HTTP status code if the user is
             updated successfully, else an error message and a 400 HTTP status code.
    """
    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No data provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    try:
        user.update(user_data)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (IntegrityError, DataError) as e:
        return jsonify({"error": "Data integrity error: " + str(e)}), 400

    return jsonify(user.to_json()), 201


@user_controller.route("/user/<int:user_id>/habit", methods=["POST"])
def create_habit(user_id):
    """
    Create a new habit for a user.

    :param user_id: The ID of the user to create the habit for.
    :return: A JSON object of the created habit and a 201 HTTP status code if the habit is
             created successfully, else an error message and a 400 HTTP status code.
    """
    habit_data = request.get_json()
    if not habit_data:
        return jsonify({"error": "No data provided for creating habit"}), 400
    try:
        habit = Habit.create(habit_data, user_id)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (IntegrityError, DataError) as e:
        return jsonify({"error": "Data integrity error: " + str(e)}), 400
    return jsonify(habit.to_json()), 201


@user_controller.route("/user/<int:user_id>/habit/<int:habit_id>", methods=["PUT"])
def update_habit(user_id, habit_id):
    """
    Update a habit for a user.

    :param user_id: The ID of the user who owns the habit.
    :param habit_id: The ID of the habit to update.
    :return: A JSON object of the updated habit and a 201 HTTP status code if the
             habit is updated successfully, else an error message and a 400 HTTP status code.
    """
    habit_data = request.get_json()
    if not habit_data:
        return jsonify({"error": "No data provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    habit = Habit.query.get(habit_id)
    if habit is None:
        return jsonify({"error": "Habit not found"}), 404

    try:
        habit.update(habit_data)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (IntegrityError, DataError) as e:
        return jsonify({"error": "Data integrity error: " + str(e)}), 400

    return jsonify(habit.to_json()), 201
