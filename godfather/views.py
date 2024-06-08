from django.shortcuts import render, redirect
from contato.forms import ContatoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from core.models import Ideia, Proposta

def home(request):
    template_name = 'public/index.html'
    context = {}
    return render(request, template_name, context)

# @login_required
def feed_usuario(request):
    template_name = 'profile/feed.html'
    context = {}
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
                return redirect('login_usuario')
        else:
            messages.error(request, 'Formulário inválido!')
        return redirect('login_usuario')
    
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, template_name, context)


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
    perfil = request.user.usuario
    template_name = 'profile/contato.html'
    if request.method == 'POST':
        if form.is_valid():
            contato = form.save(commit=False)
            contato.usario = perfil
            contato.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('contato')
        form = ContatoForm(request.POST)
    else:
        form = ContatoForm() 
    context = {
        'form': form,
    }
    
    return render(request, template_name, context) 

def minhas_ideias(request) :
    perfil = request.user.usuario
    template_name = 'profile/minhas_ideias.html'
    ideias = Ideia.objects.filter(autor=perfil)
    context = {
        'ideias': ideias,
        'perfil': perfil,
    }
    return render(request, template_name, context)


def minhas_propostas(request) :
    perfil = request.user.usuario
    template_name = 'profile/minhas_propostas.html'
    propostas = Proposta.objects.filter(investidor=perfil)
    context = {
        'propostas': propostas,
        'perfil': perfil,
    }
    return render(request, template_name, context)

def meu_perfil(request):
    perfil = request.user.usuario
    template_name = 'profile/meu_perfil.html'
    context = {}
    return render(request, template_name, context)