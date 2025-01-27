from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'appointments'

# Comenta o elimina estas líneas si no estás usando viewsets
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', views.lista_citas, name='lista_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('<int:cita_id>/', views.detalle_cita, name='detalle_cita'),
    path('<int:cita_id>/editar/', views.editar_cita, name='editar_cita'),
    path('<int:cita_id>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
    path('<int:cita_id>/estado/', views.actualizar_estado_cita, name='actualizar_estado_cita'),
    # Comenta o elimina esta línea si no estás usando viewsets
    # path('api/', include(router.urls)),
]