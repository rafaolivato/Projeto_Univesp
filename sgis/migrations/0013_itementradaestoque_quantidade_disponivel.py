# Generated by Django 5.1.7 on 2025-04-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgis', '0012_alter_itementradaestoque_validade'),
    ]

    operations = [
        migrations.AddField(
            model_name='itementradaestoque',
            name='quantidade_disponivel',
            field=models.IntegerField(default=0),
        ),
    ]
