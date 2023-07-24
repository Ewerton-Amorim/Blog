from django.urls import path
from .import views 


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro_usuario_comum, name='cadastro'),
    path('postagem/<int:postagem_id>', views.postagem, name='postagem'),
    path('cadastro_autor/', views.cadastro_autor, name='cadastro_autor'),
    path('cadastro_categoria/', views.cadastro_categoria, name='cadastro_categoria'),
    path('criar_postagem/', views.criar_postagem, name='criar_postagem'),
    path('editar_postagem/<int:postagem_id>', views.editar_postagem, name='editar_postagem'),
    path('atualiza_postagem/', views.atualiza_postagem, name='atualiza_postagem'),
    path('deleta_postagem/<int:postagem_id>', views.deleta_postagem, name='deleta_postagem'),
    path('criar_comentario/<int:postagem_id>', views.criar_comentario, name='criar_comentario'),
    path('buscar/', views.buscar, name='buscar'),
    path('gera_pdf/', views.gera_pdf, name='gera_pdf'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
] 