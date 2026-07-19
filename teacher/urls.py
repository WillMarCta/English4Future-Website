from django.urls import path
from . import views

urlpatterns = [
    path('my-students/', views.my_students, name='my_students'),
    path('add-student/<int:student_id>/', views.add_student_to_my_students_list, name='add_student'),
    path('remove-student/<int:student_id>/', views.remove_student_from_my_students_list, name='remove_student'),
]
