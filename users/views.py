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
