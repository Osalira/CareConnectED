"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
#//
from django.views.generic import TemplateView
from django.urls import path, include
from employees import views
# from appointments import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/jwt/', include('djoser.urls.jwt')),
    path('', include('employees.urls')),
    path('', include('appointments.urls')),
    #//path('api/appointments/', include('appointments.urls')),  # Include appointments URLs
    #//
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
]
