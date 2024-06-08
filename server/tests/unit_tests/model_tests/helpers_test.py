#pylint: skip-file
from server.src.models.helpers import DataValidator

def test_user_validator_all_fields_present():
    user_data = {"name": "test", "email": "test@example.com", "password": "password"}
    assert DataValidator.validate_user_data(user_data) == (True, None)

def test_user_validator_fields_with_null_values():
    user_data = {"name": None, "email": "test@example.com", "password": "password"}
    assert DataValidator.validate_user_data(user_data) == (True, None)

def test_user_validator_missing_field():
    user_data = {"name": "test"}
    assert DataValidator.validate_user_data(user_data) == (False, "Missing mandatory fields: email, password")

def test_habit_validator_all_fields_present():
    habit_data = {"name": "test habit"}
    assert DataValidator.validate_habit_data(habit_data) == (True, None)

def test_habit_validator_fields_with_null_values():
    user_data = {"name": None}
    assert DataValidator.validate_habit_data(user_data) == (True, None)

def test_habit_validator_missing_field():
    habit_data = {}
    assert DataValidator.validate_habit_data(habit_data) == (False, "Missing mandatory fields: name")