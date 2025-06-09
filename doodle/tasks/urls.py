from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'tasks'

urlpatterns = [
    path('', login_required(views.index), name='task_list'), 
    path('create/', login_required(views.task_create), name='task_create'),
    path('task_calendar/', login_required(views.task_calendar), name='task_calendar'),
    path('edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('toggle-complete/<int:task_id>/', views.toggle_complete, name='toggle_complete'),
]