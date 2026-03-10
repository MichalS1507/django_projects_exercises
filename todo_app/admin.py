"""
Admin interface configuration for the todo_app application.

This module registers models with the Django admin site and customizes
the admin interface for efficient data management.
"""
from django.contrib import admin
from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Category model.

    Provides a clean and efficient interface for managing task categories
    with basic CRUD operations and search functionality.

    Features:
    - List view showing category names and colors
    - Filtering by category name
    - Search functionality for quick category lookup
    """

    # Display fields in the list view as columns
    list_display = ['name', 'color']

    # Add filter sidebar on the right for easy filtering
    list_filter = ['name']

    # Enable search box at the top
    search_fields = ['name']

    # Default ordering for categories
    ordering = ['name']

    # Make color field editable directly in list view (optional)
    # list_editable = ['color']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Task model.

    Provides a comprehensive management interface for tasks with
    advanced filtering, searching, and bulk operations.

    Features:
    - Complete overview of all tasks with key information
    - Inline editing of completion status
    - Advanced filtering by status, priority, and category
    - Full-text search in titles and descriptions
    - Bulk actions for marking multiple tasks as completed/incomplete
    - Custom display of overdue status
    """

    # Fields displayed as columns in the task list
    # Each column shows a different aspect of the task
    list_display = [
        'title',  # Task title with link to edit
        'category',  # Associated category (if any)
        'get_priority_display',  # Human-readable priority (High/Medium/Low)
        'due_date',  # Deadline (formatted date)
        'completed',  # Completion status as checkbox
        'is_overdue',  # Custom property showing overdue status
    ]

    # Clickable fields that link to edit view
    list_display_links = ['title']

    # Filter sidebar options on the right
    # Allows quick filtering by these fields
    list_filter = [
        'completed',  # Filter by completion status
        'priority',  # Filter by priority level
        'category',  # Filter by category
        'created_date',  # Filter by creation date (with date hierarchy)
    ]

    # Enable search in these fields
    # Searches across all specified fields
    search_fields = [
        'title',  # Search in task titles
        'description',  # Search in task descriptions
        'category__name',  # Search by category name (foreign key lookup)
    ]

    # Allow inline editing of completed status directly in list view
    # Saves time by avoiding the edit form for simple status changes
    list_editable = ['completed']

    # Number of items per page in list view
    list_per_page = 20

    # Default ordering for tasks in admin
    ordering = ['-created_date', 'priority']

    # Date hierarchy navigation (shows drill-down by date)
    date_hierarchy = 'created_date'

    # Custom admin actions for bulk operations
    actions = ['mark_completed', 'mark_incomplete']

    # Fieldsets for add/edit form organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user'),
            'description': 'Core task details and ownership'
        }),
        ('Status & Priority', {
            'fields': ('completed', 'priority'),
            'description': 'Task progress and importance level'
        }),
        ('Dates', {
            'fields': ('created_date', 'due_date'),
            'description': 'Timeline and deadlines'
        }),
        ('Categorization', {
            'fields': ('category',),
            'description': 'Task classification',
            'classes': ('collapse',),  # Collapsible section
        }),
    )

    # Make created_date read-only in edit form
    readonly_fields = ['created_date']

    # Optimize queryset for list display (select related to reduce DB queries)
    def get_queryset(self, request):
        """
        Optimize task list queryset by prefetching related data.

        This reduces the number of database queries when displaying
        related fields like category names.

        Args:
            request: HTTP request object

        Returns:
            QuerySet: Optimized task queryset
        """
        queryset = super().get_queryset(request)
        # Select related foreign keys to avoid N+1 queries
        return queryset.select_related('category', 'user')

    def mark_completed(self, request, queryset):
        """
        Bulk action to mark selected tasks as completed.

        Updates all selected tasks' completion status to True
        in a single database query for efficiency.

        Args:
            request: HTTP request object
            queryset: Selected tasks queryset
        """
        updated = queryset.update(completed=True)
        self.message_user(
            request,
            f'{updated} task(s) successfully marked as completed.'
        )

    mark_completed.short_description = "Mark selected tasks as completed"

    def mark_incomplete(self, request, queryset):
        """
        Bulk action to mark selected tasks as incomplete.

        Updates all selected tasks' completion status to False
        in a single database query for efficiency.

        Args:
            request: HTTP request object
            queryset: Selected tasks queryset
        """
        updated = queryset.update(completed=False)
        self.message_user(
            request,
            f'{updated} task(s) successfully marked as incomplete.'
        )

    mark_incomplete.short_description = "Mark selected tasks as incomplete"

    # Custom method to display colored priority in list view
    def colored_priority(self, obj):
        """
        Display priority with appropriate color coding.

        Args:
            obj: Task instance

        Returns:
            str: HTML span with colored priority text
        """
        color_map = {
            1: '#dc3545',  # High - red
            2: '#ffc107',  # Medium - yellow
            3: '#28a745',  # Low - green
        }
        color = color_map.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )

    colored_priority.short_description = 'Priority'
    colored_priority.admin_order_field = 'priority'

    # Save model-related imports at the top
    from django.utils.html import format_html