# Generated by Django 4.1.5 on 2023-01-15 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_alter_postagem_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postagem",
            name="foto_postagem",
            field=models.ImageField(upload_to="fotos/%d/%m/%Y/"),
        ),
    ]
