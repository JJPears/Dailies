"""
Module for helper classes and functions.
"""


class DataValidator:
    """
    Class for validating data.
    """

    @staticmethod
    def validate_user_data(user_data):
        """
        Validates the user data.

        Args:
            user_data (dict): The user data to be validated.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the validation passed or
                    not, and an error message if validation failed.
        """
        mandatory_fields = ["name", "email", "password"]

        for field in mandatory_fields:
            if field not in user_data:
                return False, f"Missing mandatory field: {field}"
        return True, None

    @staticmethod
    def validate_habit_data(habit_data):
        """
        Validates the habit data.

        Args:
            habit_data (dict): The habit data to be validated.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the validation passed or
                    not, and an error message if validation failed.
        """
        mandatory_fields = ["name"]

        for field in mandatory_fields:
            if field not in habit_data:
                return False, f"Missing mandatory field: {field}"
        return True, None
