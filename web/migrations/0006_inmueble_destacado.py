# Generated by Django 5.0.4 on 2024-05-15 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_rename_imagen_inmueble_imagenes'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='destacado',
            field=models.BooleanField(default=False),
        ),
    ]
