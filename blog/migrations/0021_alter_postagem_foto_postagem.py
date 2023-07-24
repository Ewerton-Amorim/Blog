# Generated by Django 4.1.5 on 2023-01-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0020_alter_postagem_foto_postagem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postagem",
            name="foto_postagem",
            field=models.ImageField(
                blank=True,
                default="images/post_sem_foto.webp",
                null=True,
                upload_to="fotos/%d/%m/%Y/",
            ),
        ),
    ]