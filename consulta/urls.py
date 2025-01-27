from django.urls import path
from . import views

app_name = 'consulta'

urlpatterns = [
    path('', views.lista_consultas, name='lista_consultas'),
    path('crear/', views.crear_consulta, name='crear_consulta'),
    path('<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('<int:consulta_id>/editar/', views.editar_consulta, name='editar_consulta'),
    path('<int:consulta_id>/finalizar/', views.finalizar_consulta, name='finalizar_consulta'),
    path('<int:consulta_id>/cancelar/', views.cancelar_consulta, name='cancelar_consulta'),
    path('mascota/<int:mascota_id>/consultas/', views.consultas_mascota, name='consultas_mascota'),
    path('diagnostico/<int:consulta_id>/', views.diagnostico_detalle, name='diagnostico_detalle'),
    path('historial/<int:mascota_id>/', views.historial_medico, name='historial_medico'),
    path('descargar-diagnostico/<int:consulta_id>/', views.descargar_diagnostico_pdf, name='descargar_diagnostico_pdf'),
    path('historial/', views.historial_consultas, name='historial'),
    path('crear/<int:cita_id>/', views.crear_consulta_desde_cita, name='crear'),
]
