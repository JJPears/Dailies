from server.models.helpers import UserValidator, HabitValidator

def test_user_validator_all_fields_present():
    user_data = {"name": "test", "email": "test@example.com", "password": "password"}
    assert UserValidator.validate(user_data) == (True, None)

def test_user_validator_fields_with_null_values():
    user_data = {"name": None, "email": "test@example.com", "password": "password"}
    assert UserValidator.validate(user_data) == (True, None)

def test_user_validator_missing_field():
    user_data = {"name": "test", "email": "test@example.com"}
    assert UserValidator.validate(user_data) == (False, "Missing mandatory field: password")

def test_habit_validator_all_fields_present():
    habit_data = {"name": "test habit"}
    assert HabitValidator.validate(habit_data) == (True, None)

def test_habit_validator_fields_with_null_values():
    user_data = {"name": None}
    assert HabitValidator.validate(user_data) == (True, None)

def test_habit_validator_missing_field():
    habit_data = {}
    assert HabitValidator.validate(habit_data) == (False, "Missing mandatory field: name")