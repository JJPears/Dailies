"""
This module is a controller for the user model and its associated habits.
It handles the requests for creating, updating, and getting users and habits.
"""
from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest
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
        print("Testting")
        raise NotFound("User not found")
    return jsonify(user.to_json()), 200

@user_controller.route("/user", methods=["POST"])
def create_user():
    """
    Create a new user.

    :return: A JSON object of the created user and a 201 HTTP status code if the user
             is created successfully, else an error message and a 400 HTTP status code.
    """
    user_data = request.get_json()
    if not user_data:
        raise BadRequest("No user data provided")

    user = User.create(user_data)
    db.session.commit()

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
        raise BadRequest("No user data provided")
    user = User.query.get(user_id)
    if user is None:
        raise NotFound("User not found")
    user.update(user_data)

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
        raise BadRequest("No habit data provided")
    
    habit = Habit.create(habit_data, user_id)

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
        raise BadRequest("No habit data provided")
    user = User.query.get(user_id)
    if user is None:
        raise NotFound("User not found")
    habit = Habit.query.get(habit_id)
    if habit is None:
        raise NotFound("Habit not found")
    
    habit.update(habit_data)

    return jsonify(habit.to_json()), 201
