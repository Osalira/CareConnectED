from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('djoser.urls')),
    path('api/auth/jwt/', include('djoser.urls.jwt')),
    #//
    path('api/auth/jwt/create/', include('djoser.urls.jwt')),
    path('api/auth/users/', include('djoser.urls')),

    #path('api/employees/', include('employees.urls')),  # Custom employee-related views
]
