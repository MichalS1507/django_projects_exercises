from django.contrib import admin
from .models import Category,Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'get_priority_display',
        'due_date',
        'completed',
        'is_overdue'
    ]
    list_filter = ['completed', 'priority', 'category']
    search_fields = ['title', 'description']
    list_editable = ['completed']
    list_per_page = 20

    actions = ['mark_completed', 'mark_incomplete']

    def mark_completed(self, request, queryset):
        queryset.update(completed=True)
    mark_completed.short_description = "Mark selected tasks as completed"

    def mark_incomplete(self, request, queryset):
        queryset.update(completed=False)
    mark_incomplete.short_description = "Mark selected tasks as incomplete"


