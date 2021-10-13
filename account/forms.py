from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields= ['username', 'first_name', 'email', 'password1', 'password2']

class EditProfileForm(forms.Form):
    image = forms.ImageField(required=False)
    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    city = forms.CharField(max_length=100, required=False)
