from django import forms
from django.contrib.auth.forms import UserCreationForm
from myApp.models import User


class RegisterForm(UserCreationForm):
    # username = forms.CharField(max_length=30, required=True, help_text='Optional')
    email = forms.EmailField(max_length=254, required=True, help_text='Enter a valid email address')
    password1 = forms.CharField(max_length=254, required=True)
    password2 = forms.CharField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
