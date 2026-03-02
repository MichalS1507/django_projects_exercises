from django.urls import path
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
]