from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import UsuarioForms
from django.views.generic import CreateView
from django.contrib import messages
from .utils import is_superuser
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario, Ideia, Proposta, Areas
from .forms import AreasForm


    
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


# @login_required
# @user_passes_test(is_superuser)
def dashboard(request):
    template_name = 'admin/dashboard.html'
    qtde_usuarios = Usuario.objects.count()
    qtde_ideias = Ideia.objects.count()
    qtde_propostas = Proposta.objects.count()
    context = {
        'qtde_usuarios': qtde_usuarios,
        'qtde_ideias': qtde_ideias,
        'qtde_propostas': qtde_propostas,
    }
    return render(request, template_name, context)

# @login_required
# @user_passes_test(is_superuser)
def criar_areas(request):
    template_name = 'admin/nova-area.html'
    if request.method == 'POST':
        form = AreasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Área criada com sucesso!")
            return redirect('dashboard')
    else:
        form = AreasForm()
        
    context = {
        'form': form
    }
    return render(request, template_name, context)


# @login_required
# @user_passes_test(is_superuser)    
def listar_areas(request):
    template_name = 'admin/listar-areas.html' 
    areas = Areas.objects.all()      
    context = {
        'areas': areas,
    }
    return render(request, template_name, context)

# @login_required
# @user_passes_test(is_superuser)    
def atualizar_area(request):
    area = get_object_or_404(Areas, id=id)   
    template_name = 'admin/nova-area.html'
    if request.method == "POST":
        form = AreasForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área atualizada com sucesso!')
            return redirect('listar-empresas')
    else:
        form = AreasForm(instance=area)
    
    return render(request, template_name, {'form': form})

# @login_required
# @user_passes_test(is_superuser)      
def deletar_area(request, id):
    area = get_object_or_404(Areas, id=id)
    area.delete()
    messages.info(request, 'Área excluída com sucesso!')
    return redirect('listar_areas')


# @login_required
# @user_passes_test(is_superuser)      
def detalhar_area(request, id):
    area = get_object_or_404(Areas, id=id)
    return render(request, 'admin/detalhar_area.html', {'area': area})