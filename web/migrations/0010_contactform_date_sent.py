# Generated by Django 5.0.4 on 2024-05-06 16:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_contactform'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='date_sent',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
