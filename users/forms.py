from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm
)
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # self.fields['email'].widget.attrs['class'] = 'form-control mb-2'
        # self.fields['email'].widget.attrs['placeholder'] = 'Email'

        # self.fields['password1'].widget.attrs['class'] = 'form-control mb-2'
        # self.fields['password1'].widget.attrs['placeholder'] = 'Password'

        # self.fields['password2'].widget.attrs['class'] = 'form-control mb-2'
        # self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'