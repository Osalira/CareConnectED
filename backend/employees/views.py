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
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens with additional user data.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user
        refresh = RefreshToken.for_user(user)

        return Response({
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'employee_id': user.employee_id,
                # Add other user fields as needed employeeId
            }
        })

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
    Logout a user by blacklisting the provided refresh token.
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the refresh token
        return Response({'success': True, 'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'success': False, 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
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
