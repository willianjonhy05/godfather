from django import forms
from core.models import Usuario
from django.contrib.auth.forms import PasswordChangeForm
from core.models import Perfil
from django.core.exceptions import ValidationError

# class LoginForm(forms.Form):
#     usuario = forms.CharField(
#         label='E-mail',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Digite seu e-mail',
#             'id': 'id_usuario',
#             'required': True
#         })
#     )
#     senha = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Digite a sua senha',
#             'id': 'id_senha',
#             'required': True
#         })
#     )


class MeuPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha Atual",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha Atual'})
    )
    new_password1 = forms.CharField(
        label="Nova Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova Senha'}),
        help_text="Sua senha deve ter pelo menos 8 caracteres e não deve ser muito comum."
    )
    new_password2 = forms.CharField(
        label="Confirme a Nova Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a Nova Senha'})
    )

    class Meta:
        model = Perfil
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError({"new_password2": "As senhas não coincidem!"})

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user


    
class LoginForm(forms.Form):
    usuario = forms.CharField(
        label='E-mail',
        widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'label': 'E-mail', 
        'placeholder': 'Digite seu e-mail', 
        'id': 'id_usuario', 
        'required': True
    }))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Digite a sua senha', 
        'id': 'id_senha', 
        'required': True
    }))
    
class MeuPerfilCompletoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ['usuario', 'ativo', 'data_de_inscricao']
        
        
class MeuPerfilInfosPessoais(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['avatar',	'nome',	'descricao', 'profissao', 'sexo', 'telefone', 'email']
        
class MeuPerfilDocsPessoais(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cpf', 'rg', 'orgao_expedidor', 'nacionalidade', 'data_nascimento']
        
class MeuPerfilEnderecosPessoais(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cep', 'uf', 'cidade', 'endereco', 'bairro', 'numero']

class MeuPerfilRedesSociaisPessoais(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['perfil_instagram', 'perfil_twitterx', 'perfil_facebook',	'perfil_linkedin']