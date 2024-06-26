# Generated by Django 5.0.4 on 2024-05-19 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_alter_inmueble_imagenes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inmueble',
            name='imagenes',
        ),
        migrations.AlterField(
            model_name='extendusuario',
            name='inmuebles_arrendados',
            field=models.ManyToManyField(blank=True, related_name='arrendatarios', to='web.inmueble', verbose_name='Inmuebles Arrendados'),
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='arrienda_rural/front/assets/media/inmuebles')),
                ('inmueble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='web.inmueble')),
            ],
        ),
    ]
