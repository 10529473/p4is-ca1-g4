from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import Account
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text='Required. Add a valid e-mail address')

    class Meta:
        model = Account
        fields = ('email','username','password1','password2',)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            # account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except ObjectDoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)