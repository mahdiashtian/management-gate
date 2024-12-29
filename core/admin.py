from django.contrib import admin
from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'file_type', 'created_at', 'archived_at')
    list_filter = ('file_type', 'created_at', 'archived_at')
    search_fields = ('file',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        """Customize queryset to exclude archived items by default."""
        queryset = super().get_queryset(request)
        return queryset.filter(archived_at__isnull=True)

    def archive_media(self, request, queryset):
        """Custom action to archive selected media files."""
        queryset.update(archived_at=timezone.now())
        self.message_user(request, "Selected media files have been archived.")

    actions = ['archive_media']
