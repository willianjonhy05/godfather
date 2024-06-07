from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .forms import UsuarioForms
from django.views.generic import CreateView


    
class UsuarioCreateView(CreateView):
    form_class = UsuarioForms
    template_name = 'public/sign-up.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('home')

