from django.contrib import admin
from .models import Cars, EntryPermits


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'owner', 'model', 'color')
    list_filter = ('model', 'color')
    search_fields = ('license_plate', 'owner__username', 'owner__email')
    ordering = ('license_plate',)


@admin.register(EntryPermits)
class EntryPermitsAdmin(admin.ModelAdmin):
    list_display = ('car', 'entry_count', 'expiration', 'notes')
    list_filter = ('expiration',)
    search_fields = ('car__license_plate', 'notes')
    ordering = ('-expiration',)
