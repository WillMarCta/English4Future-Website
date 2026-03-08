from django.shortcuts import render


# Create your views here.
def English4Future(request):
    return render(request, 'landing.html')
