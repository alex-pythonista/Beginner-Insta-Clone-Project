from django import forms
from django.contrib.auth.models import User
from .models import Posts

class PostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ['image', 'caption']