# Generated by Django 5.0.4 on 2024-05-17 03:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_rename_inmueble_id_inmueble_direccion_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendusuario',
            name='inmuebles_publicados',
        ),
        migrations.AddField(
            model_name='inmueble',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]