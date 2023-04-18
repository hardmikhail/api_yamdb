from rest_framework import serializers

from review.models import User, ROLE_CHOICES


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

    class Meta:
        fields = ('email', 'username')
        # fields = ('__all__')
        model = User


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    # role = serializers.ChoiceField(choices=)
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
