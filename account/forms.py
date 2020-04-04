from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import  Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text='Required. Add a valid e-mail address')

    class Meta:
        model = Account
        fields = ('email','username','password1','password2',)

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')
    
    def clean(self):
        email = self.cleaned_data
        password = self.cleaned_data['password']
        if not authenticate(email=email,password=password):
            raise forms.ValidationError("Invalid login")