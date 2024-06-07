from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
from django.forms import ModelForm, EmailField, CharField, DateField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class UsuarioForms(forms.ModelForm):
    password = CharField(label='Senha', required=True, widget=forms.PasswordInput())
    password2 = CharField(label='Senha', required=True, widget=forms.PasswordInput())

    class Meta:
        model = Perfil
        fields = ['nome',  'telefone', 'email', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise ValidationError(
                {"password": "As senhas não coincidem!"}
            )
        
        return attrs
        
        