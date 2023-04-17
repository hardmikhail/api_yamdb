from rest_framework import serializers
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator

from review.models import User
from .validators import CorrectUsernameValidator


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, validators=[UniqueValidator(queryset=User.objects.all())])
    # username = serializers.CharField(validators=[CorrectUsernameValidator()])
    class Meta:
        fields = ('email', 'username')
        model = User

    # def get_validate

    def to_representation(self, instance):
        confirmation_code = default_token_generator.make_token(user=instance)
        send_mail(
            instance.username,
            confirmation_code,
            'webmaster@localhost',
            [instance.email],
            fail_silently=False,
        )
        return super().to_representation(instance)
    

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
