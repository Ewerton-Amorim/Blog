from django.db import models
from django import forms
from django.forms import PasswordInput
from datetime import datetime



class Categorias(models.Model):
    categoria = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self):
        return self.categoria



class Usuario(models.Model):

    nivel_acesso = (
        ('ADM','Administrador'),
        ('AU', 'Autor'),
        ('UC', 'Usuário comum'),
    )
    nome = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, max_length=30, unique=True)
    senha = models.CharField(max_length= 64, blank=False)
    data_de_cadastro = models.DateTimeField(default=datetime.now, blank=True)
    nivel_acesso = models.CharField(max_length=13, choices=nivel_acesso, blank=False, null=False, default='UC')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


def default_foto_postagem():
    return 'foto/programacao.jpg'


class Postagem(models.Model):
    
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, blank=False)
    publicacao = models.TextField(max_length=1000, blank=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(default=datetime.now, blank=True)
    foto_postagem = models.ImageField(upload_to='fotos/%d/%m/%Y/', blank=True, default=default_foto_postagem)
 
    def __str__(self):
        return self.titulo




class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=100)
    criadoEm = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=False)







