from django.contrib import admin
from .models import Perfil, Usuario, Areas

# Register your models here.

admin.site.register(Perfil)
admin.site.register(Usuario)


@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "nome"]
    search_fields = ["nome", "codigo"]
    list_display_links = [ "nome", "codigo" ]
    list_per_page = 10
