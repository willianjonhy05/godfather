from django.contrib import admin
from .models import Contato

# Register your models here.

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ["id", "nome", "email", "telefone", "assunto", "data", "lida"]
    search_fields = ["nome", "email", "telefone"]
    list_display_links = [ "nome", "id"]
    list_per_page = 10
    list_editable = ["lida"]

