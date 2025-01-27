from django.contrib import admin
from .models import Cita, Consulta, Recordatorio

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('mascota__nombre', 'veterinario__username')
    date_hierarchy = 'fecha'

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'fecha', 'diagnostico')
    list_filter = ('fecha',)
    search_fields = ('mascota__nombre', 'veterinario__username', 'diagnostico')
    date_hierarchy = 'fecha'

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'hora', 'completado', 'creado_por')
    list_filter = ('completado', 'fecha')
    search_fields = ('titulo', 'descripcion', 'creado_por__username')
    date_hierarchy = 'fecha'