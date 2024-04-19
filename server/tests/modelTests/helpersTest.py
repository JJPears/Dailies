import unittest
from server.models.helpers import UserValidator, HabitValidator

class TestUserValidator(unittest.TestCase):
    def test_all_fields_present(self):
        user_data = {"name": "test", "email": "test@example.com", "password": "password"}
        self.assertEqual(UserValidator.validate(user_data), (True, None))

    def test_fields_with_null_values(self):
        user_data = {"name": None, "email": "test@example.com", "password": "password"}
        self.assertEqual(UserValidator.validate(user_data), (True, None))

    def test_missing_field(self):
        user_data = {"name": "test", "email": "test@example.com"}
        self.assertEqual(UserValidator.validate(user_data), (False, "Missing mandatory field: password"))


class TestHabitValidator(unittest.TestCase):
    def test_all_fields_present(self):
        habit_data = {"name": "test habit"}
        self.assertEqual(HabitValidator.validate(habit_data), (True, None))

    def test_fields_with_null_values(self):
        user_data = {"name": None}
        self.assertEqual(HabitValidator.validate(user_data), (True, None))

    def test_missing_field(self):
        habit_data = {}
        self.assertEqual(HabitValidator.validate(habit_data), (False, "Missing mandatory field: name"))


if __name__ == '__main__':
    unittest.main()