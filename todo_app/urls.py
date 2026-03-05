from django.urls import path
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('create_task/', views.TaskCreateView.as_view(), name='new_task'),
    path('<int:pk>:edit/', views.TaskUpdateView.as_view(), name='update_task'),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name='complete_task'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
]