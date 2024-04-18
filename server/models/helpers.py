class UserValidator:
    @staticmethod
    def validate(user_data):
        # this allows for null values but field is mandatory
        mandatory_fields = ["name", "email", "password"]
        
        for field in mandatory_fields:
            if field not in user_data:
                return False, f"Missing mandatory field: {field}"
        return True, None


class HabitValidator:
    @staticmethod
    def validate(habit_data):
        # this allows for null values but field is mandatory
        mandatory_fields = ["name"]

        for field in mandatory_fields:
            if field not in habit_data:
                return False, f"Missing mandatory field: {field}"
        return True, None
