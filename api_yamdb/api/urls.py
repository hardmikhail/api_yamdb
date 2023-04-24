from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SignUpViewSet,
    ObtainTokenView,
    UsersViewSet,
    UsersMeViewSet,
    CategoriesViewSet,
    GenreViewSet,
    TitleViewSet)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
urlpatterns = [
    path(
        'auth/signup/',
        SignUpViewSet.as_view({'post': 'create'}),
        name='auth_signup'
    ),
    path('auth/token/', ObtainTokenView.as_view()),
    path('users/me/', UsersMeViewSet.as_view()),
    path('', include(router.urls)),
    # path('users/<username>/',UsersViewSet.as_view({'get': 'retrieve'}))
]

