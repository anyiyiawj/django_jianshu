from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','email','password')

class ProfileForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False)
    signature = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)

    class Meta:
        model = Profile
        fields = ['email', 'signature', 'location', ]

class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="旧密码",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="新密码",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="确定新密码",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']