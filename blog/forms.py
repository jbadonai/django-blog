from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import BlogModel, CommentsModel


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    gender = forms.CharField(max_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'password1', 'password2']


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea())


class NewBlogForm(forms.Form):
    # author = forms.CharField(max_length=200)
    title = forms.CharField(max_length=200)
    body = forms.CharField(widget=forms.Textarea())


