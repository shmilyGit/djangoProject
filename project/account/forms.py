from django import forms
from django.contrib.auth.models import User
from .models import UserInfo

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("password do not match.")
        return cd['password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("name", "gender", "birth", "website", "phone", "comment", "photo")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
