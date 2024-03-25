from rest_framework import routers

from calendar_app.api import EventViewSet, UsuarioViewSet, TokenViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'usuarios', UsuarioViewSet, basename='usurarios')
router.register(r'revalidar', TokenViewSet, basename='token')

urlpatterns = router.urls

# urlpatterns += [
#     path('login/', LoginView.as_view(), name='login'),
#     # Otras URLs de tu aplicación
# ]
