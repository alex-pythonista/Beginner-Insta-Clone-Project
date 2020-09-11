from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True, label="",widget=forms.TextInput(attrs={'placeholder': 'user@example.com'}))
    username = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password1 = forms.CharField(
        required=True,
        label = "",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True,
        label = "",
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter the password'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label="",widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(
        required=True,
        label = "",
        widget=forms.PasswordInput(attrs={'placeholder': 'password'})
    )
    class Meta:
        model = User
        fields = ('username', 'password')

class EditProfile(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = UserProfile
        exclude = ('user', ) 