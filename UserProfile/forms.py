from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Business


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['company_name']
