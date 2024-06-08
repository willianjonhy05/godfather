from django.db import models
from django.utils import timezone
from core.models import Usuario

# Create your models here.

class Contato(models.Model):
 
    ASSUNTO = (
        ('Sugestão', 'Sugestão'),
        ('Reclamação','Reclamação'),
        ('Dúvida','Dúvida'),
        ('Outro','Outro'),
    )   
    
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Usuario do Contato')
    nome = models.CharField('nome', max_length=155)
    email = models.EmailField('e-mail', max_length=255)
    telefone = models.CharField('telefone', blank=False,null=False,max_length=20)
    assunto  = models.CharField(max_length=20, choices=ASSUNTO)    
    data = models.DateTimeField(default=timezone.now)
    mensagem = models.TextField('mensagem', max_length=500)
    lida = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nome}"
    

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        

class Inscricao(models.Model):
    email = models.EmailField(unique=True)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return self.email