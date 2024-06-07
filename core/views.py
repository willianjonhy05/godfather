from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .forms import UsuarioForms
from django.views.generic import CreateView
from django.contrib import messages


    
class UsuarioCreateView(CreateView):
    form_class = UsuarioForms
    template_name = 'public/sign-up.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        if form.cleaned_data['concorda_termos']:
            return super().form_valid(form)
        else:
            form.add_error('concorda_termos', 'Você deve concordar com os termos para se registrar.')
            return self.form_invalid(form)


def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForms(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.concorda_termos = True
            usuario.save()
            messages.success(request, "Usuário criado com sucesso, faça seu Login!")
            return redirect('login')
    else:
        form = UsuarioForms()
    
    return render(request, 'public/sign-up.html', {'form': form})