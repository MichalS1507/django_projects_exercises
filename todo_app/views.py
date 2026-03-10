"""
Views for the todo_app application.

This module contains all view classes that handle HTTP requests and return responses.
Each view is protected by LoginRequiredMixin to ensure only authenticated users can access them.
"""
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    """
    Display a paginated list of tasks for the authenticated user.

    Features:
    - Shows only tasks belonging to the current user
    - Supports filtering by completion status (all/completed/incomplete)
    - Orders tasks: incomplete first, then by priority, then by due date
    - Paginates results (20 items per page)
    """
    template_name = "todo_app/task_index.html"
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        """
        Return filtered and ordered queryset of tasks for the current user.

        The queryset is filtered by:
        - User ownership (only tasks belonging to request.user)
        - Optional status filter from URL parameter 'filter'

        Returns:
            QuerySet: Filtered and ordered Task objects
        """
        # Base queryset - only tasks belonging to current user
        queryset = Task.objects.filter(user=self.request.user)

        # Apply status filter from URL parameter
        filter_status = self.request.GET.get('filter', 'all')

        if filter_status == 'completed':
            queryset = queryset.filter(completed=True)
        elif filter_status == 'incomplete':
            queryset = queryset.filter(completed=False)
        # 'all' returns unfiltered queryset

        # Return ordered queryset
        return queryset.order_by('completed', 'priority', 'due_date')

    def get_context_data(self, **kwargs):
        """
        Add current filter value to template context.

        This allows the template to highlight the active filter link.

        Returns:
            dict: Context data with added 'current_filter' key
        """
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Display detailed information about a specific task.

    Features:
    - Shows all task fields (title, description, dates, priority, etc.)
    - Ensures user can only view their own tasks
    - Automatically returns 404 if task doesn't exist or belongs to another user
    """
    model = Task
    template_name = "todo_app/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        """
        Restrict detail view to tasks belonging to current user.

        Returns:
            QuerySet: Tasks filtered by user ownership
        """
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Handle creation of new tasks.

    Features:
    - Displays form for task creation (GET)
    - Processes form submission and saves new task (POST)
    - Automatically assigns current user as task owner
    - Redirects to task list on success
    """
    model = Task
    form_class = TaskForm
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy('todo_app:task_list')

    def form_valid(self, form):
        """
        Set the task owner to current user before saving.

        This method is called when the submitted form is valid.
        It assigns the current authenticated user to the task instance,
        then proceeds with normal form validation and saving.

        Args:
            form: Valid TaskForm instance

        Returns:
            HttpResponse: Redirect to success_url after successful save
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Handle editing of existing tasks.

    Features:
    - Displays pre-filled form with existing task data (GET)
    - Processes form submission and updates task (POST)
    - Ensures user can only edit their own tasks
    - Redirects to task list on success
    """
    model = Task
    form_class = TaskForm
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy('todo_app:task_list')

    def get_queryset(self):
        """
        Restrict update view to tasks belonging to current user.

        Returns:
            QuerySet: Tasks filtered by user ownership
        """
        return Task.objects.filter(user=self.request.user)


class TaskCompleteView(LoginRequiredMixin, View):
    """
    Handle quick task completion without a separate template.

    This view processes POST requests to mark a task as completed.
    It uses the model's mark_completed() method and redirects back
    to the task detail page.

    Note: Uses POST method only for safety (GET should not modify data).
    """

    def post(self, request, pk):
        """
        Mark a specific task as completed.

        Args:
            request: HTTP request object
            pk: Primary key of the task to complete

        Returns:
            HttpResponse: Redirect to task detail page

        Raises:
            404: If task doesn't exist or belongs to another user
        """
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.mark_completed()
        return redirect('todo_app:task_detail', pk=pk)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Handle task deletion with confirmation.

    Features:
    - Shows confirmation modal on the task detail page (GET)
    - Processes actual deletion (POST)
    - Ensures user can only delete their own tasks
    - Redirects to task list on successful deletion
    """
    model = Task
    template_name = "todo_app/task_detail.html"
    success_url = reverse_lazy('todo_app:task_list')

    def get_context_data(self, **kwargs):
        """
        Add delete_mode flag to template context.

        This flag triggers the display of a confirmation modal
        on the task detail page.

        Returns:
            dict: Context data with added 'delete_mode' key set to True
        """
        context = super().get_context_data(**kwargs)
        context['delete_mode'] = True
        return context

    def get_queryset(self):
        """
        Restrict delete view to tasks belonging to current user.

        Returns:
            QuerySet: Tasks filtered by user ownership
        """
        return Task.objects.filter(user=self.request.user)