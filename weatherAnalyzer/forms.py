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
            return User.objects.get(name=mail, password=password)
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
        return self.cleaned_data
