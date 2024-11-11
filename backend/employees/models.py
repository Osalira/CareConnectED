from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# models.py

class Employee(AbstractUser):
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Add additional fields as needed
    
    # Remove 'username' field if not needed
    username = None

    USERNAME_FIELD = 'employee_id'  # Set employeeId as the unique identifier for authentication
    REQUIRED_FIELDS = ['first_name', 'last_ame']  # Other required fields
