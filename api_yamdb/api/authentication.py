from rest_framework_simplejwt.tokens import AccessToken


def get_tokens_for_user(user):
    access_token = AccessToken.for_user(user)
    return {
        'access': str(access_token)
    }
