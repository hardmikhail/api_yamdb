from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.mixins import CreateModelMixin

from .serializers import UserSignUpSerializer
from .models import User


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass

class TokenView(TokenObtainPairView, mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    