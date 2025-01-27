from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin'),
    path('veterinario/', views.veterinario_dashboard, name='veterinario'),
    path('secretaria/', views.secretaria_dashboard, name='secretaria'),
    path('cliente/', views.cliente_dashboard, name='cliente'),
    path('admin/usuarios/', views.listar_usuarios, name='admin_usuarios'),
    path('admin/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('admin/usuarios/permisos/', views.gestionar_permisos, name='gestionar_permisos'),
    path('admin/usuarios/actividad/', views.registros_actividad, name='registros_actividad'),
    path('admin/reportes/ingresos/', views.reporte_ingresos, name='reporte_ingresos'),
    path('admin/reportes/servicios/', views.estadisticas_servicios, name='estadisticas_servicios'),
    path('admin/reportes/satisfaccion/', views.satisfaccion_clientes, name='satisfaccion_clientes'),
    path('admin/config/general/', views.configuracion_general, name='configuracion_general'),
    path('admin/config/servicios/', views.gestionar_servicios, name='gestionar_servicios'),
    path('admin/config/respaldo/', views.respaldo_datos, name='respaldo_datos'),
    path('admin/usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/usuarios/toggle-estado/<int:user_id>/', views.toggle_estado_usuario, name='toggle_estado_usuario'),
] 