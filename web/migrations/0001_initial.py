# Generated by Django 5.0.4 on 2024-05-07 03:35

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_form_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_name', models.CharField(max_length=64)),
                ('message', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=10)),
                ('depto', models.CharField(max_length=50)),
                ('comuna', models.CharField(max_length=50)),
                ('ciudad', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Inmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('m2_construidos', models.IntegerField()),
                ('m2_totales', models.IntegerField()),
                ('estacionamientos', models.IntegerField()),
                ('cantidad_habitaciones', models.IntegerField()),
                ('cantidad_banos', models.IntegerField()),
                ('tipo_de_inmueble', models.CharField(max_length=50)),
                ('precio_arriendo', models.IntegerField()),
                ('direccion', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='web.direccion')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rut', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('nombre_1', models.CharField(max_length=50)),
                ('nombre_2', models.CharField(max_length=50)),
                ('apellido_1', models.CharField(max_length=50)),
                ('apellido_2', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=9)),
                ('tipo_usuario', models.CharField(choices=[('arrendador', 'Arrendador'), ('arrendatario', 'Arrendatario')], default='Arrendatario', max_length=20)),
                ('direccion', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='web.direccion')),
                ('groups', models.ManyToManyField(blank=True, help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de los grupos en los que se encuentra.', related_name='usuario_groups', to='auth.group', verbose_name='Grupos')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Permisos específicos para este usuario.', related_name='usuario_permissions', to='auth.permission', verbose_name='Permisos del usuario')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
