from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def is_teacher(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return wrapper


def is_student(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return wrapper


def is_admin(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return wrapper
