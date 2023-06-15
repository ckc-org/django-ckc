from rest_framework.exceptions import ValidationError


class SnackbarException(ValidationError):
    def __init__(self, message):
        super().__init__({'snackbar_message': message})
