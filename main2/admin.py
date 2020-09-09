from django.contrib import admin
from .models import Track, Task, Rate



@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('author', 'id_task', 'duration', 'date', 'id_rate')
    list_filter = ('author', 'date')
    fieldsets = (
        (None, {
            'fields': ('date', 'id_task', 'duration', 'id_rate')
        }),
        ('Author', {
            'fields': ('author',)
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('author', 'name')


# Registrations
admin.site.register(Rate)

