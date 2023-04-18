from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, ObtainTokenView, UsersViewSet, UsersMeViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet)
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
