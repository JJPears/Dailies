from datetime import datetime
from database import db
from ..models.helpers import HabitValidator, UserValidator


# Main user model, each user linked to a list of dailies they can achieve
# Maybe I want them to be able to link to long term goals?
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # last_login = db.Column(db.DateTime)
    habits = db.relationship("habit", backref="user", lazy=True)

    def update(self, user_data):
        valid, error = UserValidator.validate(user_data)
        if not valid:
            raise ValueError(error)
        for field in user_data:
            if field == "id":
                continue
            setattr(self, field, user_data[field])

    @staticmethod
    def create(user_data):
        habits = []
        if "habits" in user_data:
            habits_data = user_data.pop("habits")
            for habit_data in habits_data:
                valid, error = HabitValidator.validate(habit_data)
                if not valid:
                    raise ValueError(error)
                habit = Habit(name=habit_data["name"])
                habits.append(habit)

        user = User(**user_data, habits=habits)

        db.session.add(user)
        return user


# TODO email validation/verification
# TODO password hashing


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def update(self, habit_data):
        valid, error = HabitValidator.validate(habit_data)
        if not valid:
            raise ValueError(error)
        for field in habit_data:
            if field == "id" or field == "user_id":
                continue
            setattr(self, field, habit_data[field])

    @staticmethod
    def create(habit_data, user_id):
        user = User.query.get(user_id)

        if user is None:
            raise ValueError("User not found")
        valid, error = HabitValidator.validate(habit_data)
        if not valid:
            raise ValueError(error)
        habit = Habit(name=habit_data["name"], user_id=user_id)
        db.session.add(habit)
        return habit
