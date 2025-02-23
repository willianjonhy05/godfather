from .models import Areas
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, Usuario
from django.forms import ModelForm, EmailField, CharField, DateField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class UsuarioForms(forms.ModelForm):
    password = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar Senha', required=True, widget=forms.PasswordInput())
    concorda_termos = forms.BooleanField(label='Concordo com os termos de uso e privacidade', required=True)

    class Meta:
        model = Perfil
        fields = ['nome', 'telefone', 'email', 'password', 'password2', 'concorda_termos']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError({"password": "As senhas não coincidem!"})

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        
    
class AreasForm(forms.ModelForm):
                           
    class Meta:
        model = Areas
        fields = ['nome', 'observacoes']
        
        
class UsuarioFormCompletoAdmin(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__' 