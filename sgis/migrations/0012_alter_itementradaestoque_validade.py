# Generated by Django 5.1.7 on 2025-04-09 00:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgis', '0011_itementradaestoque_lote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itementradaestoque',
            name='validade',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
