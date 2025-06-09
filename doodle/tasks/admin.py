from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'difficulty', 'completed', 'due_date')
    list_filter = ('completed', 'difficulty')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'due_date'
# Register your models here.
