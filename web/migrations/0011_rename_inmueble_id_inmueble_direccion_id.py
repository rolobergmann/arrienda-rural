# Generated by Django 5.0.4 on 2024-05-17 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_remove_inmueble_direccion_inmueble_inmueble_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inmueble',
            old_name='inmueble_id',
            new_name='direccion_id',
        ),
    ]