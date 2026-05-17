"""
URL configuration for english4future project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages import views as pages_views
from users import views as user_views
from task import views as task_views
from courses import views as courses_views
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('English4Future', pages_views.English4Future, name='English4Future'),
    path('signup/', user_views.user_signup, name='signup'),
    path('signin/', user_views.user_signin, name='signin'),
    path('task/', include('task.urls')),
    path('courses/', courses_views.courses, name='courses'),
    path('dashboard/', pages_views.dashboard, name='dashboard'),
    path('logout/', user_views.signout, name='logout')
]
