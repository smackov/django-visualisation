from django.contrib import admin

from .models import Track, Task, Rate, Quote


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    "Registration the Track model"
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
    "Registration the Task model"
    list_display = ('author', 'name')


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    "Registration the Quote model"
    list_display = ('author', 'text')


# Registration the Rate model
admin.site.register(Rate)
