import unittest
from server.models.helpers import UserValidator, HabitValidator

class TestValidators(unittest.TestCase):
    def test_user_validator(self):
        # Test with all fields present
        user_data = {"name": "test", "email": "test@example.com", "password": "password"}
        self.assertEqual(UserValidator.validate(user_data), (True, None))

        # Test with missing field
        user_data = {"name": "test", "email": "test@example.com"}
        self.assertEqual(UserValidator.validate(user_data), (False, "Missing mandatory field: password"))

    def test_habit_validator(self):
        # Test with all fields present
        habit_data = {"name": "test habit"}
        self.assertEqual(HabitValidator.validate(habit_data), (True, None))

        # Test with missing field
        habit_data = {}
        self.assertEqual(HabitValidator.validate(habit_data), (False, "Missing mandatory field: name"))

if __name__ == '__main__':
    unittest.main()