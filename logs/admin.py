from django.contrib import admin
from .models import LoginLog, LogoutLog


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('car', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('car__license_plate', 'car__owner__username', 'car__owner__email')
    ordering = ('-created_at',)


@admin.register(LogoutLog)
class LogoutLogAdmin(admin.ModelAdmin):
    list_display = ('car', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('car__license_plate', 'car__owner__username', 'car__owner__email')
    ordering = ('-created_at',)
