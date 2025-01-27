from django.contrib import admin
from .models import Especie, Mascota

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'edad', 'peso', 'propietario')
    list_filter = ('especie', 'raza')
    search_fields = ('nombre', 'raza', 'propietario__username')
    readonly_fields = ('edad',)