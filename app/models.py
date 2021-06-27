from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Leads(models.Model):
    empresa = models.CharField(max_length=100,default='')
    nome = models.CharField(max_length=100, null=True, default="")
    cargo = models.CharField(max_length=500)
    telefone = models.CharField(max_length=15, null=True, default="")
    email =models.CharField(max_length=200, null=True, default="")
    link = models.CharField(max_length=200, null=True, default="")
    def __str__(self):
        if self.nome:
            return self.nome
        return "Problema de Timeout"
    
