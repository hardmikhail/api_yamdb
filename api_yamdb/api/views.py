from rest_framework import mixins, permissions, status, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from reviews.models import Categories, Genre, Title, Review
from user.models import User
from .authentication import get_tokens_for_user
from .filters import TitleFilter
from .permissions import (IsAdminModeratorAuthorOrReadOnly,
                          IsAdminOrReadOnly,
                          AdminOnly)
from .serializers import (UserSignUpSerializer,
                          ObtainTokenSerializer,
                          UsersSerializer,
                          UsersMeSerializer,
                          CategoriesSerializer,
                          GenreSerializer,
                          TitleGETSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentsSerializer
                          )


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
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
    queryset = User.objects.get_queryset()
    permission_classes = (AdminOnly,)
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)


class UsersMeViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UsersMeSerializer(user, data=request.data, partial=True)
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
        user = User.objects.filter(username=username)
        if not user.exists():
            return Response(
                {'message': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'message': 'Неверные данные!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        jwt_token = get_tokens_for_user(user)

        return Response(jwt_token)


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.action in ('list', 'retrieve'):
            return TitleGETSerializer
        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        Review.objects.filter(title=title)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()
