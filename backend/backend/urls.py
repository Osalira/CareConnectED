
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
    
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
]
