#backend\employees\urls.py
from django.urls import path
from .views import logout_view, register, user_info

urlpatterns = [
    path('logout/', logout_view, name='logout'),
     path('user/', user_info, name='user_info'),
    path('register/', register, name='register'),
]
