from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, CharField



class UsuarioForms(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'sexo', 'cpf', 'email', 'data_nascimento']
        
        
        
# class RegistrationForm(UserCreationForm):

#     first_name = CharField(max_length=150, label="Nome")
#     last_name = CharField(max_length=150, label="Sobrenome")
#     email = EmailField(max_length=200, label="Email")
    
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]