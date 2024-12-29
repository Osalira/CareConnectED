#backend\employees\forms.py
from django import forms
from .models import Employee  # Import your custom Employee model

class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'employee_id', 'password']  # Fields from Employee model

    def save(self, commit=True) -> Employee:
        employee = super().save(commit=False)
        employee.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            employee.save()
        return employee
