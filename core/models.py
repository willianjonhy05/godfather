from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNPJ
import re, random

# Create your models here.


class Perfil(AbstractUser):
    
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField("Telefone", max_length=11)
    nome = models.CharField("Nome Completo", max_length=100)
    concorda_termos = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
    def gerar_username(self):
        email = self.email
        if '@' in email:
            base_username = email.split('@')[0]
        else:
            base_username = email
        
        while True:
            numeros_aleatorios = ''.join(random.choices('0123456789', k=4))
            username = f"{base_username}{numeros_aleatorios}"
            if not Perfil.objects.filter(username=username).exists():
                break
        
        return username
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.gerar_username()
        super().save(*args, **kwargs)

    
    class Meta:
        verbose_name = "Perfil de Login"
        verbose_name_plural = "Perfis de Login"  


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
        
        
    class Meta:
        verbose_name = "Segmento"
        verbose_name_plural = "Segmentos"  

class Usuario(models.Model):
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
        
    usuario = models.OneToOneField(Perfil, verbose_name='Usuario', on_delete=models.CASCADE, blank=True, null=True, related_name='usuario')
    avatar = models.ImageField("Foto", upload_to='avatar/%Y/%m/%d/', blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=11)
    nome = models.CharField("Nome Completo", max_length=100)
    descricao = models.TextField("Sobre mim", max_length=500, null=True, blank=True)
    profissao = models.CharField("Profissão", max_length=60, null=True, blank=True)
    sexo = models.CharField("Sexo", max_length=1, choices=SEXO, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, unique=True, null=True, blank=True)
    rg = models.CharField("RG", max_length=20, unique=True, null=True, blank=True)
    orgao_expedidor = models.CharField("Órgão Expedidor", max_length=20, choices=ORGAOS_EXPEDIDORES, null=True, blank=True)
    cep = models.CharField("CEP", max_length=8, null=True, blank=True)
    uf = models.CharField("Estado", max_length=2, choices=ESTADO, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=50, null=True, blank=True)
    endereco = models.CharField("Nome da Rua/Avenida", max_length=50, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=25, null=True, blank=True)
    numero = models.CharField("Número", max_length=25, null=True, blank=True)
    nacionalidade = models.CharField("Nacionalidade", max_length=20, default="Brasileira")
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    email = models.EmailField("Email") 
    data_de_inscricao = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField("Status do Usuário", default=True)
    perfil_instagram = models.URLField("Link do Perfil no Instagram", blank=True, null=True)
    perfil_twitterx = models.URLField("Link do Perfil no Twitter/X", blank=True, null=True)
    perfil_facebook = models.URLField("Link do Perfil no Facebook", blank=True, null=True)
    perfil_linkedin = models.URLField("Link do Perfil no LinkedIn", blank=True, null=True)
    
    @property
    def idade(self):
        hoje = date.today()
        diferenca = hoje - self.data_nascimento
        return round(diferenca.days // 365.25) 

    def __str__(self):
        return self.usuario.nome
    
    def validate_cpf(self):
        if self.cpf:
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

    administrador =  models.ForeignKey(Usuario, verbose_name='Administrador da Empresa', on_delete=models.CASCADE)
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
        
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"



class Ideia(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em Progresso', 'Em Progresso'),
        ('Concluída', 'Concluída'),
        ('Rejeitada', 'Rejeitada')
    ]

    TIPO_CHOICES = [
        ('Produto', 'Produto'),
        ('Serviço', 'Serviço')
    ]
    
    titulo = models.CharField("Título da Ideia", max_length=100)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, related_name='area')
    descricao = models.TextField("Descrição da Ideia")
    foto = models.ImageField("Foto", upload_to='ideias/%Y/%m/%d/', blank=True, null=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ideia')
    data_criacao = models.DateTimeField("Data de Criação", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Data de Atualização", auto_now=True)
    status = models.CharField("Status da Ideia", max_length=20, choices=STATUS_CHOICES, default='Pendente')
    justificativa = models.TextField("Justificativa", blank=True, null=True)
    objetivos = models.TextField("Objetivos", blank=True, null=True)
    metodologia = models.TextField("Metodologia", blank=True, null=True)
    cronograma = models.TextField("Cronograma", blank=True, null=True)
    tipo = models.CharField("Tipo", max_length=20, choices=TIPO_CHOICES, default='Produto')
    problematica = models.TextField("Problemática", blank=True, null=True)
    publico_alvo = models.CharField("Público Alvo", max_length=255, blank=True, null=True)
    viabilidade = models.TextField("Análise de Viabilidade", blank=True, null=True)
    impacto = models.TextField("Impacto Esperado", blank=True, null=True)
    investimento_desejado = models.DecimalField("Investimento Desejado (R$)", max_digits=10, decimal_places=2, blank=True, null=True)
    resultados_esperados = models.TextField("Resultados Esperados", blank=True, null=True)
    riscos = models.TextField("Riscos e Mitigações", blank=True, null=True)
    parceiros = models.TextField("Parcerias Estratégicas", blank=True, null=True)
    recursos_necessarios = models.TextField("Recursos Necessários", blank=True, null=True)
    documentos = models.FileField("Outros documentos", upload_to='documentos/%Y/%m/%d/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Ideia"
        verbose_name_plural = "Ideias"


    def __str__(self):
        return self.titulo
    
class Proposta(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aceita', 'Aceita'),
        ('Rejeitada', 'Rejeitada')
    ]

    ideia = models.ForeignKey(Ideia, on_delete=models.CASCADE, verbose_name='Ideia')
    investidor = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Investidor')
    data_proposta = models.DateTimeField("Data da Proposta", auto_now_add=True)
    valor_investimento = models.DecimalField("Valor do Investimento (R$)", max_digits=10, decimal_places=2)
    condicoes = models.TextField("Condições da Proposta")
    status = models.CharField("Status da Proposta", max_length=20, choices=STATUS_CHOICES, default='Pendente')
    retorno_esperado = models.DecimalField("Retorno Esperado (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    prazo_retorno = models.CharField("Prazo para Retorno do Investimento", max_length=100, blank=True, null=True)
    comentarios = models.TextField("Comentários Adicionais", blank=True, null=True)

    class Meta:
        verbose_name = "Proposta"
        verbose_name_plural = "Propostas"


    def __str__(self):
        return f"Proposta de {self.investidor.username} para {self.ideia.titulo}"