# Create your views here.
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from calendar_app.models import User
from calendar_app.serializer import CustomTokenObtainPairSerializer, CustomUserSerializer


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(
            email=email,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            # print(login_serializer)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'ok': True,
                    'token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def custom_token_refresh(request):
#     response = TokenRefreshView.as_view()(request)
#     user = request.user
#     user_data = {
#         'username': user.username,
#         'email': user.email,
#         # Agregar otros campos que necesites
#     }
#     response.data['user'] = user_data
#     return response
