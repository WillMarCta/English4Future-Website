# to render the html page and to redirect the user to another page after they sign up
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
from .models import Profile

# Create your views here.


def user_signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                user.profile.role = 'student'
                user.profile.save()

                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    "error": "Username already exists"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            "error": "Password does not match"
        })


def user_signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

        return render(request, 'signin.html', {
            'form': form,
            'error': "Invalid username or password"
        })


def signout(request):
    logout(request)  # Esto elimina la sesión del usuario
    # Lo mandamos de vuelta a la landing page
    return redirect('English4Future')

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
    if request.method == 'POST':
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