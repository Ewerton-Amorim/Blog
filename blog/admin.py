from django.contrib import admin
from blog.models import Usuario, Postagem, Categorias, Comentario

class ListandoUsuarios(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'data_de_cadastro')
    list_per_page = 5


class ListandoComentarios(admin.ModelAdmin):
    list_display = ('id','comentario', 'usuario')  
    list_per_page = 5


class ListandoPostagens(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'titulo','usuario', 'data_publicacao')     
    list_per_page = 5

admin.site.register(Usuario, ListandoUsuarios)
admin.site.register(Postagem, ListandoPostagens)
admin.site.register(Categorias)
admin.site.register(Comentario, ListandoComentarios)