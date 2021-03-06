from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from weatherAnalyzer.models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'your email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'password'})
        }

    def clean(self):
        return self.cleaned_data

    def authenticate(self):
        mail = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            return User.objects.get(email=mail, password=password)
        except:
            return None


class SignUpForm(LoginForm):
    confirmEmail = forms.EmailField(label='Confirm email',
                                    widget=forms.EmailInput(attrs={'placeholder': 'confirm email'}))

    confirmPassword = forms.CharField(label='Confirm password',
                                      widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
                                      max_length=15,
                                      min_length=6)

    class Meta(LoginForm.Meta):
        fields = ['email', 'confirmEmail', 'password', 'confirmPassword']

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Account with this email already exists!')
        if not self.check_emails() or not self.check_passwords():
            raise ValidationError('Emails and passwords must match!')
        return self.cleaned_data

    def check_emails(self):
        e = self.cleaned_data.get('email')
        ce = self.cleaned_data.get('confirmEmail')
        if None not in (e, ce):
            return e == ce

    def check_passwords(self):
        p = self.cleaned_data.get('password')
        cp = self.cleaned_data.get('confirmPassword')
        if None not in (p, cp):
            return p == cp
