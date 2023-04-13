from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator 
from django.shortcuts import get_object_or_404

from .tokens import token


# confirmation_code=account_activation_token.make_token(User)
# token = account_activation_token.make_token(User)



class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])


    class Meta:
        fields = ('email', 'username')
        model = User

    def to_representation(self, instance):
        token = default_token_generator.make_token(user=instance)
        send_mail(
            'Subject here',
            token,
            'webmaster@localhost',
            [instance.email],
            fail_silently=False,
        )
        return super().to_representation(instance)
    

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
