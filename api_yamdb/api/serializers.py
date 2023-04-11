from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('email', 'username')
        # fields = ('__all__')
        model = User
    
    def validate(self, attrs):
        return attrs

    def to_internal_value(self, data):
        # token = PasswordResetTokenGenerator
        send_mail(
        'Subject here',
        # token.make_token(self, user=User),
        '',
        'webmaster@localhost',
        [data.get('email')],
        fail_silently=False,
        )
        return super().to_internal_value(data)