from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Perfil, Usuario


@receiver(post_save, sender=Perfil)
def criar_perfil_de_usuario(sender, instance, created, **kwargs):
    if created:
        usuario = Usuario.objects.create(email=instance.email)

