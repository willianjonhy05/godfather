"""
URL configuration for energia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import dashboard, lista_de_usuarios, atualizar_usuario
from .views import criar_areas, deletar_area, detalhar_area, listar_areas, atualizar_area, contatos



urlpatterns = [
    path('', dashboard, name='dashboard'),
    
    path('nova-area/', criar_areas, name='nova_area'),
    path('listar-areas/', listar_areas, name='listar_areas'),
    path('detalhar-area/<int:id>/', detalhar_area, name='detalhar_area'),
    path('atualizar-area/<int:id>/', atualizar_area, name='atualizar_area'),
    path('deletar-area/<int:id>/', deletar_area, name='deletar_area'),
    
    path('contatos/', contatos, name='contatos'),
    
    path('usuarios/', lista_de_usuarios, name='lista_usuarios'),
    path('usuarios/atualizar/<int:id>/', atualizar_usuario, name='atualizar_usuario'),
    

]


