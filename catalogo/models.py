from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg






class Carro(models.Model):
    ESCOLHAS_CARRO = [
    ('GT3', 'GT3'),
    ('PCUP', 'PCUP'),
]
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=ESCOLHAS_CARRO)
    foto = models.ImageField(upload_to='foto/%Y/%m/%d', blank=True)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
class Pista(models.Model):
    nome = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='foto/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.nome

# Função auxiliar para o caminho dos arquivos
def upload_setup_path(instance, filename):
    return f'setups/{instance.pista.nome}/{instance.carro.nome}/{instance.nome_versao}/{filename}'

# --- CLASSE PRIVADA ---
class Setup(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meus_setups_privados")
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="setups_privados")
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="setups_privados")

    nome_versao = models.CharField(max_length=50, default="Versão Inicial")
    
    # Arquivos
    config_qualy_safe = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_qualy      = models.FileField(upload_to=upload_setup_path, blank=True, null=True)
    config_qualy_rain = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_race_safe  = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_race       = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_race_rain  = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 

    data_criacao = models.DateTimeField(default=datetime.now)

    publicado = models.BooleanField(default=False)

    def __str__(self):
        return f"PRIVADO: {self.carro.nome} - {self.pista.nome} ({self.nome_versao})"
    

# --- CLASSE PÚBLICA ---
class SetupPublico(models.Model):
    TIPO_CHOICES = [
        ('S', 'Sprint (Corridas Curtas)'),
        ('E', 'Endurance (Corridas Longas)'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meus_setups_publicos")
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="setups_publicos")
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="setups_publicos")
    
    nome_versao = models.CharField(max_length=50, default="Versão Inicial")
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='S')
    
    # Arquivos
    config_qualy_safe = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_qualy      = models.FileField(upload_to=upload_setup_path, blank=True, null=True)
    config_qualy_rain = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_race_safe  = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_race       = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 
    config_race_rain  = models.FileField(upload_to=upload_setup_path, blank=True, null=True) 

    data_criacao = models.DateTimeField(default=datetime.now)

    # STATUS DE MODERAÇÃO (Para o seu controle de lojas)
    publicado = models.BooleanField(default=False)
    verificado = models.BooleanField(default=False) # Se você testou e aprovou || para saber se não é de alguma loja de setups

    def __str__(self):
        return f"PÚBLICO: {self.carro.nome} - {self.pista.nome} ({self.nome_versao})"
    
class Avaliacao(models.Model):
    setup = models.ForeignKey(SetupPublico, on_delete=models.CASCADE, related_name='avaliações')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrelas = models.PositiveSmallIntegerField()
    comentario = models.TextField(max_length=150)