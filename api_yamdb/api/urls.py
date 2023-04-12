from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUpViewSet, ObtainTokenView

# router = DefaultRouter()
# router.register('auth/signup/', SignUpViewSet)
# router.register('auth/token/', TokenViewSet)

urlpatterns = [
    path('auth/signup/', SignUpViewSet.as_view({'post': 'create'}), name='auth_signup'),
    path('auth/token/', ObtainTokenView.as_view())
]
