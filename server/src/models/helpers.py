"""
Module for helper classes and functions.
"""


class DataValidator:
    """
    Class for validating data.
    """

    # TODO don't need multiple methods for these, just pass in mandatory fields
    # and data then check data has all mandatory fields
    @staticmethod
    def validate_user_data(user_data):
        """
        Validates the user data.

        Args:
            user_data (dict): The user data to be validated.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the validation passed or
                    not, and an error message if validation failed, error message contains a list
                    of all missing mandatory fields.
        """
        mandatory_fields = ["name", "email", "password"]
        missing_fields = []

        for field in mandatory_fields:
            if field not in user_data:
                missing_fields.append(field)

        if len(missing_fields) > 0:
            return False, f"Missing mandatory fields: {', '.join(missing_fields)}"
        return True, None

    @staticmethod
    def validate_habit_data(habit_data):
        """
        Validates the habit data.

        Args:
            habit_data (dict): The habit data to be validated.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the validation passed or
                    not, and an error message with missing mandatory fields.
        """
        mandatory_fields = ["name"]
        missing_fields = []

        for field in mandatory_fields:
            if field not in habit_data:
                missing_fields.append(field)

        if len(missing_fields) > 0:
            return False, f"Missing mandatory fields: {', '.join(missing_fields)}"
        return True, None
