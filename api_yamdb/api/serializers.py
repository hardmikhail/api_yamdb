from rest_framework import serializers
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator

from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('email', 'username')
        model = User

    def to_representation(self, instance):
        confirmation_code = default_token_generator.make_token(user=instance)
        send_mail(
            'Subject here',
            confirmation_code,
            'webmaster@localhost',
            [instance.email],
            fail_silently=False,
        )
        return super().to_representation(instance)
    

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
