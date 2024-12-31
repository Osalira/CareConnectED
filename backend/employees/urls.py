#backend\employees\urls.py
from django.urls import path
from .views import logout_view, register, user

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('user/', user, name='user_info'),
    path('register/', register, name='register'),
]
