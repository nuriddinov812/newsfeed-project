from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    email = forms.EmailField(label ='Email')
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
        

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
        
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        # photo and date_of_birth live on the Profile model, not User
        model = Profile
        fields = ('photo', 'date_of_birth')                
        