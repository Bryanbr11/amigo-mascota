from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultaViewSet, HistorialConsultaViewSet

router = DefaultRouter()
router.register(r'consultas', ConsultaViewSet)
router.register(r'historial', HistorialConsultaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]