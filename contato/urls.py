from django.urls import path
from .views import MarcarComoNaoLida, MarcarComoLida



urlpatterns = [
    path('marcar_como_lida/<int:id>/', MarcarComoLida, name='marcar_como_lida' ),
    path('marcar_como_nao_lida/<int:id>/', MarcarComoNaoLida, name='marcar_como_nao_lida' ),
    


]
