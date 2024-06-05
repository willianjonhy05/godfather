from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNPJ
import re, random

# Create your models here.

class Areas(models.Model):
    nome = models.CharField("Nome da Área", max_length=25)
    observacoes = models.TextField("Informações sobre a área")
    codigo = models.CharField("Código da Área", max_length=7, unique=True, editable=False)


    def __str__(self):
        return self.nome
    
    def gerar_codigo(self):
        nome_abreviado = self.nome[:3].upper()
        numeros_aleatorios = ''.join(random.choices('0123456789', k=4))
        codigo = nome_abreviado + numeros_aleatorios
        if not Areas.objects.filter(codigo=codigo).exists():
            return codigo
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)

class Candidato(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    
    ESTADO = (
		('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
		('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
		('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'),
		('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
		('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'),
		('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),
		('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
		('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
		('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),
		('TO', 'Tocantins')
	)
    
    ORGAOS_EXPEDIDORES = [
        ('SSP', 'Secretaria de Segurança Pública'),
        ('PC', 'Polícia Civil'),
        ('DETRAN', 'Departamento de Trânsito'),
        ('ITEP', 'Instituto Técnico-Científico de Perícia'),
        ('POLITEC', 'Politec'),
        ('IGP', 'Instituto-Geral de Perícias'),
        ('IPC', 'Instituto de Polícia Científica'),
    ]
        
    usuario = models.OneToOneField(User, verbose_name='Usuario', on_delete=models.CASCADE, blank=True, null=True, related_name='funcionario')
    telefone = models.CharField("Telefone", max_length=11)
    nome = models.CharField("Nome Completo", max_length=100)
    sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    rg = models.CharField("RG", max_length=20, unique=True)
    orgao_expedidor = models.CharField("Órgão Expedidor", max_length=20, choices=ORGAOS_EXPEDIDORES, null=True, blank=True)
    cep = models.CharField("CEP", max_length=8, null=True, blank=True)
    uf = models.CharField("Estado", max_length=2, choices=ESTADO, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=50, null=True, blank=True)
    endereco = models.CharField("Nome da Rua/Avenida", max_length=50, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=25, null=True, blank=True)
    numero = models.CharField("Número", max_length=25, null=True, blank=True)
    nacionalidade = models.CharField("Nacionalidade", max_length=20, default="Brasileira")
    data_nascimento = models.DateField('Data de Nascimento')
    email = models.EmailField("Email") 
    data_de_inscricao = models.DateTimeField(default=timezone.now)
    
    @property
    def idade(self):
        hoje = date.today()
        diferenca = hoje - self.data_nascimento
        return round(diferenca.days // 365.25) 

    def __str__(self):
        return self.nome
    
    def validate_cpf(self):
        self.cpf = re.sub(r'\D', '', self.cpf)
        cpf = CPF()
        if not cpf.validate(self.cpf):
            raise ValidationError(f'CPF inválido!')

    def save(self, *args, **kwargs):
        self.validate_cpf()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"  
        
        
class Empresa(models.Model):

    SITUACAO_CADASTRAL = (
        ('Nula', 'Nula'),
        ('Ativa', 'Ativa'),
        ('Suspensa', 'Suspensa'),
        ('Inapta', 'Inapta'),
        ('Ativa Não-Regular', 'Ativa Não-Regular'),
        ('Baixada', 'Baixada'),
    )    

    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, blank=True, null=True)
    razao_social = models.CharField("Nome da Razão Social", max_length=50, blank=True, null=True)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=50, blank=True, null=True)
    natureza_juridica = models.CharField("Natureza Jurídica", max_length=70, blank=True, null=True)
    data_de_abertura = models.DateField("Data de Abertura da Empresa", blank=True, null=True)
    situcao = models.CharField("Situação Cadastral", choices=SITUACAO_CADASTRAL, max_length=20)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True) 
    email = models.EmailField("Email")
    telefone = models.CharField("Telefone", max_length=11)
    cep = models.CharField("CEP", max_length=8)
    endereco = models.CharField("Endereço", max_length=50, blank=True, null=True)
    bairro = models.CharField("Bairro", max_length=25, blank=True, null=True)
    cidade = models.CharField("Cidade", max_length=50, blank=True, null=True)
    estado = models.CharField("UF", max_length=2, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=50, blank=True, null=True)
    site = models.URLField("Site", blank=True, null=True)
    confirmado = models.BooleanField("Confirmar Dados", default=False)

    def __str__(self):
        return self.razao_social

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def validate_cnpj(self):
        self.cnpj = re.sub(r'\D', '', self.cnpj)
        cnpj = CNPJ()
        if not cnpj.validate(self.cnpj):
            raise ValidationError('CNPJ inválido!')

    def save(self, *args, **kwargs):
        self.validate_cnpj()
        super().save(*args, **kwargs)


class Investidor(models.Model):
    ...