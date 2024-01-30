class UserValidator:
    @staticmethod
    def validate(data):
        mandatory_fields = ['name', 'email', 'password']
        for field in mandatory_fields:
            if field not in data:
                return False, f'Missing mandatory field: {field}'
        return True, None