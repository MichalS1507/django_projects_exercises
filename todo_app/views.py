from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm
from .models import Task

# Create your views here.
class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = "todo_app/task_index.html"
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        filter_status = self.request.GET.get('filter', 'all')

        if filter_status == 'completed':
            queryset = queryset.filter(completed=True)
        elif filter_status == 'incomplete':
            queryset = queryset.filter(completed=False)

        return queryset.order_by('completed', 'priority', 'due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "todo_app/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy('todo_app:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy('todo_app:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.mark_completed()
        return redirect('todo_app:task_detail', pk=pk)

class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "todo_app/task_detail.html"
    success_url = reverse_lazy('todo_app:task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_mode'] = True
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)