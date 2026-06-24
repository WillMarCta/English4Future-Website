from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=130)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_by_student = models.BooleanField(default=False)
    completed_by_teacher = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)

    # estudiante
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    # profesor
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks")

    # curso
    course = models.ForeignKey(
        'courses.Course', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
