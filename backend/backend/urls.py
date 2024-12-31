# backend\backend\urls.py
from django.contrib import admin
#//
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from employees.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Djoser Authentication Endpoints
    path('api/auth/', include('djoser.urls')),
    path('api/auth/jwt/', include('djoser.urls.jwt')),

    # App-Specific URLs
    path('api/employees/', include('employees.urls')),
    # path('api/appointments/', include('appointments.urls')),
    path('', include('appointments.urls')),
    # JWT Custom Endpoints
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Frontend Catch-All
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
]

