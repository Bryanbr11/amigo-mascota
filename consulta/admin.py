from django.contrib import admin
from .models import Consulta, HistorialConsulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'veterinario', 'fecha', 'estado', 'tipo_servicio']
    list_filter = ['estado', 'tipo_servicio', 'fecha']
    search_fields = ['mascota__nombre', 'veterinario__username', 'motivo']
    readonly_fields = ['creado_en', 'actualizado_en']
    fieldsets = (
        ('Información Básica', {
            'fields': ('mascota', 'veterinario', 'tipo_servicio', 'estado')
        }),
        ('Detalles de la Consulta', {
            'fields': ('motivo', 'sintomas', 'signos_clinicos', 'peso', 'diagnostico', 'diagnostico_ia', 'tratamiento')
        }),
        ('Información Adicional', {
            'fields': ('notas_adicionales', 'costo', 'creado_en', 'actualizado_en')
        }),
    )

@admin.register(HistorialConsulta)
class HistorialConsultaAdmin(admin.ModelAdmin):
    list_display = ['consulta', 'fecha_modificacion', 'estado_anterior']
    list_filter = ['fecha_modificacion', 'estado_anterior']
    search_fields = ['consulta__mascota__nombre']
    readonly_fields = ['fecha_modificacion']