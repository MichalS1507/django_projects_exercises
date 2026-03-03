from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
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