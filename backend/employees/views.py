# backend/employees/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import CreateEmployeeForm  # Import the updated form
import json

# Custom JWT Token Obtain Pair View
# backend/employees/views.py

# Custom Token Obtain Pair View
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens with additional user data.
    Sets the refresh token in an HTTP-Only Secure cookie and only sends access token in response.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response_data = {
            'success': True,
            'access': str(access_token),
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                # Add other user fields as needed
            }
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # Set the refresh token in an HTTP-Only Secure cookie
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,  # Ensure it's only sent over HTTPS
            samesite='Strict',  # or 'Lax' based on your needs
            path='/api/token/refresh/',  # Path for refresh endpoint
            max_age=24 * 60 * 60,  # 1 day in seconds
        )

        return response

# Custom Token Refresh View
class CustomTokenRefreshView(TokenObtainPairView):
    """
    Custom view to refresh JWT access tokens using the refresh token from HTTP-Only cookie.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'success': False, 'message': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            response_data = {
                'success': True,
                'access': str(new_access_token),
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        except Exception as e:
            return Response({'success': False, 'message': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated users to register
def register(request):
    """
    Register a new user.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    form = CreateEmployeeForm(data)

    if form.is_valid():
        user = form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout a user by blacklisting the refresh token from the cookie and deleting the cookie.
    """
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'success': False, 'message': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({'success': True, 'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('refresh_token')
        return response
    except Exception as e:
        return Response({'success': False, 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Retrieve authenticated user information.
    """
    return JsonResponse(
        {
            'employee_id': request.user.employee_id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        },
        status=200
    )

