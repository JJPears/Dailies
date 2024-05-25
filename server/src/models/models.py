"""
Module containing database entities for user and habit, alongside logic for operations
such as updating and creating.
"""

from server.src.database import db
from ..models.helpers import DataValidator


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        habits (list): The list of habits associated with the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    habits = db.relationship("habit", backref="user", lazy=True)

    def update(self, user_data):
        """
        Updates the user with the given data.

        Args:
            user_data (dict): The data to update the user with.

        Raises:
            ValueError: If the user data is not valid.

        Returns:
            None
        """
        valid, error = DataValidator.validate_user_data(user_data)
        if not valid:
            raise ValueError(error)
        for field in user_data:
            if field == "id":
                continue
            setattr(self, field, user_data[field])

    @staticmethod
    def create(user_data):
        """
        Creates a new user with the given data, including creating habits where applicable.

        Args:
            user_data (dict): The data to create the user with.

        Raises:
            ValueError: If the user data is not valid.

        Returns:
            User: The created user object.
        """
        habits = []
        if "habits" in user_data:
            habits_data = user_data.pop("habits")
            for habit_data in habits_data:
                valid, error = DataValidator.validate_habit_data(habit_data)
                if not valid:
                    raise ValueError(error)
                habit = Habit(name=habit_data["name"])
                habits.append(habit)

        user = User(**user_data, habits=habits)

        db.session.add(user)
        return user


class Habit(db.Model):
    """
    Represents a habit in the system.

    Attributes:
        id (int): The unique identifier of the habit.
        name (str): The name of the habit.
        user_id (int): The ID of the user associated with the habit.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def update(self, habit_data):
        """
        Updates the habit with the given data.

        Args:
            habit_data (dict): The data to update the habit with.

        Raises:
            ValueError: If the habit data is not valid.

        Returns:
            None
        """
        valid, error = DataValidator.validate_habit_data(habit_data)
        if not valid:
            raise ValueError(error)
        for field in habit_data:
            if field in ("id", "user_id"):
                continue
            setattr(self, field, habit_data[field])

    @staticmethod
    def create(habit_data, user_id):
        """
        Creates a new habit with the given data and associates it with a user.

        Args:
            habit_data (dict): The data to create the habit with.
            user_id (int): The ID of the user to associate the habit with.

        Raises:
            ValueError: If the user is not found or the habit data is not valid.

        Returns:
            Habit: The created habit object.
        """
        user = User.query.get(user_id)

        if user is None:
            raise ValueError("User not found")
        valid, error = DataValidator.validate_habit_data(habit_data)
        if not valid:
            raise ValueError(error)
        habit = Habit(name=habit_data["name"], user_id=user_id)
        db.session.add(habit)
        return habit
