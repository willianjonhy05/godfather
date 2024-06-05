from django.shortcuts import render
from .forms import InscricaoForm
from django.contrib import messages

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
    