from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .forms import UsuarioForm


def create_user_profile(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UsuarioForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']
            user.username = user_form.cleaned_data['email'] 
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.usuario = user
            profile.save()
            
            return redirect('profile_success')
    else:
        user_form = UserCreationForm()
        profile_form = UsuarioForm()
    
    return render(request, 'public/create_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })