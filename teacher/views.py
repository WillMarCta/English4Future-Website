from django.shortcuts import render, redirect
# to create the form for the user to sign up
from django.contrib.auth.forms import UserCreationForm
# to create the user in the database when they sign up
from django.contrib.auth.models import User
# to create the cookie for the user when they sign up
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseForbidden
from users.models import Profile

# Create your views here.


# --- : Lista Global ---
@login_required
def all_students(request):
    return User.objects.filter(
        is_staff=False, 
        is_superuser=False,
        profile__role='student'
    )

# --- assign students to a teacher ---
@login_required
def add_student_to_my_students_list(request, student_id):
    student_profile = Profile.objects.get(user_id=student_id)
    student_profile.teacher = request.user
    student_profile.save()
    return redirect('my_students')



# --- FUNCIÓN 2: Vista Principal ---
@login_required
def my_students(request):
    if request.method == 'POST' and 'student_id' in request.POST:
        student_id = request.POST.get('student_id')
        if student_id:
            student_profile = Profile.objects.get(user_id=student_id)
            student_profile.teacher = request.user 
            student_profile.save()
            print("Usuario actual:", request.user)
            print("Estudiantes encontrados:", Profile.objects.filter(teacher=request.user).count())
        return redirect('my_students')


    user_role = request.user.profile.role.lower()  # Convertimos a minúsculas para evitar problemas de mayúsculas/minúsculas

    # 1. Si es profesor (sea 'Teacher', 'teacher' o 'TEACHER')
    if user_role == 'teacher':
        students = Profile.objects.filter(teacher=request.user).select_related('user')
        global_student_list = all_students(request)
        
        return render(request, 'my_students.html', {
            "students": students,
            "all_students": global_student_list
        })
    
    # 2. Si no es profesor (así aseguramos que SIEMPRE responda un HttpResponse)
    global_student_list = all_students(request)
    return render(request, 'my_students.html', {
        "students": [],
        "all_students": global_student_list
    })

@login_required
def remove_student_from_my_students_list(request, student_id):
    student_profile = Profile.objects.get(user_id=student_id)
    if student_profile.teacher == request.user:
        student_profile.teacher = None
        student_profile.save()
        return redirect('my_students')
    else:
        return HttpResponseForbidden("You are not allowed to remove this student.")