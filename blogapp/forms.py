from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from blogapp.models import UserProfile, Blogs, Comments

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following",)
        widgets={
            "date_of_birth":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class ChangePasswordForm(forms.Form):
    oldpassword=forms.CharField(widget=forms.PasswordInput)
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField()

class BlogForm(ModelForm):
    class Meta:
        model=Blogs
        fields=[
            "title",
            "description",
            "image",
            ]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"})

        }

class CommentForm(ModelForm):
    class Meta:
        model=Comments
        fields=[
            "comment"
        ]

        widgets={
            "comment":forms.TextInput(attrs={'class':'form-control'})
        }
