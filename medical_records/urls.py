from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    path('crear/', views.crear_ficha_medica, name='crear_ficha'),
    path('', views.lista_fichas_medicas, name='lista_fichas'),
    path('<int:ficha_id>/', views.detalle_ficha_medica, name='detalle_ficha'),
]