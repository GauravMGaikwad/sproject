from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    repeat_password = forms.CharField(widget=forms.PasswordInput, label="Repeat Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        # Check for matching passwords
        if password != repeat_password:
            raise ValidationError("Passwords do not match.")

        # Check if username or email already exists
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already taken.")
        
        return cleaned_data

    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'password']
