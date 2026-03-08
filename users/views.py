# to render the html page and to redirect the user to another page after they sign up
from django.shortcuts import render, redirect
# to create the form for the user to sign up
from django.contrib.auth.forms import UserCreationForm
# to create the user in the database when they sign up
from django.contrib.auth.models import User
# to create the cookie for the user when they sign up
from django.contrib.auth import login
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
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
                login(request, user)
                return redirect('task')
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
    form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})
