# Generated by Django 4.1.5 on 2023-01-12 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_postagem_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postagem',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Postagem', to='blog.categorias', verbose_name='categoria'),
        ),
    ]
