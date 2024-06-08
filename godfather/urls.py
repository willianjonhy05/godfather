"""
URL configuration for godfather project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, contato, politica, feed_usuario, login_usuario, sair, contato_usuario, minhas_ideias, minhas_propostas, meu_perfil
from contato.views import inscricao_newsletter
from core.views import UsuarioCreateView, criar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscricao/', inscricao_newsletter, name='inscricao'),
    path('login/', login_usuario, name='login_usuario'),
    path('sair/', sair, name='sair'),
    path('politica/', politica, name='politica'),
    path('feed/', feed_usuario, name='feed_user'),
    path('feed/minhas-ideias/', minhas_ideias, name='minhas_ideias'),
    path('feed/minhas-propostas/', minhas_propostas, name='minhas_propostas'),
    path('meu-perfil/', meu_perfil, name='meu_perfil'),
    path('dashboard/', include('core.urls')),
    path('contato/', include('contato.urls')),
    path('criar-usuario/', criar_usuario, name='registrar_usuario'),
    path('contato/', contato_usuario, name='contato'),
    path('fale-conosco/', contato, name='fale-conosco'),
    path('', home, name='home'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
