from rest_framework.exceptions import ValidationError


class SnackbarError(ValidationError):
    def __init__(self, message):
        super().__init__({'snackbar_message': message})
