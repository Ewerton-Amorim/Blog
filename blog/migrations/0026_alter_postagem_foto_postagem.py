# Generated by Django 4.1.5 on 2023-01-19 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0025_rename_tipo_usuario_nivel_acesso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postagem",
            name="foto_postagem",
            field=models.ImageField(
                blank=True,
                default="fotos/post_sem_foto.webp",
                null=True,
                upload_to="fotos/%d/%m/%Y/",
            ),
        ),
    ]