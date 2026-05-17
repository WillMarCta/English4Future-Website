from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import is_teacher


@login_required
def courses(request):
    return render(request, 'courses.html')


@is_teacher
def create_course(request):
    return render(request, 'courses.html')
