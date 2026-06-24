from django.test import TestCase
from django.contrib.auth.models import User

from .models import Task


class TaskDeletionTests(TestCase):
    def test_task_survives_when_owner_user_is_deleted(self):
        user = User.objects.create_user(username='student1', password='testpass123')
        task = Task.objects.create(
            title='Tarea de prueba',
            user=user,
            created_by=user,
        )

        user.delete()

        task.refresh_from_db()

        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        self.assertIsNone(task.user)
        self.assertIsNone(task.created_by)
