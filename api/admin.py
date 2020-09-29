from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):

    list_display = ('pk', 'author', 'title', 'description', 'start_date',
                    'status', 'finish_date')
    search_fields = ('title',)
    list_filter = ('start_date',)
    empty_value_display = '-пусто-'


admin.site.register(Task, TaskAdmin)
