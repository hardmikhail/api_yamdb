from rest_framework import mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter

from .serializers import (UserSignUpSerializer,
                          ObtainTokenSerializer,
                          UsersSerializer)
from review.models import User
from .permissions import IsAdmin, IsUser
from .authentication import get_tokens_for_user


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        if username == 'me':
            raise ValidationError({'username': 'Имя me запрещено!'})
        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            raise ValidationError({'message': 'Данные уже используются!'})
        confirmation_code = default_token_generator.make_token(user=user)
        send_mail(
            subject=username,
            message=confirmation_code,
            from_email='webmaster@localhost',
            recipient_list=[email],
            fail_silently=False,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username',]


class UsersMeViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ObtainTokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = User.objects.filter(username=username).first()
        if not User.objects.filter(username=username).exists():
            return Response(
                {'message': 'Invalid username'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        jwt_token = get_tokens_for_user(user)

        return Response(jwt_token)
