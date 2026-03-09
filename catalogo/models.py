from django.db import models
from datetime import datetime

# Create your models here.
ESCOLHAS_CARRO = [
        ('GT3', 'GT3'),
        ('PCUP', 'PCUP'),
    ]

ESCOLHAS_SETUP = [
        ('QUALY_SAFE', 'QUALY_SAFE'),
        ('QUALY', 'QUALY'),
        ('QUALY_RAIN', 'QUALY_RAIN'),
        ('RACE_SAFE', 'RACE_SAFE'),
        ('RACE', 'RACE'),
        ('RACE_RAIN', 'RACE_RAIN'),
    ]

class Carro(models.Model):
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
    
class Setup(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="setups")
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="setups")
    nome_config = models.CharField(max_length=100, choices=ESCOLHAS_SETUP) 
    arquivo = models.FileField(upload_to="setups/%Y/%m/", blank=True)
    data_criacao = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.carro} - {self.pista} ({self.nome_config})"