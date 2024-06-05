from django import forms
from .models import Contato, Inscricao

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']
        
        
class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['email']