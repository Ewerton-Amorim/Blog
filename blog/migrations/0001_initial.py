# Generated by Django 4.1.5 on 2023-01-08 22:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('senha', models.CharField(max_length=64)),
                ('data_de_cadastro', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('nivel_acesso', models.CharField(choices=[('Administrador', 'Administrador'), ('Autor', 'Autor'), ('Usuario_comum', 'Usuário comum')], default='UC', max_length=13)),
                ('ativo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Postagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(choices=[('Programação', 'Programação'), ('Games', 'Games'), ('Hardware', 'Hardware')], default='Programação', max_length=11)),
                ('titulo', models.CharField(max_length=100)),
                ('publicacao', models.TextField(max_length=1000)),
                ('data_publicacao', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.usuario')),
            ],
        ),
    ]