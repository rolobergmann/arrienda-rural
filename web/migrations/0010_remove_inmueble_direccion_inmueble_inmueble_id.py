# Generated by Django 5.0.4 on 2024-05-17 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_extendusuario_inmuebles_publicados_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inmueble',
            name='direccion',
        ),
        migrations.AddField(
            model_name='inmueble',
            name='inmueble_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.direccion'),
        ),
    ]