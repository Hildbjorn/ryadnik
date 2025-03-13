from django.contrib import admin
from .models import Task, Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'tags')
    search_fields = ('title', 'description')

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)