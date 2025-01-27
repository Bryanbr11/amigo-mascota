from django.contrib import admin
from .models import Recordatorio

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'hora', 'completado', 'creado_por')
    list_filter = ('completado', 'fecha', 'creado_por')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha'
