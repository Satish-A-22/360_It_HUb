# forms.py

from django import forms
from It_Services.models import UserData,Service  # Import the correct model name

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['email', 'password', 'check_me_out']
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'payment_terms', 'service_price', 'service_package', 'service_tax', 'service_image']