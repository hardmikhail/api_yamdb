from django.urls import path

from .views import SignUpViewSet, ObtainTokenView


urlpatterns = [
    path('auth/signup/', SignUpViewSet.as_view({'post': 'create'}), name='auth_signup'),
    path('auth/token/', ObtainTokenView.as_view())
]
