from django.shortcuts import render, redirect, get_object_or_404
from contato.forms import ContatoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, MeuPerfilCompletoForm, MeuPerfilInfosPessoais, MeuPerfilDocsPessoais, MeuPerfilEnderecosPessoais, MeuPerfilRedesSociaisPessoais, MeuPasswordChangeForm
from django.contrib.auth.decorators import login_required
from core.models import Ideia, Proposta, Usuario
from django.contrib.auth import update_session_auth_hash

def home(request):
    template_name = 'public/index.html'
    context = {}
    return render(request, template_name, context)

# @login_required
def feed_usuario(request):
    template_name = 'profile/feed.html'
    usuario = get_object_or_404(Usuario, usuario=request.user)
    context = {'usuario': usuario,}
    return render(request, template_name, context) 


def login_usuario(request):
    template_name = 'public/login.html'
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            user = authenticate(username=usuario, password=senha)
            if user is not None and user.is_active:
                login(request, user)
                messages.info(request, 'Você fez login com sucesso!')
                return redirect('feed_user')
            else:
                messages.error(request, 'Usuário ou senha inválidos!')
        else:
            messages.error(request, 'Formulário inválido!')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def alterar_senha(request):
    usuario = get_object_or_404(Usuario, usuario=request.user)
    if request.method == 'POST':
        form = MeuPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('meu_perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = MeuPasswordChangeForm(request.user)
    
    return render(request, 'profile/alterar_senha.html', {
        'form': form,
        'usuario': usuario,
    })

# @login_required
def sair(request):
    logout(request)
    return redirect('login_usuario')

def contato(request):
    template_name = 'public/contato.html'
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('contato')
        form = ContatoForm(request.POST)
    else:
        form = ContatoForm() 
    context = {
        'form': form,
    }
    
    return render(request, template_name, context)

def politica(request):
    template_name = 'public/politica.html'
    context = {}
    return render(request, template_name, context)


def contato_usuario(request):
    usuario = get_object_or_404(Usuario, usuario=request.user)
    template_name = 'profile/contato.html'

    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            contato = form.save(commit=False)
            contato.usuario = usuario
            contato.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('contato')
    else:
        form = ContatoForm()

    context = {
        'form': form,
        'usuario': usuario,
    }
    
    return render(request, template_name, context)

def minhas_ideias(request) :
    perfil = get_object_or_404(Usuario, usuario=request.user)
    template_name = 'profile/minhas_ideias.html'
    ideias = Ideia.objects.filter(autor=perfil)
    context = {
        'ideias': ideias,
        'perfil': perfil,
    }
    return render(request, template_name, context)


def minhas_propostas(request) :
    perfil = get_object_or_404(Usuario, usuario=request.user)
    template_name = 'profile/minhas_propostas.html'
    propostas = Proposta.objects.filter(investidor=perfil)
    context = {
        'propostas': propostas,
        'perfil': perfil,
    }
    return render(request, template_name, context)

def meu_perfil(request):
    usuario = get_object_or_404(Usuario, usuario=request.user)
    template_name = 'profile/meu_perfil.html'
    
    
    if request.method == 'POST':
        formpessoal = MeuPerfilInfosPessoais(request.POST, request.FILES, instance=usuario)
        formdocs = MeuPerfilDocsPessoais(request.POST, instance=usuario)
        formsenderecos = MeuPerfilEnderecosPessoais(request.POST, instance=usuario)
        formsredes = MeuPerfilRedesSociaisPessoais(request.POST, instance=usuario)
        
        if formpessoal.is_valid():
            formpessoal.save()
            messages.success(request, 'Informações pessoais atualizadas com sucesso!')
        
        if formdocs.is_valid():
            formdocs.save()
            messages.success(request, 'Documentos atualizados com sucesso!')
            
        if formsenderecos.is_valid():
            formsenderecos.save()
            messages.success(request, 'Endereços atualizados com sucesso!')
            
        if formsredes.is_valid():
            formsredes.save()
            messages.success(request, 'Redes sociais atualizadas com sucesso!')
        
        return redirect('meu_perfil')

    else:
        formpessoal = MeuPerfilInfosPessoais(instance=usuario)
        formdocs = MeuPerfilDocsPessoais(instance=usuario)
        formsenderecos = MeuPerfilEnderecosPessoais(instance=usuario)
        formsredes = MeuPerfilRedesSociaisPessoais(instance=usuario)
    
    context = {
        'usuario': usuario,
        'formpessoal': formpessoal,
        'formdocs': formdocs,
        'formsenderecos': formsenderecos,
        'formsredes': formsredes,
    }
    
    return render(request, template_name, context)


# def meu_perfil(request):
#     usuario = get_object_or_404(Usuario, usuario=request.user)
#     template_name = 'profile/meu_perfil.html'
    
#     if request.method == 'POST':
#         form = MeuPerfilCompletoForm(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Usuário atualizado com sucesso!')
#             return redirect('meu_perfil')
#     else:
#         form = MeuPerfilCompletoForm(instance=usuario)
    
#     return render(request, template_name, {'form': form, 'usuario': usuario})