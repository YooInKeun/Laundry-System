from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['password1', 'password2']
        
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
            'password1',
            'password2',
            'email',
            'phone',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'password'
                }
            ),
            'password2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'password'
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }