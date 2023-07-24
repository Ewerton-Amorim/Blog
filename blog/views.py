

from django.shortcuts import render, redirect
from .models import Postagem, Usuario, Categorias, Comentario
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth, messages
from datetime import datetime
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from fpdf import FPDF




def cadastro_usuario_comum(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        senha = request.POST["senha"]
        senha2 = request.POST["senha2"]

        if campo_vazio(nome):
            messages.error(request, 'o campo nome não pode ficar em branco')
            return render(request, "blog/cadastro.html")

        if campo_vazio(email):
            messages.error(request, 'O campo email não pode ficar em branco')
            return render(request, "blog/cadastro.html")
        if campo_vazio(senha):
            messages.error(request, 'O campo senha não pode ficar em branco')
            return redirect('cadastro')
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado com esse e-mail')
            return render(request, "blog/cadastro.html")

        if valida_senhas_diferentes(senha, senha2):
            messages.error(request, 'as senhas precisam ser iguais')
            return render(request, "blog/cadastro.html")

        user = Usuario(nome=nome, email=email, senha=senha)
        user.save()
        messages.success(request, 'usuário cadastrado com sucesso')
        return redirect("login")

    return render(request, "blog/cadastro.html")

def cadastro_autor(request):
    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        print(e)
        return redirect('login')

    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")

        if campo_vazio(nome):
            print("o campo nome não pode ficar em branco")
            return render(request, "blog/dashboardAdm.html")

        if campo_vazio(email):
            print("O campo email não pode ficar em branco")
            return render(request, "blog/dashboardAdm.html")

        if Usuario.objects.filter(email=email).exists():
            print("Usuário já cadastrado")
            return render(request, "blog/dashboardAdm.html")

        if valida_senhas_diferentes(senha, senha2):
            print("as senhas precisam ser iguais")
            return render(request, "blog/dashboardAdm.html")

        user = Usuario(nome=nome, email=email, senha=senha, nivel_acesso="AU")
        user.save()


        print("autor cadastrado com sucesso")
        return render(request,"blog/dashboardAdm.html")

    else:
        return render(request, "blog/dashboardAdm.html")

def postagem(request, postagem_id):
    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')    
    user_id = request.session.get("user_id")
    user = Usuario.objects.filter(id=user_id)
    post = Postagem.objects.get(pk=postagem_id)
   
    
    return render(request, 'blog/postagens.html', {
        'postagem':post,
        'usuarios':user,
    })


def criar_postagem(request):

    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')  

    categorias = Categorias.objects.all()
    postagens = Postagem.objects.order_by('-data_publicacao')

    if request.method == "POST":
        categoria = request.POST.get("categoria")
        titulo = request.POST.get("titulo")
        publicacao = request.POST.get("publicacao")
        foto_postagem = request.FILES.get("pictureInput") #usando o get eu pego apenas um arquivo, para pegar mais de um, usa-se o getlist e fazer algumas outras

        user_id = request.session["user_id"]

        categoria_filter_query = Categorias.objects.filter(categoria=categoria).first()
        usuario = Usuario.objects.filter(
            id=user_id,
        ).first()
        
        if 'pictureInput' in request.FILES:

            postagem_com_foto = Postagem(
                categoria=categoria_filter_query,
                usuario=usuario,
                titulo=titulo,
                publicacao=publicacao,
                foto_postagem=foto_postagem
            )
            
            postagem_com_foto.save()
        else:
            messages.error(request, 'A postagem precisa de uma foto')
            return redirect('criar_postagem')    
        messages.success(request, 'Postagem feita com sucesso')
        return redirect('criar_postagem')



    return render(request, "blog/criar_postagem.html", {"categorias": categorias, 'postagens': postagens})


def editar_postagem(request, postagem_id):

    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')    

    post = Postagem.objects.get(pk=postagem_id)
    categorias = Categorias.objects.all()
 
    return render(request,'blog/editar_postagem.html',{
        'categorias': categorias,
        'postagem':post
    })

def atualiza_postagem(request):

    
    if request.method == 'POST':
       
        new_categoria = request.POST['categoria']
        postagem_id = request.POST['postagem_id']
        postagem = Postagem.objects.get(pk=postagem_id)
        if new_categoria:
            categoria = Categorias.objects.get(categoria=new_categoria)
            if postagem.categoria != categoria:
                postagem.categoria = categoria
        postagem.titulo = request.POST['titulo']
        postagem.publicacao = request.POST['publicacao']

    
        if 'pictureInput' in request.FILES:
            postagem.foto_postagem = request.FILES['pictureInput']

        if postagem:
            postagem.save() 
            # messages.success(request, 'Postagem editada com sucesso')
            return redirect('index')           

def criar_comentario(request, postagem_id):

    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')    
    postagens = Postagem.objects.filter(id=postagem_id).first()
   
    if request.method == 'POST':

        postagem = Postagem.objects.get(id=postagem_id)
        user_id = request.session.get('user_id')
        usuario = Usuario.objects.get(id=user_id)
        comentario_input = request.POST.get('comentario_input')

        comentario = Comentario(comentario=comentario_input, postagem=postagem, usuario=usuario)
        comentario.save()


        return redirect('postagem', postagem_id)    
    return render(request, 'blog/criar_comentario.html',{
        'postagens': postagens,
        
    })    

def deleta_postagem(request, postagem_id): 

    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')    

    post = Postagem.objects.get(pk=postagem_id)
    if request.method == 'POST':
        post.delete()
        return redirect('index')

    return render(request, 'blog/deleta_postagem.html', {
        'postagem':post
    })
   
def cadastro_categoria(request):

    try:
        usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')    
    if request.method == "POST":
        categoria = request.POST["categoria"]
        print(categoria)

        if campo_vazio(categoria):
            print("O campo categoria não pode ficar vazio")
            return render(request, "blog/dashboardAdm.html")

        if Categorias.objects.filter(categoria=categoria).exists():
            print("categoria já cadastrada")
            return render(request, "blog/dashboardAdm.html")
        categoria = Categorias(categoria=categoria)
        categoria.save()
        print("categoria cadastrada com sucesso")
        return render(request, "blog/dashboardAdm.html")
        # return redirect('blog/dashboardAdm')

    return render(request, "blog/dashboardAdm.html")

def buscar(request):
    try:
        Usuario_tipo = request.session['usuario_tipo']
    except Exception as e:
        return redirect('login')    

    postagens = Postagem.objects.order_by('-data_publicacao')
    user_id = request.session.get("user_id")
    user = Usuario.objects.filter(id=user_id).first()

    if 'buscar' in request.GET:
        titulo_postagem = request.GET['buscar']

        if 'buscar':
            postagens = postagens.filter(titulo__icontains=titulo_postagem)
    return render(request, 'blog/buscar.html', {
        'postagem': postagens,
        'usuario': user,
        'user_id': user_id
    })

def login(request):

    if request.method != "POST":
        return render(request, 'blog/login.html')

    email = request.POST["email"]
    senha = request.POST["senha"]
    usuario = Usuario.objects.filter(
        email=email, senha=senha
    ).first() # pegando um usuário


    try:
        request.session['user_id'] = usuario.id
        request.session['usuario_tipo'] = usuario.nivel_acesso
    except:
        messages.error(request, 'Senha ou e-mail inválidos')
        return redirect('login')
    # print(usuario.nivel_acesso)
    if not usuario:  
        return redirect('login') 
    
    usuario_tipo = request.session['usuario_tipo']
    if usuario.nivel_acesso == "ADM":
        # return redirect('index')

        return redirect('cadastro_autor')
        # return render(request, 'blog/dashboardAdm.html')
    if usuario.nivel_acesso == "UC":
        return redirect('index')

        # return redirect("dashboard") # falta designar url para usuario comum
    if usuario.nivel_acesso == "AU":
        # return render(request,"blog/dashboardAutor.html")
        print('logado com autor')
        return redirect('index')
   
def logout(request):
    auth.logout(request)
    print("usario deslogado")
    return redirect('index')


def index(request):

    post = Postagem.objects.order_by("-data_publicacao")
    user_id = request.session.get("user_id")
    user = Usuario.objects.filter(id=user_id)
    paginator = Paginator(post, 9)
    page = request.GET.get("page")
    post_por_pagina = paginator.get_page(page)


    dados = {
        "posts": post_por_pagina,
        "usuarios": user
        }

   

    if user_id: 
        usuario_logado = Usuario.objects.filter(id=user_id).first()
        dados['user_id'] = user_id

    if not user_id:
        return redirect('login')

    return render(request, "blog/index.html", dados)


def dashboard(request):


    return render(request, "blog/dashboardUsuarioComum.html")




def reserva_linha(cnv, posY):

    posY-= 20

    if posY < 10:
        posY = 810
        cnv.showPage()
        cnv.setFont("Helvetica", 10)

    return posY    

def gera_pdf(request):

    buffer = io.BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)
    cnv.setFont("Helvetica", 10)

    postagens = Postagem.objects.all()


    # posXInicial = 50
    posY = 810

    for postagem in postagens:

        posY = reserva_linha(cnv, posY)

        cnv.drawString(20, posY, 'Autor')
        cnv.drawString(120, posY, postagem.usuario.nome)
        posY = reserva_linha(cnv, posY)
        cnv.drawString(20, posY, 'Título')
        cnv.drawString(120, posY, postagem.titulo)
        posY = reserva_linha(cnv, posY)
        cnv.drawString(20, posY, 'Categoria')
        cnv.drawString(120, posY, postagem.categoria.categoria)
        posY = reserva_linha(cnv, posY)
        posY = reserva_linha(cnv, posY)
        cnv.drawString(20, posY, 'Data de publicação')
        cnv.drawString(120, posY, postagem.data_publicacao.strftime(" %d,%b,%Y"))
        posY = reserva_linha(cnv, posY)
        cnv.drawString(20, posY,'Postagem')
        
        for post in frase_generator(iter(postagem.publicacao.split(' '))):
        
            cnv.drawString(120, posY, post)
            posY = reserva_linha(cnv, posY)

    cnv.showPage()
    cnv.save()
    buffer.seek(0)
          

    return FileResponse(buffer, as_attachment=True, filename='postagens.pdf')




def frase_generator(lista_palavras):


    palavra = next(lista_palavras)

    frase = f'{palavra} '

    try:
        
        while True:
            
            palavra = next(lista_palavras)
            length_frase_atual = len(frase)
                
            if length_frase_atual + len(f'{palavra} ') < 90:
                frase += f'{palavra} '
                
                continue
            yield frase
            frase = f'{palavra} '
        
    except StopIteration:
        yield frase

# ***** fuções usadas para fazer verificações***#
def campo_vazio(campo):
    return not campo.strip()


def valida_senhas_diferentes(senha, senha2):
    """Método que verifica se duas senhas são diferentes"""
    return senha != senha2
