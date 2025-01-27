from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('', views.lista_mascotas, name='lista'),
    path('crear/', views.crear_mascota, name='crear'),
    path('<int:mascota_id>/', views.detalle_mascota, name='detalle'),
    path('<int:mascota_id>/editar/', views.editar_mascota, name='editar'),
    path('<int:mascota_id>/eliminar/', views.eliminar_mascota, name='eliminar'),
]