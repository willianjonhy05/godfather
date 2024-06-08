from django.shortcuts import render, redirect, get_object_or_404
from .forms import InscricaoForm
from django.contrib import messages
from .utils import is_superuser
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Contato

# Create your views here.


def inscricao_newsletter(request):
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save()
            messages.success(request, 'Inscrição realizada com sucesso!')
    else:
        form = InscricaoForm()

    return render(request, 'public/inscricao.html', {'form': form})
    
# @login_required
# @user_passes_test(is_superuser)        
def MarcarComoLida(request, id):
    contato = get_object_or_404(Contato, id=id)
    if not contato.lida:
        contato.lida = True
        contato.save()
        messages.success(request, 'Mensagem marcada como lida!')
        return redirect('contatos')
    else:
        messages.info(request, 'Mensagem já está marcada como lida!')
        return redirect('contatos')

# @login_required
# @user_passes_test(is_superuser)       
def MarcarComoNaoLida(request, id):
    contato = get_object_or_404(Contato, id=id)
    if contato.lida:
        contato.lida = False
        contato.save()
        messages.success(request, 'Mensagem marcada como não lida!')
        return redirect('contatos')
    else:
        messages.info(request, 'Mensagem já está marcada como não lida!')
        return redirect('contatos')