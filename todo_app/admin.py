from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Category model.
    """
    # Fields to display in the list view
    list_display = ['name', 'color']
    # Add filter sidebar by name
    list_filter = ['name']
    # Add search functionality for name field
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Task model.
    Provides comprehensive task management in admin panel.
    """
    # Fields to display in the list view
    list_display = [
        'title',
        'category',
        'get_priority_display', # Shows human-readable priority (High/Medium/Low)
        'due_date',
        'completed',
        'is_overdue'    # Custom property from model
    ]

    # Filter sidebar options
    list_filter = ['completed', 'priority', 'category']
    # Enable search in these fields
    search_fields = ['title', 'description']
    # Allow inline editing of completed status
    list_editable = ['completed']
    # Pagination: 20 items per page
    list_per_page = 20

    # Custom admin actions
    actions = ['mark_completed', 'mark_incomplete']

    def mark_completed(self, request, queryset):
        """
        Admin action to mark selected tasks as completed.
        Updates all tasks in the queryset at once.
        """
        queryset.update(completed=True)
    mark_completed.short_description = "Mark selected tasks as completed"

    def mark_incomplete(self, request, queryset):
        """
        Admin action to mark selected tasks as incomplete.
        Updates all tasks in the queryset at once.
        """
        queryset.update(completed=False)
    mark_incomplete.short_description = "Mark selected tasks as incomplete"