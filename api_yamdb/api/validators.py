from rest_framework.validators import ValidationError


class CorrectUsernameValidator:
    message = 'dfa'
    code = 'surrogate_characters_not_allowed'

    def __call__(self, value):
        if value.username == 'me':
            raise ValidationError(self.message)
