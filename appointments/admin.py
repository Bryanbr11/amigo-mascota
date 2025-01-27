from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'cliente', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'veterinario', 'cliente')
    search_fields = ('mascota__nombre', 'veterinario__username', 'cliente__username', 'motivo')
    date_hierarchy = 'fecha'