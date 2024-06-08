from django.shortcuts import render, redirect
from contato.forms import ContatoForm
from django.contrib import messages

def home(request):
    template_name = 'public/index.html'
    context = {}
    return render(request, template_name, context)


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

