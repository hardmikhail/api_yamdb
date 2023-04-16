from rest_framework import mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets

from .serializers import UserSignUpSerializer, ObtainTokenSerializer, UsersSerializer
from .models import User
from .permissions import IsAdmin
from .authentication import get_tokens_for_user


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = (IsAdmin,) #админ
    serializer_class = UsersSerializer
    lookup_field = 'username'


class UsersMeViewSet(APIView):
    # queryset = User.objects.all() 
    # permission_classes = (,)
    serializer_class = UsersSerializer
    # lookup_field = 'username'
    def get(self, request, *args, **kwargs):
        return Response(request.data)



class ObtainTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = User.objects.filter(username=username).first()
        if not User.objects.filter(username=username).exists():
            return Response({'message': 'Invalid username'}, status=status.HTTP_404_NOT_FOUND)
        if user is None or not default_token_generator.check_token(user, confirmation_code):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        jwt_token = get_tokens_for_user(user)

        return Response(jwt_token)


    