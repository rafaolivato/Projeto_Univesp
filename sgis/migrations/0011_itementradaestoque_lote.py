# Generated by Django 5.1.7 on 2025-04-01 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgis', '0010_remove_entradaestoque_lote_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itementradaestoque',
            name='lote',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
