from django import forms
# from blog.models import Categorias, Postagem

# class FormPostagem(forms.ModelForm):
#     class Meta:
#         model = Postagem
#         # exclude = ['data_publicacao ', 'usuario', 'foto_postagem ']
#         fields = ['categoria']

class CategoriasForm(forms.Form):
    categoria = forms.CharField(label='Categoria', max_length=100)        
