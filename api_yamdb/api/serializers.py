from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.views import TokenObtainPairView

from .tokens import account_activation_token


confirmation_code=account_activation_token.make_token(User)


class UserSignUpSerializer(serializers.ModelSerializer, PasswordResetTokenGenerator):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    # username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('email', 'username')
        # fields = ('__all__')
        model = User

    def to_internal_value(self, data):
        send_mail(
        'Subject here',
        confirmation_code,
        'webmaster@localhost',
        [data.get('email')],
        fail_silently=False,
        )
        return super().to_internal_value(data)


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()