from django import forms
from core.models import Usuario

class LoginForm(forms.Form):
    usuario = forms.CharField(
        label='E-mail',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail',
            'id': 'id_usuario',
            'required': True
        })
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a sua senha',
            'id': 'id_senha',
            'required': True
        })
    )
    
class MeuPerfilForm(forms.Form):
    class Meta:
        model = Usuario
        fields = ['avatar', 'nome', 'descricao', 'profissao', 'sexo', 'cpf', 'rg', 'orgao_expedidor', 'cep', 'nacionalidade', 'telefone', 'email', 'perfil_instagram', 'perfil_twitterx', 'perfil_facebook', 'perfil_linkedin', ]