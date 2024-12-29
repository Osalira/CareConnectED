#backend\employees\urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/auth/', include('djoser.urls')),
    path('api/auth/jwt/', include('djoser.urls.jwt')),
    #//
    path('api/auth/jwt/create/', include('djoser.urls.jwt')),
    path('api/auth/users/', include('djoser.urls')),

    #path('api/employees/', include('employees.urls')),  # Custom employee-related views

    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/register', views.register, name='register'),
]
