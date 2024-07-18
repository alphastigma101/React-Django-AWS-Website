class Validation:
    @staticmethod
    def validate_2d_array(value) -> bool:
        try:
            # Ensure that the main value is a list
            if not isinstance(value, list):
                return False
            for i in value:
                # Ensure each element in the main list is also a list
                if not isinstance(i, list):
                    return False
            return True
        except Exception as e:
            return False

    @staticmethod
    def is_dictionary(data:dict) -> bool:
        if (isinstance(data, dict)):
            return True
        return False


