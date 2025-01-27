from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'timestamp', 'ip_address')
    list_filter = ('action_type', 'timestamp', 'user')
    search_fields = ('user__username', 'details', 'ip_address')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
