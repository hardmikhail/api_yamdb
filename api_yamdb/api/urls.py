from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import TokenView
# from .views import SignUpViewSet, TokenViewSet

# router = DefaultRouter()
# router.register('auth/signup/', SignUpViewSet)
# router.register('auth/token/', TokenViewSet)

urlpatterns = [
    path('auth/token/', TokenView.as_view({'post': 'create'}), name='token_obtain_pair'),
    # path('auth/signup/', )
]
