from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('complete/student/<int:task_id>/',
         views.complete_by_student, name='complete_by_student'),
]
