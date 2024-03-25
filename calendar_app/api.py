from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework_simplejwt.views import TokenRefreshView

from calendar_app.models import Event, User
from calendar_app.serializer import EventSerializer, UsuarioSerializer, UsuarioListSerializer, PasswordSerializer, \
    UpdateUserSerializer


class UsuarioViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UsuarioSerializer
    list_serializer_class = UsuarioListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(is_active=True).filter(is_active=True).values('id', 'username',
                                                                                                    'email', 'password')
        return self.queryset

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            })
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            serialized_user = self.serializer_class(user).data
            return Response({
                'ok': True,
                'message': 'Usuario registrado correctamente.',
                'data': serialized_user
            }, status=status.HTTP_201_CREATED)
        return Response({
            'ok': False,
            'message': 'Hay errores en el registro',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la actualización',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_instance = get_object_or_404(self.model, id=pk)
        user_instance.delete()
        return Response({
            'message': 'Usuario eliminado correctamente'
        })

    @action(detail=True, methods=['get'])
    def desactivar(self, request, pk=None):
        user_instance = self.get_object(pk)
        user_instance.is_active = False
        user_instance.save()
        serializer = self.get_serializer(user_instance)
        return Response({
            'message': 'Usuario desactivado correctamente',
            'usuario': serializer.data
        }, status=status.HTTP_200_OK)


# class LoginView(APIView):
#     @staticmethod
#     def post(request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         print(request.data)
#
#         user = authenticate(request, email=email, password=password)
#
#         print("Resultado de authenticate:", user)
#
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'ok': True,
#                              'token': token.key,
#                              'name': user.username,
#                              'uid': user.id
#                              })
#         else:
#             return Response({'ok': False, 'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"message": "No tiene permiso para eliminar este evento."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenViewSet(ViewSetMixin, TokenRefreshView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def revalidate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user_data = {
            'username': user.username,
            'email': user.email,
            # Agregar otros campos que necesites
        }
        return Response({'tokens': serializer.validated_data, 'user': user_data})

# class TokenViewSet(ViewSetMixin, TokenRefreshView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = request.user
#         user_data = {
#             'username': user.username,
#             'email': user.email,
#             # Agregar otros campos que necesites
#         }
#         response = super().post(request, *args, **kwargs)
#         response.data['user'] = user_data
#         return response
