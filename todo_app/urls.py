"""
URL configuration for the todo_app application.

This module defines all URL patterns for the todo_app, mapping each URL
to its corresponding view. It uses Django's path() function for routing
and includes parameter capturing for detail views.
"""
from django.urls import path
from . import views

# Application namespace for reverse URL lookups
# Used in templates and views with 'todo_app:url_name' syntax
app_name = 'todo_app'

# URL patterns list - each path maps a URL pattern to a view
urlpatterns = [
    # Homepage / Task list
    # Displays all tasks for the current user with filtering options
    # URL: /todo/
    path('',
         views.TaskListView.as_view(),
         name='task_list'),

    # Task detail view
    # Shows complete information about a single task
    # URL: /todo/<task_id>/
    # Example: /todo/5/ - shows task with ID 5
    path('<int:pk>/',
         views.TaskDetailView.as_view(),
         name='task_detail'),

    # Create new task
    # Displays form for creating a new task (GET)
    # Processes form submission and creates task (POST)
    # URL: /todo/create_task/
    path('create_task/',
         views.TaskCreateView.as_view(),
         name='new_task'),

    # Update existing task
    # Displays form with pre-filled task data (GET)
    # Processes form submission and updates task (POST)
    # URL: /todo/<task_id>/edit/
    # Example: /todo/5/edit/ - edit task with ID 5
    path('<int:pk>/edit/',
         views.TaskUpdateView.as_view(),
         name='update_task'),

    # Mark task as completed
    # Processes POST request to mark task as done
    # No template - redirects back to task detail
    # URL: /todo/<task_id>/complete/
    # Example: /todo/5/complete/ - complete task with ID 5
    path('<int:pk>/complete/',
         views.TaskCompleteView.as_view(),
         name='complete_task'),

    # Delete task
    # Shows confirmation modal on detail page (GET)
    # Processes actual deletion (POST)
    # URL: /todo/<task_id>/delete/
    # Example: /todo/5/delete/ - delete task with ID 5
    path('<int:pk>/delete/',
         views.TaskDeleteView.as_view(),
         name='delete_task'),
]