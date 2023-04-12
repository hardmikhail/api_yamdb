from rest_framework import mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.mixins import CreateModelMixin

from .serializers import UserSignUpSerializer, ObtainTokenSerializer
from .models import User
from .authentication import JWTAuthentication
from .serializers import confirmation_code


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer


# class TokenView(TokenObtainPairView):
#     serializer_class = TokenSerializer
#     # pass

class ObtainTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirm_code = serializer.validated_data.get('confirmation_code')

        user = User.objects.filter(username=username).first()

        # if user is None or not user.check_password(email):
        if user is None or confirm_code != confirmation_code:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token})


    