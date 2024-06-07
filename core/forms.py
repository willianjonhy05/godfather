from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
from django.forms import ModelForm, EmailField, CharField, DateField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class UsuarioForms(forms.ModelForm):
    nome = CharField(label="Nome Completo", max_length=100)
    cpf = CharField(label="CPF", max_length=14)
    telefone = CharField(label="Telefone", max_length=11)
    password = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirme a senha', required=True, widget=forms.PasswordInput())
    data_de_nascimento = DateField(label='Data de Nascimento')
    
    class Meta:
        model = Perfil
        fields = ['email', 'nome', 'username', 'cpf', 'telefone', 'data_de_nascimento', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise ValidationError(
                {"password": "As senhas não coincidem!"}
            )
        
        return attrs
        
        
        
# class RegistrationForm(UserCreationForm):

#     first_name = CharField(max_length=150, label="Nome")
#     last_name = CharField(max_length=150, label="Sobrenome")
#     email = EmailField(max_length=200, label="Email")
    
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]