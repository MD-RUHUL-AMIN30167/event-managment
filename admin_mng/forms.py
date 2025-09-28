from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from event_App.forms import StyleForMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model
User=get_user_model()


import re


class CustomRegistrationForm(StyleForMixin,forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password'] 
     # check same email
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('email already exists')
        return email
    # field error
    def clean_password(self):
        password=self.cleaned_data.get('password')
        errors=[]
        if len(password)<8:
            errors.append("your password must be charcter 8 long")
        if not re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            errors.append("Password must be at least 8 characters long, include uppercase, lowercase, digit, and special character.") 
        if errors:
            raise forms.ValidationError(errors)
        return password
    # non fileld error
    def clean(self):
        cleaned_data = super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password and confirm password not match please try again')
        return cleaned_data
    
class LoginForm(StyleForMixin,AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


# cteate group admin and manager
class CreateGroupForm(StyleForMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type'),
        widget=forms.CheckboxSelectMultiple(),  
        required=False,
        label='Assign Permissions',
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class EditProfileForm(StyleForMixin,forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','email','profile_image','bio')


