from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import is_student
from .models import Task

# Create your views here.


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {"tasks": tasks})


def complete_by_student(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed_by_student = True
    task.save()
    return redirect('task_list')
