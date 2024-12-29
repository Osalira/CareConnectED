#backend\employees\views.py
from django.shortcuts import render
from django.http import HttpResponse
#///
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from .forms import CreateEmployeeForm  # Import the updated form
# Create your views here.


def home(request):
    return HttpResponse("Welcome to the Mister Ed Medical Information System!")
#///
@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})


@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        employee_id = data['employee_id']
        password = data['password']
        # print("Received data:", data)
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON'}, status=400
        )

    # Authenticate using employee_id
    user = authenticate(request, username=employee_id, password=password)

    if user:
        login(request, user)
        # Return success along with the user's first name and last name
        return JsonResponse({
            'success': True,
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    return JsonResponse(
        {'success': False, 'message': 'Invalid credentials'}, status=401
    )



@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})


@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {'employee_id': request.user.employee_id, 'first_name': request.user.first_name, 'last_name': request.user.last_name}
        )
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )


@require_http_methods(['POST'])
def register(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # Log data received for debugging
    # print("Received data:", data)

    # Initialize form with parsed data
    form = CreateEmployeeForm(data)

    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        # Log form errors for debugging
        # print("Form errors:", form.errors)
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)
